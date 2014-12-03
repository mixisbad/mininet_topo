#!/bin/bash
time=$(($RANDOM%39901 + 100))
sleep $(($time/1000)).$(($time%1000))
wget -b -O /dev/null -o /dev/null 10.255.0.100
