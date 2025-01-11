from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='unireo',
      version='0.1.2',
      description='A universal SDK for synchronized dual-eye cameras compliant with the UVC protocol',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Anawaert',
      author_email='anawaertstudio@outlook.com',
      url='https://github.com/Anawaert/unireo',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ]
)