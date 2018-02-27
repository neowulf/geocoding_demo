#!/bin/bash

#####
# Usage
#   ./tests.sh http://localhost:8000
#####

. ./bash_test_setup.sh

server="${1:-http://localhost:8001}"

try "Bad Request - Incorrect Query Parameters - LatLng"
assert '400' $(curl -s -o /dev/null -w "%{http_code}"  "${server}/reverse_geocode?latlng=41.8842")

try "Bad Request - Incorrect Parameters - Missing Provider"
assert '400' $(curl -s -o /dev/null -w "%{http_code}"  "${server}/reverse_geocode?latlng=41.8842,-87.6388")

try "Bad Request - Not Found"
assert '404' $(curl -s -o /dev/null -w "%{http_code}"  "${server}/invalid_api")

try "Good Request - Google"
get_result=$(curl -s "${server}/reverse_geocode?latlng=41.8842,-87.6388&provider=google")
assert 'Google' `echo ${get_result} | jq -r .provider`
assert '425 W Randolph St, Chicago, IL 60606, USA' "$(echo ${get_result} | jq -r .result[0])"

try "Good Request - Here"
get_result=$(curl -s "${server}/reverse_geocode?latlng=41.8842,-87.6388&provider=here")
assert 'Here' `echo ${get_result} | jq -r .provider`
assert '425 W Randolph St, Chicago, IL 60606, United States' "$(echo ${get_result} | jq -r .result[0])"


