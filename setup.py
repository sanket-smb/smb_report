# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in smb_report/__init__.py
from smb_report import __version__ as version

setup(
	name='smb_report',
	version=version,
	description='custom and edit existing report as per requirements',
	author='SMB',
	author_email='maheshwaribhavesh95863@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
