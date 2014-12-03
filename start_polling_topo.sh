sudo mn --controller=remote,ip=127.0.0.1,port=6633 --link tc,bw=5 --mac --custom ./test_polling_topo.py --topo mytopo --switch ovsk

