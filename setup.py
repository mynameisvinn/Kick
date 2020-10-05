from setuptools import setup, find_packages
import os

setup(
   name='Kick',
   version='1.0',
   description='remote code execution with decorators',
   author='vincent tang',
   author_email='vin.tang@gmail.com',
   packages=find_packages(),
   include_package_data=True,
   zip_safe=False,
   data_files=[(os.path.expanduser('~'), ['Kick/kick.ini'])]  # installing data files (ie non python files) into home dir https://stackoverflow.com/questions/41328318/how-to-install-data-files-of-python-package-into-home-directory
)

# including data_files https://stackoverflow.com/questions/2026876/packaging-python-applications-with-configuration-files