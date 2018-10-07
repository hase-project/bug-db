VERSION=6.10
BINPATH=./coreutils_dir/coreutils-$(VERSION)/src

source:
	wget -c http://ftp.gnu.org/gnu/coreutils/coreutils-$(VERSION).tar.gz
	mkdir -p coreutils_dir
	tar -zxf coreutils-$(VERSION).tar.gz -C coreutils_dir

build:
	cd ./coreutils_dir/coreutils-$(VERSION); \
	./configure; \
	make

# commit-id: https://github.com/coreutils/coreutils/commit/d701f6abb73e36721de5df083df4769786a14528
record-tac:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	echo > $(BINPATH)/foobar; \
	sudo $(HASEBIN) record -- $(BINPATH)/tac -r $(BINPATH)/foobar $(BINPATH)/foobar; \
	rm -f $(BINPATH)/foorbar
endif

# commit-id: https://github.com/coreutils/coreutils/commit/72d052896a9092b811961a8f3e6ca5d151a59be5
# commit-id: https://github.com/coreutils/coreutils/commit/eb8fa94f2cf030d625c12ad68bb8883de204c196
record-mkdir:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- $(BINPATH)/mkdir -Z invalid-selinux-context foobar
endif

# commit-id: https://github.com/coreutils/coreutils/commit/7cb24684cc4ef96bb25dfc1c819acfc3b98d9442
record-sha512sum:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	echo 'SHA512 (' > $(BINPATH)/foobar; \
	sudo $(HASEBIN) record -- $(BINPATH)/sha512sum -c < $(BINPATH)/foobar; \
	rm -f $(BINPATH)/foobar
endif

# commit-id: https://github.com/coreutils/coreutils/commit/a0851554bd52038ed47e46ee521ce74a5a09f747
record-ptx:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	echo > $(BINPATH)/A01234567890123456789012345678901234567890123456789; \
	sudo $(HASEBIN) record -- $(BINPATH)/ptx -F'\' $(BINPATH)/A01234567890123456789012345678901234567890123456789; \
	rm -f $(BINPATH)/A01234567890123456789012345678901234567890123456789
endif

# commit-id: https://github.com/coreutils/coreutils/commit/b58a8b4ef588ec8a365b920d12e27fdd71aa48d1
record-paste:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- $(BINPATH)/paste -d'\' 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
endif

# commid-id: https://github.com/coreutils/coreutils/commit/f926f7ce0e0a224ef3a37a82e60fd3d7aaca906e
record-stty:
ifndef HASEBIN
	echo "Please define hase binary path"
else
	sudo $(HASEBIN) record -- $(BINPATH)/stty eol -F /dev/tty
endif


clean:
	rm -rf ./coreutils_dir
	rm -rf ./coreutils-$(VERSION).tar.gz