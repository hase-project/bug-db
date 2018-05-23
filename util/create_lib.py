import sys
import os
import stat

from .bug_list import submodule_list


def add_executable(path):
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)


def add_submodule(path, url, commit_id):
    with open("../setup.sh", "a+") as f:
        f.write("git submodule add -f {} {}\n".format(url, path))
        # FIXME: in case that git may have index.lock error
        f.write("sleep 0.1\n")
    with open("../checkout.sh", "a+") as f:
        f.write("cd ./{}\n".format(path))
        f.write("git checkout {}\n".format(commit_id))
        f.write("cd -\n")


def rebuild_submodule():
    with open("../setup.sh", "w+") as f:
        f.write("rm -rf .git\n")
        f.write("rm -rf lib\n")
        f.write("git init\n")
    open("../checkout.sh", "w+").close()
    add_executable("setup.sh")
    add_executable("checkout.sh")
    for lib, url, commits in submodule_list:
        for commit in commits:
            path = "lib/{}/{}".format(lib, commit)
            add_submodule(path, url, commit)

if __name__ == "__main__":
    rebuild_submodule()

