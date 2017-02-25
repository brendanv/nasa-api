`nasa` provides a simple Python wrapper to interact with the [NASA Data APIs](https://data.nasa.gov/developer/external/planetary/). Full documentation for the APIs is available on [NASA's site](https://data.nasa.gov/developer/external/planetary/), and named parameters here are the same as there.


Installation
------------

Install using `pip`:

    pip install nasa-api-wrapper

If you'd like to contribute, feel free to run `git clone` on the Github repository:

    git clone https://github.com/brendanv/nasa-api.git


Usage
-----

[Acquire an API key](https://data.nasa.gov/developer/external/planetary/#apply-for-an-api-key) and set your API key as the NASA_API_KEY environment variable before using the API!

Supported APIs
-------

### Astronomy Picture of the Day

Receive images and metadata about NASA's current and past [Astronomy Pictures of the Day](http://apod.nasa.gov/apod/astropix.html). Just choose a date, and indicate if you'd like to receive the set of tags for the image along with your other data.

```python
>>> from nasa import apod
>>> picture = apod.apod('2015-05-01')
>>> picture.url
'http://apod.nasa.gov/apod/image/1505/messengerImpactSite_black600.jpg'
>>> picture.title
"MESSENGER's Last Day on Mercury"
```

### Earth Assets and Imagery

Fetch Landsat 8 images of any location on Earth! This consists of two distinct APIs: [Assets](https://api.nasa.gov/api.html#assets) that detail when a picture was taken of a given location, and the actual [Imagery](https://api.nasa.gov/api.html#imagery) for that location and time.

You can use the Assets API to fetch images:
```python
>>> from nasa import earth
>>> assets = earth.assets(lat=1.5, lon=100.75, begin='2014-02-01', end='2014-06-01')
>>> [(a.date, a.id) for a in assets]
[('2014-02-04T03:30:01', 'LC8_L1T_TOA/LC81270592014035LGN00'),
 ('2014-02-20T03:29:47', 'LC8_L1T_TOA/LC81270592014051LGN00'),
 ...
 ('2014-05-27T03:28:32', 'LC8_L1T_TOA/LC81270592014147LGN00')]

>>> image = assets[0].get_asset_image()
>>> image.id
'LC8_L1T_TOA/LC81270592014035LGN00"'
>>> image.image.__str__()
'<PIL.PngImagePlugin.PngImageFile image mode=RGB size=512x512>'
```

Or simply fetch the images directly:
```python
>>> from nasa import earth 
>>> image = earth.image(lat=1.5, lon=100.75, date='2014-02-01')
>>> image.id
'LC8_L1T_TOA/LC81270592014035LGN00'
```

### Patents

See what cool patents are held in the NASA patent portfolio using the [Patents API](https://api.nasa.gov/api.html#patents).

```python
>>> from nasa import patents
>>> patents = patents.patents(query='temperature', limit=5)
>>> [(p.id, p.category) for p in patents]
[('patent_MSC-24506-1', 'aeronautics'),
 ('patent_LEW-18761-1', 'materials and coatings'),
 ('patent_LEW-18561-1', 'materials and coatings'),
 ('patent_LEW-18949-1', 'materials and coatings'),
 ('patent_LAR-17681-1', 'materials and coatings')]
```

### Sounds

Browse sounds released by NASA using the [Sounds API](https://api.nasa.gov/api.html#sounds).

```python
>>> from nasa import sounds
>>> sounds = sounds.sounds(query='apollo')
>>> [(s.id, s.duration) for s in sounds]
[(181835738, 18365),
 (173578614, 30095),
 ...
 (172463116, 2429)]
```

### [MAAS](http://marsweather.ingenology.com/#get_started)
Browse reports from the Mars Atmospheric Aggregation System

Easily get the latest report:

```python
>>> from nasa import maas
>>> report = maas.latest()
>>> report.min_temp_fahrenheit
-110.2
```

Or multiple reports that match a given query:

```python
>>> from nasa import maas
>>> reports = maas.archived(terrestrial_date_start='2012-10-01', terrestrial_date_end='2012-10-31')
>>> reports['count']
508
>>> [r.sol for r in reports['results']]
[84, 83, 82, 81, 80, 79, 78, 77, 76, 75]

# Get the next page of results
>>> paginator = reports['next']
>>> next_page = paginator()
>>> [r.sol for r in next_page['results']]
[74, 73, 72, 71, 70, 68, 67, 66, 65, 64]
```

`archived` takes keyword args that allow you to filter by most report fields available on the MAASReport.
