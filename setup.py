
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='KillQuip',
    author='GoodMan',
    version='0.2.0',
    url='https://github.com/Sh4565/KillQuip',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'kill-quip=src.run:run',
            'kq=src.run:run',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Win',
    ],
    python_requires='>=3.11',
)
