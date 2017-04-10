=======
MARTApy
=======
A Python-based library for accessing the MARTA API.

More: http://www.itsmarta.com/app-developer-resources.aspx


Quickstart
============
Installation
------------
To install via *pip*, just:

.. code-block:: bash

    $ pip install martapy

Or, locally from the same directory as ``setup.py``:

.. code-block:: bash

    $ python setup.py install


Example use
-----------

To get a list of train arrivals:

.. code-block:: python

    from martapy.rail import RailClient

    rail_client = RailClient(api_key="your_api_key")
    arrivals = rail_client.arrivals()

This returns an instance of ``martapy.rail.Arrivals(list)`` which
has a few handy methods to filter results further.

For example, to print the destination and waiting time for upcoming
arrivals at *Peachtree Center Station*:

.. code-block:: python

    from martapy.rail import RailClient

    rail_client = RailClient(api_key="your_api_key")
    peachtree_station = rail_client.arrivals().by_station('peachtree')

    for arrival in peachtree_station:
        print("To: {}, When: {}".format(arrival.destination, arrival.waiting_time))

With output that would look something like::
    To: Airport, When: Arriving
    To: Lindbergh, When: 16 min
    To: Doraville, When: 19 min

Filters
-------

To narrow results, ``martapy.rail.Arrivals(list)`` has
a number of properties/methods:

- Arrivals by **line**:
  ``red_line``
  ``blue_line``
  ``green_line``
  ``gold_line``
- Arrivals by **direction**:
  ``northbound``
  ``eastbound``
  ``westbound``
  ``southbound``
- Arrivals by **waiting time**:
  ``boarding``
  ``arriving``
  ``arrived``
- Arrivals grouped by **station name**:
  ``Arrivals.stations``
- Arrivals grouped by **train ID**:
  ``Arrivals.trains``
- Arrivals associated with a **specific station**:
  ``Arrivals.by_station('station name')``

These can be chained as well for more specific results. For example, to
get all arrivals for the red line which are heading southbound:

.. code-block:: python

    from martapy.rail import RailClient

    rail_client = RailClient(api_key="your_api_key")
    arrivals = rail_client.arrivals().red_line.southbound


Other properties
----------------
Each ``Arrivals`` instance returned is just a list of
``martapy.rail.Arrival`` objects, with properties similar to the filters
above (*station, direction, event\_time, line...*). To get the original
JSON string back, use ``Arrival.json``.
