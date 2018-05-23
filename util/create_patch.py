import subprocess
import os
import shutil

from bug_list import *


def add_patch(path):
    patch_path = "../patch/{}".format(path[2:].replace('/', '-'))
    diff = subprocess.Popen(
        ['git', 'diff'], 
        cwd="../{}".format(path),
        stdout=subprocess.PIPE
    )
    diff.wait()
    content = diff.stdout.read()
    if content:
        with open(patch_path, "w+") as f:
            f.write(content)
        with open("../patch.sh", "a+") as f:
            f.write("cd {}\n".format(path))
            f.write("git apply {}\n".format(abspath(patch_path)))
            f.write("cd -\n")


def rebuild_patch():
    shutil.rmtree("../patch")
    os.mkdir("../patch")
    open("../patch.sh", "w+").close()
    add_executable("../patch.sh")
    for lib, _, commits in submodule_list:
        for commit in commits:
            path = format_path(lib, commit)
            add_patch(path)

if __name__ == "__main__":
    rebuild_patch()