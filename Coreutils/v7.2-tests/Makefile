VERSION=7.2
BINPATH=./coreutils_dir/coreutils-$(VERSION)/src

source:
	wget -c http://ftp.gnu.org/gnu/coreutils/coreutils-$(VERSION).tar.xz
	mkdir -p coreutils_dir
	tar -xf coreutils-$(VERSION).tar.xz -C coreutils_dir

build:
	cd ./coreutils_dir/coreutils-$(VERSION); \
	./configure; \
	make

# commit-id: https://github.com/coreutils/coreutils/commit/25eb4c69097ca4f5665b050cfa4247a19ffd8c55
record-sort:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	touch $(BINPATH)/foobar; \
	sudo $(HASEBIN) record -- $(BINPATH)/sort -m -o $(BINPATH)/foobar $(BINPATH)/foobar; \
	rm -f $(BINPATH)/foobar
endif


clean:
	rm -rf ./coreutils_dir
	rm -rf ./coreutils-$(VERSION).tar.xz