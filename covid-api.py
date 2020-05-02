import csv
import datetime
import requests
import json
from io import StringIO
from flask import Flask
import flask
import threading
import time
from flask import request


US = 'https://raw.github.com/nytimes/covid-19-data/master/us.csv'
US_STATES = 'https://raw.github.com/nytimes/covid-19-data/master/us-states.csv'
US_COUNTIES = 'https://raw.github.com/nytimes/covid-19-data/master/us-counties.csv'

app = Flask(__name__)


def logging(*args):
    print('DEBUG: \t', end='')
    for log in args:
        print(log, end=' ')
    print()


def write_json_to_file(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f)


def csv_to_json(raw_data):
    csv_reader = csv.reader(StringIO(raw_data), delimiter=',')
    line_count = 0
    json_list = list()
    headers = list()
    for row in csv_reader:
        if line_count == 0:
            headers = row
            line_count += 1
        else:
            data = dict()
            for index in range(len(row)):
                data[headers[index]] = row[index]
            json_list.append(data)
    return json_list


def get_data(url):
    logging('Requesting for url : ', url)
    r = requests.get(url)
    if r.status_code == 200:
        logging('Request Successfull')
        return r.text
    logging('Request failed')
    return None


def create_metadata(data):
    states = set()
    counties = set()
    dates = set()
    for row in data:
        states.add(row['state'])
        counties.add(row['county'])
        dates.add(row['date'])
    states = sorted(states)
    counties = sorted(counties)
    dates = sorted(dates)
    return {'states': states, 'counties': counties, 'dates': dates}


def reload():
    logging('Reloading data')
    data = get_data(US)
    if data is not None:
        write_json_to_file('us_data.json', csv_to_json(data))
    else:
        logging('Failed reloading data', US)
    data = get_data(US_STATES)
    if data is not None:
        write_json_to_file('us_states.json', csv_to_json(data))
    else:
        logging('Failed reloading data', US_STATES)
    data = get_data(US_COUNTIES)
    if data is not None:
        json_data = csv_to_json(data)
        write_json_to_file('us_counties.json', json_data)
        write_json_to_file('metadata.json', create_metadata(json_data))
    else:
        logging('Failed reloading data', US_COUNTIES)

    logging('Done reloading')


def reload_worker():
    logging('Reload Worker Started.')
    try:
        while True:
            reload()
            logging('Sleeping for 2 hrs')
            time.sleep(7200)
    except:
        reload_worker()


def read_filter_data(file_name, req_args):
    with open(file_name) as f:
        data = json.load(f)
        if len(req_args) == 0:
            return json.dumps(data)
        filtered_data = list()
        for row in data:
            for arg in req_args.keys():
                if arg in row:
                    value = str(req_args.get(arg))
                    if '<' in value:
                        try:
                            if int(row[arg]) < int(value.replace('<', '')):
                                filtered_data.append(row)
                        except:
                            if (row[arg]) < value.replace('<', ''):
                                filtered_data.append(row)
                    elif '>' in value:
                        try:
                            if int(row[arg]) > int(value.replace('>', '')):
                                filtered_data.append(row)
                        except:
                            if (row[arg]) > value.replace('>', ''):
                                filtered_data.append(row)
                    elif value.lower() in row[arg].lower():
                        filtered_data.append(row)
        return json.dumps(filtered_data)


def us_endpoint():
    resp = flask.Response(read_filter_data('us_data.json', request.args))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.content_type = 'application/json'
    return resp


def us_states_endpoint():
    resp = flask.Response(read_filter_data('us_states.json', request.args))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.content_type = 'application/json'
    return resp


def us_counties_endpoint():
    resp = flask.Response(read_filter_data('us_counties.json', request.args))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.content_type = 'application/json'
    return resp


def metadata():
    resp = flask.Response(read_filter_data('metadata.json', {}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.content_type = 'application/json'
    return resp


def reload_on_demand():
    reload()
    return {'Success': True}


app.add_url_rule('/', 'us_endpoint', us_endpoint)
app.add_url_rule('/states/', 'us_states_endpoint', us_states_endpoint)
app.add_url_rule('/counties/', 'us_counties_endpoint', us_counties_endpoint)
app.add_url_rule('/metadata/', 'metadata', metadata)
app.add_url_rule('/reload/', 'reload', reload_on_demand)


if __name__ == '__main__':
    t1 = threading.Thread(target=reload_worker, args=())
    t1.start()
    app.run(debug=False)
    t1.join()
