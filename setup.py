from setuptools import find_packages, setup

setup(
    name='bugdb',
    version='0.1',
    description="Reproduce/Record bugs for hase",
    packages=find_packages(),
    install_requires=['hase'],
    entry_points={
        "console_scripts": ["bugdb-record = bugdb:main"],
    }
)
