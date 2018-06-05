git submodule add -f https://github.com/coreutils/coreutils lib/coreutils
sleep 0.1
cd lib/coreutils
./bootstrap
./configure --quiet
sed -i 's/man\/false.1//g' ./Makefile
sed -i 's/man\/true.1//g' ./Makefile
sed -i 's/-O2//g' ./Makefile
git apply ../../patch/coreutils_raise.patch
make
cd ../../util
python collect_coreutils.py
