#photodedup 

### A Photo Deduplication Tool

Ever wanted to clean up duplicate photos in your hard drive and folders? 

photodedup is a photo deduplication tool written in Python. 

### Features
* Uses EXIF meta data to determine duplicate photos
* List unique and duplicate photos
* Cross platform -- using python libraries only
* Builds a local cache to speed up processing

## Usage

```
usage: photodedup.py [-h] [-d] [-u] [-c] image_path

photo deduplication tool

positional arguments:
  image_path       path to image folder

optional arguments:
  -h, --help       show this help message and exit
  -d, --duplicate  list duplicate images
  -u, --unique     list unique images
  -c, --cache      find from cache instead of disk

```

## Examples

List duplicate photos

`photodedup.py -d /path/to/photos`

List unique photos

`photodedup.py -u /path/to/photos`

Add -c to query from cache instead of disk

`photodedup.py -dc  /path/to/photos`

`photodedup.py -uc /path/to/photos`
  


