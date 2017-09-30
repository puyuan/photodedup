import argparse
import logging

from photodedup.photodedup import PhotoDedup

logger = logging.getLogger()


def get_parser():
    parser = argparse.ArgumentParser(description='photo deduplication tool')

    parser.add_argument('-u', '--unique', help='list unique images',
                        action='store_true')
    parser.add_argument('-c', '--cache', help='find from cache instead of disk',
                        action='store_true')
    parser.add_argument('image_path', help="path to image folder")

    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    image_path = args['image_path']
    photoDedup = PhotoDedup(image_path)
    photoDedup.create_index()

    if not args["cache"]:
        photoDedup.scan_images()

    if args["unique"]:
        result = photoDedup.get_unique_images()
        photoDedup.print(result)
    else:
        result = photoDedup.get_duplicate_images()
        photoDedup.print(result)

if __name__ == "__main__":
    main()