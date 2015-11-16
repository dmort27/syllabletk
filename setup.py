from setuptools import setup

setup(name='syllabletk',
      version='0.0',
      description='Library for manipulating and analyzing syllables transcribed ' +
      'in Unicode IPA.',
      url='http://www.davidmortensen.org/syllabletk',
      author='David R. Mortensen',
      author_email='dmortens@cs.cmu.edu',
      license='MIT',
      install_requires=['setuptools',
                        'panphon',
                        'regex'],
      packages=['syllabletk'],
      zip_safe=True
      )
