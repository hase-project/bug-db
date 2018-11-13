# README

## bugdb

Build first without root:

```console
$ ./bin/bugdb-record --build-only
```

Then as root run

```console
$ ./bin/bugdb-record
```

## Comparison with klee

1. clone libs and apply patch
```
cd util
python create_lib.py
cd ..
./setup.sh
./checkout.sh
./patch.sh
```

2. modify libs to support KLEE execution (maybe not)

3. build bytecode(?)

4. use KLEE(?) to get error testcase and parse

5. use hase to replay the testcase

6. (*) create patchs for modified lib
```
cd util
python create_patch.py
cd ..
git add/commit/push
```

## raise-added coreutils
```
./setup_coreutils.sh
cd util
python test_coreutils.py [target]
```

prereq libraries: Autoconf, Automake, Bison, Gettext, Git, Gperf, Gzip, Perl, RSync, Tar, TexInfo

## sqlite3/nginx/memcached bugs
```
make source
make build
make record
# if needed
make test
```
