from setuptools import (
    find_packages,
    setup,
)


setup(
    name='meiling',
    version='0.0.1',
    description="Authenticate nginx requests through OAuth",
    url='https://github.com/kennydo/nginx-meiling-proxy',
    author='Kenny Do',
    author_email='chinesedewey@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
    ],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
        ],
    },
)
