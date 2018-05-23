import sys
import os
import subprocess

from .bug_list import submodule_list


def add_patch(path):
    patch_name = path.replace('/', '-')
    