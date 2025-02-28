#!/bin/bash

# Save the keys in GOOGLE_API_KEYS variable
API_KEYS=$GOOGLE_API_KEYS

if [[ -z $API_KEYS ]]; then
    echo "No Keys Provided"
    exit 1
fi

count=1
for key in ${API_KEYS[@]}; 
do
    echo "Executing scraper with API KEY $count"
    export GOOGLE_BOOKS_API_KEY=$key
    python3 scrape_summaries.py
    ((count++))
done
