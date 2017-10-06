from setuptools import setup, find_packages

setup(
    name='photodedup',
    version='0.2.1',
    description='A simple photo deduplication tool written in Python',
    author='Paul Yuan',
    author_email='puyuan1@gmail.com',
    url='https://github.com/puyuan/photodedup',
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    install_requires=['exifread'],
    keywords="photo dedup deduplication duplicate exif",
    entry_points={'console_scripts' : ['photodedup=photodedup:main']},
    packages=find_packages()
)
