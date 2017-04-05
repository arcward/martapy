# MARTApy
A Python-based library for accessing the MARTA API.

More info: http://www.itsmarta.com/app-developer-resources.aspx

## Installation

To install, just run `python setup.py install`

## Example use
To get a list of arrivals:
```python
from martapy.rail import RailClient

rail_client = RailClient(api_key="your_api_key")
arrivals = rail_client.arrivals()
```
This returns an instance of `martapy.rail.Arrivals(list)`, 
with various methods to filter results.

For example, to print the destination and waiting time for upcoming arrivals at
Peachtree Center Station:
```python
from martapy.rail import RailClient

rail_client = RailClient(api_key="your_api_key")
peachtree_station = rail_client.arrivals().by_station('peachtree')

for arrival in peachtree_station:
    print("To: {}, When: {}".format(arrival.destination, arrival.waiting_time))
```
With output similar to:
```
To: Airport, When: Arriving
To: Lindbergh, When: 16 min
To: Doraville, When: 19 min
```

### Filters
To narrow down results, `martapy.rail.Arrivals(list)` has these 
properties/methods:

* Arrivals by **line**: 
  * `red_line`
  * `blue_line`
  * `green_line`
  * `gold_line`
* Arrivals by **direction**:
  * `northbound`
  * `eastbound`
  * `westbound`
  * `southbound`
* Arrivals by **waiting time**:
  * `boarding`
  * `arriving`
  * `arrived`
* `Arrivals.by_station('station name')` returns all arrivals for a specific
station
* `Arrivals.trains` Returns each train and its associated arrivals: (as an 
_OrderedDict_ with train IDs as keys, and that train's list of arrivals as 
its value)
* `Arrivals.stations` returns each station and its associated arrivals (as an  
_OrderedDict_ with station names as keys, list of arrivals as its value)

These can be chained as well for more specific results. For example, to get all 
arrivals for the red line which are heading southbound:

```python
from martapy.rail import RailClient

rail_client = RailClient(api_key="your_api_key")
arrivals = rail_client.arrivals().red_line.southbound
```

### Other properties
Each `Arrivals` instance returned is just a list of 
`martapy.rail.Arrival` objects, with properties similar to the 
filters above (*station, direction, event_time, line...*). To get 
the original JSON string back, use `Arrival.json`.
