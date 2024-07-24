#!/bin/bash

TOPIC="test/payload"
BROKER="localhost"
MAX_SIZE=256000000 

size=120000
while [ $size -le $MAX_SIZE ]; do
    payload=$(head -c $size </dev/urandom | base64 | head -c $size)
    echo "Sending payload of size: $size"
    mosquitto_pub -t $TOPIC -m "$payload" -h $BROKER
    #sleep 1
    size=$(( size + 1 ))
done
