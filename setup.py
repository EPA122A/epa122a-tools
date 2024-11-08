from setuptools import setup, find_packages

setup(
    name='epa122a_tools',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='A simple data downloader package for EPA122A',
    author='Giacomo Marangoni',
    author_email='G.Marangoni@tudelft.nl',
    url='https://github.com/EPA122A/epa122a-tools',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
