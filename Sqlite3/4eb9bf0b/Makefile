# ticket: https://www.sqlite.org/src/info/78e04e52eaf

VERSION=4eb9bf0b

source: clean
	wget https://www.sqlite.org/src/tarball/$(VERSION)/SQLite-$(VERSION).tar.gz
	mkdir SQLite
	tar -zxf SQLite-$(VERSION).tar.gz -C SQLite

build:
	cd SQLite/SQLite-$(VERSION); \
	chmod +x ./configure; \
	mkdir build; \
	cd build; \
	../configure; \
	make; \
	cp ../src/shell.c ./; \
	gcc -pthread -DSQLITE_DEBUG -o sqlite3 sqlite3.c shell.c -ldl

record:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record ./SQLite/SQLite-$(VERSION)/build/sqlite3 < ./stdin
endif

clean:
	rm -rf SQLite-$(VERSION).tar.gz
	rm -rf ./SQLite