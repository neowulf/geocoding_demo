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

## Build and Deployment

1. [Optional Step] - Setup environment:
    ```bash
    vagrant plugin install vagrant-vbguest
    vagrant up
    vagrant ssh
    
    # FIXME make the following two sentences part of the Vagrantfile
    bash miniconda.sh -b
    PATH="${HOME}/miniconda3/bin:$PATH"
    
    cd /vagrant
    ```
1. Setup the conda environment:
    ```bash
    conda env create -f conda_environment.yml
    source activate geocoding_demo
    ```
1. Build the docker image.
    ```bash
    ansible-playbook --ask-vault-pass playbook.yml
    ```
1. Provide the ansible vault password.
1. The docker image will only get created if the unit tests succeed without any failure.
1. Run the docker image.
    ```bash
    docker run -d -p 8000:8000 geocoding/demo
    ```
1. The server should be running in the background. 
1. Execute the following to test the http server:
    ```bash
    ./tests.sh http://localhost:8000
    ```

## Usage

1. The following query parameters need to be provided:
    1. `latlng=latitude,longitude`
    1. `provider` can be either `google` or `here`.

### Google Provider:

```bash
curl 'localhost:8000/reverse_geocode?latlng=41.8842,-87.6388&provider=google' -v
```

### Here Provider:

```bash
curl 'localhost:8000/reverse_geocode?latlng=41.8842,-87.6388&provider=here' -v
```


### Running the Tests

1. Run the unit tests:
```bash
python -m unittest tests
```

1. Run the http server tests:
```bash
./tests.sh http://localhost:8000
```

## Assumptions

1. The following tools are available on the host machine:
    1. conda
    1. docker
    1. bash
    1. curl
    1. jq
1. Google provider is the fallback provider. This could have been extracted into the `config.ini`.
1. Google api - provides the first `street_address` match.
1. Here api - provides the first `houseNumber` match.
1. `config.ini.j2` is a jinja file which will eventually reside as `config.ini` where the real secrets need 
    to be filled for the different providers. 
    1. `ansible` provides the `config.ini` when building the docker image.
    1. If the `config.ini` is missing or incorrect - the docker image won't be built due to failing tests.