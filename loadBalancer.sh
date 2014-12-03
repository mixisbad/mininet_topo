#!/bin/sh

curl -X POST -d '{"id":"1","name":"vip1","protocol":"tcp","address":"10.0.0.100","port":"80"}' http://localhost:8080/quantum/v1.0/vips/
curl -X POST -d '{"id":"1","name":"pool1","protocol":"tcp","vip_id":"1"}' http://localhost:8080/quantum/v1.0/pools/
curl -X POST -d '{"id":"1","address":"10.0.0.1","port":"80","pool_id":"1"}' http://localhost:8080/quantum/v1.0/members/
curl -X POST -d '{"id":"2","address":"10.0.0.2","port":"80","pool_id":"1"}' http://localhost:8080/quantum/v1.0/members/
curl -X POST -d '{"id":"3","address":"10.0.0.3","port":"80","pool_id":"1"}' http://localhost:8080/quantum/v1.0/members/
