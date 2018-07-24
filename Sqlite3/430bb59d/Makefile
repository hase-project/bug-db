# ticket: https://www.sqlite.org/src/info/c2ad16f997ee9c8e

VERSION=430bb59d

source: clean
	wget https://www.sqlite.org/src/tarball/$(VERSION)/SQLite-$(VERSION).tar.gz
	mkdir SQLite
	tar -zxf SQLite-$(VERSION).tar.gz -C SQLite

build:
	cd SQLite/SQLite-$(VERSION); \
	mkdir build; \
	cd build; \
	../configure; \
	make

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record ./SQLite/SQLite-$(VERSION)/build/sqlite3 < ./stdin
endif

clean:
	rm -rf SQLite-$(VERSION).tar.gz
	rm -rf ./SQLite