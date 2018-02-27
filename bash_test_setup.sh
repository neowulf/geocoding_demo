#!/usr/bin/env bash

TMP_DIR="tmp"
rm -rf ${TMP_DIR} && mkdir ${TMP_DIR}

# https://coderwall.com/p/nsso8w/using-shell-script-to-test-your-server

## Unit-Testable Shell Scripts (http://eradman.com/posts/ut-shell-scripts.html)
typeset -i tests_run=0
function try { this="$1"; }
trap 'printf "$0: exit code $? on line $LINENO\nFAIL: $this\n"; exit 1' ERR
function assert {
    let tests_run+=1
    [ "$1" = "$2" ] && { echo -n "."; return; }
    printf "\nFAIL: $this\n'$1' != '$2'\n"; exit 1
}

function assert_regex {
    let tests_run+=1
    [[ "$2" =~ $1 ]] && { echo -n "."; return; }
    printf "\nFAIL: $this\n'$1' != '$2'\n"; exit 1
}

## end

# Sample invocation: timeout 2 "wsdump.py ws://localhost:8080/websocket_endpoint"
function timeout {
    time=$1

    # start the command in a subshell to avoid problem with pipes
    # (spawn accepts one command)
    command="/bin/sh -c \"$2\""
    expect -c "set echo \"-noecho\"; set timeout $time; spawn -noecho $command; expect timeout { exit 1 } eof { exit 0 }"
    if [ $? = 1 ] ; then
        echo "Timeout after ${time} seconds"
    fi
}

# Check if jq exists
type jq >/dev/null 2>&1 || { echo -e >&2 "jq is required.\n Visit https://stedolan.github.io/jq for more information.\n Aborting."; exit 1; }


# Check if wsdump.py exists
# type wsdump.py >/dev/null 2>&1 || { echo -e >&2 "Python websocket client utility is required.\n Execute \`pip install websocket-client\`.\n Aborting."; exit 1; }

URL="http://localhost:8000"
