Covid 19 API's for USA
Data source New York Times https://github.com/nytimes/covid-19-data.

API Docs : https://documenter.getpostman.com/view/10051991/SzmZdLWK?version=latest

 GET 'https://blooming-basin-33031.herokuapp.com/'

```
[
  {
    "date": "2020-01-21",
    "cases": "1",
    "deaths": "0"
  },
  {
    "date": "2020-01-22",
    "cases": "1",
    "deaths": "0"
  },
  {
    "date": "2020-01-23",
    "cases": "1",
    "deaths": "0"
  },
  {
    "date": "2020-01-24",
    "cases": "2",
    "deaths": "0"
  },
  {
    "date": "2020-01-25",
    "cases": "3",
    "deaths": "0"
  }
]
```

 GET 'https://blooming-basin-33031.herokuapp.com/states/'
```
[
  {
    "date": "2020-01-21",
    "state": "Washington",
    "fips": "53",
    "cases": "1",
    "deaths": "0"
  },
  {
    "date": "2020-01-22",
    "state": "Washington",
    "fips": "53",
    "cases": "1",
    "deaths": "0"
  },
  {
    "date": "2020-01-23",
    "state": "Washington",
    "fips": "53",
    "cases": "1",
    "deaths": "0"
  },
  {
    "date": "2020-01-24",
    "state": "Illinois",
    "fips": "17",
    "cases": "1",
    "deaths": "0"
  }
]
 ```
 
GET 'https://blooming-basin-33031.herokuapp.com/counties

```
[
  {
    "date": "2020-04-24",
    "county": "New York City",
    "state": "New York",
    "fips": "",
    "cases": "150484",
    "deaths": "11157"
  },
  {
    "date": "2020-04-25",
    "county": "New York City",
    "state": "New York",
    "fips": "",
    "cases": "155124",
    "deaths": "11419"
  },
  {
    "date": "2020-04-26",
    "county": "New York City",
    "state": "New York",
    "fips": "",
    "cases": "158268",
    "deaths": "11648"
  },
  {
    "date": "2020-04-27",
    "county": "New York City",
    "state": "New York",
    "fips": "",
    "cases": "160499",
    "deaths": "11857"
  }
]
```
