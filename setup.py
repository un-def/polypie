import os
import re

from setuptools import setup


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


with open('README.rst') as f:
    long_description = f.read()

with open('polypie.py') as f:
    author, author_email, version = re.search(
        "__author__ = '(.+) <(.+)>'.+__version__ = '([.0-9]+)'",
        f.read(),
        flags=re.DOTALL
    ).groups()


setup(
    name='polypie',
    version=version,
    py_modules=['polypie'],
    install_requires=['typecheck-decorator>=1.3'],
    test_suite='test_polypie.py',
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
