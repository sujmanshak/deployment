#!/usr/bin/env bash

function server() {
    sudo kill `sudo lsof -t -i:8000`
    cd server
    python HTTPListener.py &
    cd -
}

function tests() {
    echo "Make sure to start the server first"
    cd tests
    python getTests.py
    cd -
}

function help() {
    echo "Usage: ./run.sh {server|tests}"
}

# Run the target passed as the first arg on the command line
# If no first arg, run server
if [ $# -gt 1 ]; then help; exit; fi
if [ $# = 1 ]; then $1; else server; fi
