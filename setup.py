from setuptools import setup, find_packages

setup(
    name='photodedup',
    version='0.2',
    description='A simple photo deduplicator tool written in Python',
    author='Paul Yuan',
    author_email='puyuan1@gmail.com',
    url='https://github.com/puyuan',
    install_requires=['markdown'],
    entry_points={'console_scripts' : ['photodedup=photodedup:main']},
    packages=find_packages()
)