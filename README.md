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

### Test
TODO

### Docker Invocation
TODO

## Design

1. Use strategy pattern to switch between the various Geocoding Services.
1. If an exception occurs when invoking the requested API, fallback to the default API.

