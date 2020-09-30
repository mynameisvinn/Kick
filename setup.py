from setuptools import setup, find_packages

setup(
   name='Kick',
   version='1.0',
   description='remote code execution with a single decorator',
   author='vincent tang',
   author_email='vin.tang@gmail.com',
   packages=find_packages(),
   zip_safe=False
)