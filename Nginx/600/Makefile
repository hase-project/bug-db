# ticket: https://trac.nginx.org/nginx/ticket/600

VERSION=1.7.2
PREFIX=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

source:
	wget http://nginx.org/download/nginx-$(VERSION).tar.gz
	mkdir -p nginx
	tar -zxf nginx-$(VERSION).tar.gz -C nginx

build:
	mkdir -p logs
	cd nginx/nginx-$(VERSION); \
	./configure --prefix=$(PREFIX); \
	make

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- ./nginx/nginx-$(VERSION)/objs/nginx -c nginx.conf 
endif

test:
	curl -k localhost:80/index.html

stop:
	# sudo kill $$(ps aux | grep '[n]ginx' | awk '{print $$2}')
	sudo killall -I nginx || true

clean:
	rm -rf ./nginx
	rm -rf ./nginx-$(VERSION).tar.gz
	rm -rf ./logs
	sudo find . -name "*_temp" -type d -delete