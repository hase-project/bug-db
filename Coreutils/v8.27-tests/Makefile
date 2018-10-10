VERSION=8.27
BINPATH=./coreutils_dir/coreutils-$(VERSION)/src

source:
	wget -c http://ftp.gnu.org/gnu/coreutils/coreutils-$(VERSION).tar.xz
	mkdir -p coreutils_dir
	tar -xf coreutils-$(VERSION).tar.xz -C coreutils_dir

build:
	cd ./coreutils_dir/coreutils-$(VERSION); \
	./configure; \
	make

# commit-id: https://github.com/coreutils/coreutils/commit/9287ef2b1707e2a222f8ae776ce3785abcb16fba
record-date:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	tz_long=$(printf '%2000s' | tr ' ' a); \
	sudo $(HASEBIN) record -- $(BINPATH)/date -d "TZ=\"${tz_long}0\" 2017"
endif

# commit-id: https://github.com/coreutils/coreutils/commit/cc19f63be3ad0f27c9ea7f223883b75917fda7fb
record-b2sum:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	echo "BLAKE2" > $(BINPATH)/foobar; \
	sudo $(HASEBIN) record -- $(BINPATH)/b2sum -c < $(BINPATH)/foobar; \
	rm -f $(BINPATH)/foobar
endif

clean:
	rm -rf ./coreutils_dir
	rm -rf ./coreutils-$(VERSION).tar.xz
