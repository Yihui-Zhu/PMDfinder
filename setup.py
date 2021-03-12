from setuptools import setup, find_packages

classifier = [
    'Development Status :: 5 - Production/Stable',
    'Intended Autience :: Education',
    'Operating System :: macOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
  name='PMDfinder',
  version='0.0.1',
  description='Identify partially methylation from methylome',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Yihui Zhu',
  author_email='yhzhu@ucdavis.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='PMD', 
  packages=find_packages(),
  install_requires=[
      'pandas',
      'numpy',
      'random',
      'scikit-learn',
      'tensorflow',
      'matplotlib'
  ] 
)