import os
import re

from setuptools import setup


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


with open('README.rst') as f:
    long_description = f.read()

with open('polypie.py') as f:
    author, author_email, version = re.search(
        "__author__ = '(.+) <(.+)>'.+__version__ = '([.0-9a-z]+)'",
        f.read(),
        flags=re.DOTALL
    ).groups()


setup(
    name='polypie',
    version=version,
    py_modules=['polypie'],
    install_requires=['typeguard'],
    python_requires='>=3.5',
    license='BSD License',
    description='Python polymorphic function declaration with obvious syntax',
    long_description=long_description,
    url='https://github.com/un-def/polypie',
    author=author,
    author_email=author_email,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
