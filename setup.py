import os
import io
import imp
from setuptools import find_packages, setup


VERSION = imp.load_source(
    'version', os.path.join('.', 'radiality', 'version.py')
).__version__

README = io.open('README.md', 'r', encoding='utf-8').read()

REQUIRES = [
    'websockets==3.2',
    'PyYAML==3.12'
]

setup(
    name='radiality',
    version=VERSION,
    description='Framework for microservices with reactive architecture.',
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='web framework api websocket microservice reactive architecture',
    author='Max Sukhorukov',
    author_email='signaldetect@gmail.com',
    url='https://github.com/signaldetect/radiality',
    license='Apache 2.0',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    setup_requires=[]
)
