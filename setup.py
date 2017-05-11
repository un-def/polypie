from pathlib import Path
import re
from sys import version_info

from setuptools import setup


PROJECT_DIR = Path(__file__).parent.resolve()


if version_info < (3, 4):
    raise RuntimeError("Requires Python 3.4 or later.")

with open(str(PROJECT_DIR / 'README.rst')) as f:
    long_description = f.read()

with open(str(PROJECT_DIR / 'polypie.py')) as f:
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
    description='Python declarations of polymorphic function with an obvious '
                'syntax.',
    long_description=long_description,
    url='https://github.com/un-def/polypie',
    author=author,
    author_email=author_email,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
