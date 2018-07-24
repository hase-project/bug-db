# ticket: https://www.cvedetails.com/cve/CVE-2015-3416/

VERSION=3ad829e5

source: clean
	wget https://www.sqlite.org/src/tarball/$(VERSION)/SQLite-$(VERSION).tar.gz
	mkdir SQLite
	tar -zxf SQLite-$(VERSION).tar.gz -C SQLite

build:
	cd SQLite/SQLite-$(VERSION); \
	mkdir build; \
	cd build; \
	../configure; \
	make; \
	cp ../../../test_mprintf.c ./test_mprintf.c; \
	gcc -g test_mprintf.c sqlite3.o -o test_mprintf -ldl -lpthread

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record ./SQLite/SQLite-$(VERSION)/build/test_mprintf
endif

clean:
	rm -rf SQLite-$(VERSION).tar.gz
	rm -rf ./SQLite