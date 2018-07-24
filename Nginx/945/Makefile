# ticket: https://trac.nginx.org/nginx/ticket/945

VERSION=1.9.13
PREFIX=$(dir $(realpath $(lastword $(MAKEFILE_LIST))))

source: clean
	wget http://nginx.org/download//nginx-$(VERSION).tar.gz
	mkdir -p nginx
	tar -zxf nginx-$(VERSION).tar.gz -C nginx

build:
	mkdir -p logs
	cd nginx/nginx-$(VERSION); \
	./configure --prefix=$(PREFIX) --with-http_ssl_module; \
	make

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- ./nginx/nginx-$(VERSION)/objs/nginx -c nginx.conf &
endif

# better collect pid
test_%:
	watch -n 0.1 'kill -HUP $*'

stop:
	# sudo kill $$(ps aux | grep '[n]ginx' | awk '{print $$2}')
	sudo killall -I nginx || true

clean:
	rm -rf ./nginx
	rm -rf ./nginx-$(VERSION).tar.gz
	rm -rf ./logs
	sudo find . -name "*_temp" -type d -delete