'''setup for package'''

from setuptools import setup

with open('README.md') as h_md:
    LONG_DESCRIPTION = h_md.read()

with open('docs/changes.md') as h_md:
    BUF = h_md.read()

LONG_DESCRIPTION += BUF

DESCRIPTION = "Function Retry Decorator"

setup(
    name="retry",
    version="0.1.0",

    packages=['retry', ],

    # metadata for upload to PyPI
    author='byteskeptical',
    author_email='40208858+byteskeptical@users.noreply.github.com',
    description=DESCRIPTION,
    download_url='https://pypi.org/project/retry',
    license='BSD',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords='errors exceptions retry wrapper decorator',
    platforms=['any'],
    test_suite='tests.retry_tests',
    url='https://github.com/byteskeptical/retry',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities'
    ],
)
