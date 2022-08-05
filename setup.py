#!/usr/bin/env python3
from setuptools import setup, find_packages


def main():
    setup(
        name = 'ssdecoder',
        version = '1.0.0',
        url = 'https://github.com/liu-congcong/ssdecoder/',
        author = 'Liucongcong',
        author_email = 'congcong_liu@icloud.com',
        license = 'MIT',
        description = 'SS or SSR string decoder.',
        scripts = ['bin/ssdecoder',],
        packages = find_packages(),
        package_data = {'': ['LICENSE',]}
    )


if __name__ == '__main__':
    main()
