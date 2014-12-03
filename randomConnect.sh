#!/bin/bash
while true
do
	time=$(($RANDOM%98 + 1))
	sleep 0.$time
	wget -O - 10.0.0.100
done
