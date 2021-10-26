# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from distutils.core import setup
setup(
    name='ganjoor-api-wrapper',
    packages=['ganjoor'],
    version='0.1.2',
    license='MIT',
    description='Ganjoor API wrapper in python',
    author='Mohammad Kazemi',
    author_email='kazemi.me.222@gmail.com',
    url='https://github.com/MmeK/ganjoor_api_wrapper',
    download_url='https://github.com/MmeK/ganjoor_api_wrapper/archive/refs/tags/v0.1.2-alpha.tar.gz',
    keywords=['Ganjoor', 'API', 'API-wrapper', 'Poetry', 'Persian', 'Farsi'],
    install_requires=[            # I get to this in a second
        'inflection',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
