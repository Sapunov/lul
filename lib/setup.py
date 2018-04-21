from __future__ import unicode_literals

from setuptools import find_packages, setup


if __name__ == '__main__':

    with open('README') as readme:
        setup(
            name='logulife',
            version='0.0.1',

            description=readme.readline().strip(),
            long_description=readme.read().strip() or None,
            url='',

            license='GPL3',
            author='Nikita Sapunov',
            author_email='kiton1994@gmail.com',

            classifiers=[
                'Intended Audience :: Everybody',
                'Operating System :: MacOS :: MacOS X',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Programming Language :: Python :: 3'
            ],
            platforms=['unix', 'linux', 'osx', 'windows'],

            install_requires=['requests'],

            packages=find_packages(),
        )
