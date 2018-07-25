# ticket: https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=2824

VERSION=7e0d3e9c

source: clean
	wget https://www.sqlite.org/src/tarball/$(VERSION)/SQLite-$(VERSION).tar.gz
	mkdir SQLite
	tar -zxf SQLite-$(VERSION).tar.gz -C SQLite

build:
	cd SQLite/SQLite-$(VERSION); \
	mkdir build; \
	cd build; \
	../configure; \
	make CFLAGS='-g -O2 -DSQLITE_OS_UNIX=1 -DSQLITE_DEBUG=1'

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record ./SQLite/SQLite-$(VERSION)/build/sqlite3 < ./stdin
endif

clean:
	rm -rf SQLite-$(VERSION).tar.gz
	rm -rf ./SQLite