import io
import os
import re
from os import path

from setuptools import find_packages, setup


try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements


PROJECT_ROOT = path.abspath(path.dirname(__file__))


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


def read_requirements(path):
    """Read a requirements file."""
    reqs = parse_requirements(path, session=False)
    return [str(ir.req) for ir in reqs]


# hardcoded
required = read_requirements(path.join(PROJECT_ROOT, "requirements.txt"))


setup(
    name="shoml",
    version="0.1.0",
    url="https://github.com/shoarora/shoml",
    license='MIT',

    author="Sho Arora",
    author_email="sho854@gmail.com",

    description="shoml - assorted personal ML-related utilities",
    long_description=read("README.md"),

    packages=find_packages(exclude=('tests',)),
    python_requires='>=3.6',
    install_requires=required,
    extras_require={
        ':python_version == "3.6"': ['dataclasses==0.7'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
