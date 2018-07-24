# ticket: https://www.sqlite.org/src/info/d02e1406a58ea02d

VERSION=62678be3

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