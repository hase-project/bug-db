# README

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

5. (*) create patchs for code
```
cd util
python create_patch.py
cd ..
git add/commit/push
```
