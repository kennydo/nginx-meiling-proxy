from setuptools import setup


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
    packages=[
        'meiling',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
