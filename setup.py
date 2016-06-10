import os

from setuptools import setup

import polypie


os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='polypie',
    version=polypie.__version__,
    py_modules=['polypie'],
    install_requires=['typecheck-decorator>=1.3'],
    license='BSD License',
    description='Python polymorphic function declaration with obvious syntax',
    long_description=long_description,
    url='https://github.com/un-def/polypie',
    author='un.def',
    author_email='un.def@ya.ru',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
