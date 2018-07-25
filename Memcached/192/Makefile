# ticket: https://code.google.com/archive/p/memcached/issues/192

VERSION=1.4.13
PREFIX=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

source:
	wget http://memcached.org/files/old/memcached-$(VERSION).tar.gz
	mkdir -p memcached
	tar -zxf memcached-$(VERSION).tar.gz -C memcached

build:
	cd memcached/memcached-$(VERSION); \
	./configure; \
	make

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- ./memcached/memcached-$(VERSION)/memcached -u nobody -p 23000
endif

test:
	echo -en '\x80\x12\x00\x01\x08\x00\x00\x00\xff\xff\xff\xe8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' | nc localhost 23000
    
stop:
	# sudo kill $$(ps aux | grep '[n]ginx' | awk '{print $$2}')
	sudo killall -I memcached || true

clean:
	rm -rf ./memcached
	rm -rf ./memcached-$(VERSION).tar.gz
