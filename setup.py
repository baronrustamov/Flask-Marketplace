from setuptools import setup, find_packages
import os
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

BASE_PATH = os.path.dirname(__file__)

with open(os.path.join(BASE_PATH, 'Flask_Marketplace/__init__.py'), 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open(os.path.join(BASE_PATH, 'ReadMe.md'), "r") as fh:
    long_description = fh.read()


def get_requirements():
    with open(os.path.join(BASE_PATH, 'requirements.txt')) as f:
        rv = f.read().splitlines()
    return rv


setup(
    name='Flask-Marketplace',
    version=version,
    author='Ewetoye Ibrahim',
    author_email='i.ewetoye@gmail.com',
    description='A modular multivendor and multicurrency marketplace solution',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/EwetoyeIbrahim/Flask-Marketplace',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    classifiers=[
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
