from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='csvwlib',
      version='0.2.2',
      description='Python implementation of CSV on the Web',
      long_description=readme(),
      url='https://github.com/Aleksander-Drozd/csvwlib',
      download_url='https://github.com/Aleksander-Drozd/csvwlib/archive/0.1.tar.gz',
      author='Aleksander Drozd',
      author_email='aleksander.drozd@outlook.com',
      license='MIT',
	  packages=['csvwlib', 'csvwlib.converter', 'csvwlib.utils', 'csvwlib.utils.rdf', 'csvwlib.utils.url', 'csvwlib.utils.json'],
      install_requires=[
          'python-dateutil==2.6.1',
          'rdflib==4.2.2',
          'rdflib-jsonld==0.4.0',
          'requests==2.18.4',
          'uritemplate==3.0.0',
      ],
      zip_safe=False)
