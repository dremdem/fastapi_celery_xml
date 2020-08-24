#!/bin/bash

#docker-compose build
#docker-compose up -d

# set -x

JSON_HEAD='content-type: application/json'

BASEURL='http://127.0.0.1:8000'
URLS="$BASEURL/urls"
KEYS="$BASEURL/keys"

FILENAME_RANGE=$(seq 1 2)

ATTEMPT_TIMEOUT_SEC=1
MAX_ATTEMPTS=5

# In general, IDS is not subset of FILENAME_RANGE
for i in $FILENAME_RANGE; do
    IDS[$i]=$(curl -X POST -H '$JSON_HEAD' $URLS \
        -d '{
            "url": "https://hub.b2basket.ru/media/test_problem/file_'$i'.xml"
        }' | jq '.id')
done

ATTEMPT=0

while [[ "$READY" != 'true' ]]; do
    ATTEMPT=$((ATTEMPT+1))

    if [[ $ATTEMPT > $MAX_ATTEMPTS ]]; then
        echo "\e[0;31mToo many attempts!\e[m"
        curl -H '$JSON_HEAD' $URLS
        exit
    fi

    READY='true'

    for i in ${IDS[@]}; do
        PROCESSED=$(curl -H '$JSON_HEAD' "$URLS/$i" | jq '.processed')

        if [[ "$PROCESSED" != 'true' ]]; then
            READY='false'
            sleep $ATTEMPT_TIMEOUT_SEC
            break
        fi
    done
done

curl -H '$JSON_HEAD' $KEYS
