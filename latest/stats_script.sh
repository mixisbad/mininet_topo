#!/bin/bash

rm -f data.txt stats.csv
./get_stats.sh > data.txt
java StatParser
cat stats.csv
