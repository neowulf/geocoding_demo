## Geocoding Demo

### Requirements

1. Implemented in Python
1. Support Multiple Geocoding Services
1. Implements Fallback To Backup Geocoding Services
1. RESTful HTTP Interface
1. JSON for Data Serialization
1. Provides Documentation - How To Run The Service
1. Provides Documentation - How To Use The Services API
1. Uses git and github for for revision control

### Non-Requirements

1. Does Not Have To Be Performant or Scalable

### Resources

1. [Geocoding Service by HERE](https://developer.here.com/documentation/geocoder/topics/quick-start.html)
1. [Geocoding Service by Google](https://developers.google.com/maps/documentation/geocoding/start##Design)

## How To Run

### Sample Invocation

```bash
curl 'localhost:8000/reverse_geocode?latlng=41.8842,-87.6388&provider=google' -v
```

### Running the Tests

Setup the conda environment
```bash
conda env create -f conda_environment.yml
source activate geocoding_demo
```

To run the unit tests:
```bash
python -m unittest tests
```

To run the api tests:
```bash
python driver.py
./tests.sh
```

### Docker Invocation
TODO

## Design

1. Use strategy pattern to switch between the various Geocoding Services.
1. If an exception occurs when invoking the requested API, fallback to the default API.

## Assumptions

1. The following tools are available on the host machine:
    1. conda
    1. docker
    1. bash
    1. curl
1. Google provider is the fallback provider.
1. Google api - provides the first found `street_address`.
1. Here api - provides the first found `houseNumber`.
 