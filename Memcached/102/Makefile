# ticket: https://code.google.com/archive/p/memcached/issues/102

VERSION=1.2.8
PREFIX=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

source:
	wget https://launchpad.net/memcached/1.2/1.2.8/+download/memcached-1.2.8.tar.gz
	mkdir -p memcached
	tar -zxf memcached-$(VERSION).tar.gz -C memcached

build:
	cd memcached/memcached-$(VERSION); \
	./configure; \
	sed -i 's/\#include <limits.h>/#include <limits.h>\n\#define IOV_MAX 1024/g' memcached.c; \
	make

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- ./memcached/memcached-$(VERSION)/memcached -u nobody
endif

test:
	cat /dev/zero | nc -q1 127.0.0.1 11211

stop:
	# sudo kill $$(ps aux | grep '[n]ginx' | awk '{print $$2}')
	sudo killall -I memcached || true

clean:
	rm -rf ./memcached
	rm -rf ./memcached-$(VERSION).tar.gz
