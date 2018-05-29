import os
import os.path
import sys
import shutil

# gnulib commit id: https://github.com/coreutils/gnulib/commit/81acba941a158525a3a8b976cb74e59c8cde1b74


def collect_coreutil():
    try:
        os.mkdir('../bin')
    except:
        pass
    try:
        os.mkdir('../tests')
    except:
        pass
    sign = "raise(SIGQUIT);"
    path_to_coreutil_src = "../lib/coreutils/src"
    for name in os.listdir(path_to_coreutil_src):
        if name.endswith('.c'):
            with open(path_to_coreutil_src + "/{}".format(name)) as f:
                s = f.read()
                if sign in s:
                    print(name[:-2])
                    try:
                        shutil.copy(
                            path_to_coreutil_src + "/{}".format(name[:-2]), 
                            "../bin")
                    except:
                        pass
                    open("../tests/{}.test".format(name[:-2]), "a+").close()
                    open("../tests/{}.stdin".format(name[:-2]), "a+").close()

if __name__ == "__main__":
    collect_coreutil()