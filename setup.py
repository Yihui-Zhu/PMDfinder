from setuptools import setup, find_packages

classifier = [
    'Development Status :: 5 - Production/Stable',
    'Intended Autience :: Education',
    'Operating System :: macOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(name='PMDfinder',
      version='0.3.0',
      description='Identify partially methylation from methylome',
      url='https://github.com/Yihui-Zhu/PMDfinder',  
      author='Yihui Zhu',
      author_email='yhzhu@ucdavis.edu',
      license='MIT', 
      keywords='PMD', 
      packages=find_packages(),
      install_requires=[
          'pandas',
          'numpy',
          'sklearn',
          'tensorflow',
          'matplotlib'
      ])
