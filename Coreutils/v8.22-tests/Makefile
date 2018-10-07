VERSION=8.22
BINPATH=./coreutils_dir/coreutils-$(VERSION)/src

source:
	wget -c http://ftp.gnu.org/gnu/coreutils/coreutils-$(VERSION).tar.xz
	mkdir -p coreutils_dir
	tar -xf coreutils-$(VERSION).tar.xz -C coreutils_dir

build:
	cd ./coreutils_dir/coreutils-$(VERSION); \
	./configure; \
	make

# commit-id: https://github.com/coreutils/coreutils/commit/fb13cdc727541adef0010279f770f2afa358002e
record-shuf:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- $(BINPATH)/shuf -i 0-0 1
endif

# commit-id: https://github.com/coreutils/coreutils/commit/0093ac8d57a0f1a16fd09d98f6a524dddb6053e7
record-ln:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- $(BINPATH)/ln -sr '' F
endif

# commit-id: https://github.com/coreutils/coreutils/commit/a4faa6a0a3ae93c01d036d830ae7a21b74913baf
record-date:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- $(BINPATH)/date --date='TZ="""'
endif


clean:
	rm -rf ./coreutils_dir
	rm -rf ./coreutils-$(VERSION).tar.xz