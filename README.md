#photodedup 

## A Photo Deduplication Tool

Ever wanted to clean up duplicate photos in your hard drive and folders? 

photodedup is a photo deduplication tool written in Python. 

### Features
* Uses EXIF meta data to determine duplicate photos
* List unique and duplicate photos
* Cross platform -- using python libraries only
* Builds a local cache to speed up processing

## Usage
List duplicate photos

`photodedup -d /path/to/photos`

List unique photos

`photodedup -u /path/to/photos`

Add -c to query from cache instead of disk

`photodedup -dc  /path/to/photos`
  


