from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pycsvw',
      version='0.1',
      description='Python implementation of CSV on the Web',
      long_description=readme(),
      url='https://github.com/Aleksander-Drozd/pycsvw',
	  download_url='https://github.com/Aleksander-Drozd/pycsvw/archive/0.1.tar.gz',
      author='Aleksander Drozd',
      author_email='aleksander.drozd@outlook.com',
      license='MIT',
      packages=['pycsvw.converter', 'pycsvw.utils', 'pycsvw.utils.json', 'pycsvw.utils.rdf',
                'pycsvw.utils.url'],
      install_requires=[
          'python-dateutil==2.6.1',
          'rdflib==4.2.2',
          'rdflib-jsonld==0.4.0',
          'requests==2.18.4',
          'uritemplate==3.0.0',
      ],
      zip_safe=False)
