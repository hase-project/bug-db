# ticket: https://www.exploit-db.com/exploits/40697/
# This testcase doesn't produce coredump (through show abnormal message)

VERSION=1.4.4
PREFIX=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

source:
	wget http://memcached.org/files/old/memcached-$(VERSION).tar.gz
	wget https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-1.0.18.tar.gz
	mkdir -p memcached
	tar -zxf memcached-$(VERSION).tar.gz -C memcached
	tar -zxf libmemcached-1.0.18.tar.gz -C memcached

build:
	cd memcached/memcached-$(VERSION); \
	./configure; \
	make CFLAGS='-g -O2 -pthread -Wall -pedantic -Wmissing-prototypes -Wmissing-declarations -Wredundant-decls -fsanitize=address'
	cd memcached/libmemcached-1.0.18; \
	./configure; \
	make

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- ./memcached/memcached-$(VERSION)/memcached -u nobody -p 23001 -vv
endif

test:
	./memcached/libmemcached-1.0.18/clients/memrm --servers localhost:23001 --binary ABCDEF xyz
    
stop:
	# sudo kill $$(ps aux | grep '[n]ginx' | awk '{print $$2}')
	sudo killall -I memcached || true

clean:
	rm -rf ./memcached
	rm -rf ./memcached-$(VERSION).tar.gz
