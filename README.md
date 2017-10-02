# photo dedup

### A Photo Deduplication Tool

Ever wanted to clean up duplicate photos in your hard drive and folders? 

photodedup is a photo deduplication tool written in Python. 

### Features
* Uses EXIF meta data to determine duplicate photos
* List unique and duplicate photos
* Cross platform -- using python libraries only
* Builds a fileindex to speed up processing

## Install

```bash
pip install photodedup
```

## Usage

```
usage: photodedup.py [-h] [-u] [-c] image_path

photo deduplication tool

positional arguments:
  image_path       path to image folder

optional arguments:
  -h, --help       show this help message and exit
  -u, --unique     list unique images
  -c, --cache      find from cache instead of disk

```

## Examples

List duplicate photos

`photodedup.py  /path/to/photos`

List unique photos

`photodedup.py -u /path/to/photos`

By default, each time we will scan the source directory. If you want to use results from the previous scan, add -c to query from cache instead of disk

`photodedup.py -c  /path/to/photos`

`photodedup.py -uc /path/to/photos`
  

## Changelog
v0.2 - 2017-10-02

- Reimplement fileindex using sets
- Support only python 3 for now
- Remove -d flags, defaults lists duplicates
- Begin publishing packages to pypi

## TODO
- support python 2
