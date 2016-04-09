from PIL import Image
import os
import PIL.ExifTags
import json

ROOT_DIR = 'images'
ORIGINALS_DIR = os.path.join(ROOT_DIR, 'originals')
THUMBNAILS_DIR = os.path.join(ROOT_DIR, 'thumbnails')
LARGE_IMAGES_DIR = os.path.join(ROOT_DIR, 'largeImages')

THUMBNAIL_SIZE = 375, 600
LARGE_IMAGE_SIZE = 1200, 1200

def initDirs():
  if not os.path.exists(THUMBNAILS_DIR):
    os.makedirs(THUMBNAILS_DIR)

  if not os.path.exists(LARGE_IMAGES_DIR):
    os.makedirs(LARGE_IMAGES_DIR)

def initAlbumDirs(album):
  targetThumbnailsDir = os.path.join(THUMBNAILS_DIR, album)
  if not os.path.exists(targetThumbnailsDir):
    os.makedirs(targetThumbnailsDir)

  targetLargeImagesDir = os.path.join(LARGE_IMAGES_DIR, album)
  if not os.path.exists(targetLargeImagesDir):
    os.makedirs(targetLargeImagesDir)

def resizeImage(img, album, name):
  thumbnail = img.copy()
  thumbnail.thumbnail(THUMBNAIL_SIZE)

  large = img.copy()
  large.thumbnail(LARGE_IMAGE_SIZE)

  targetThumbnail = os.path.join(THUMBNAILS_DIR, album, name)
  targetLarge = os.path.join(LARGE_IMAGES_DIR, album, name)

  thumbnail.save(targetThumbnail, 'JPEG')
  large.save(targetLarge, 'JPEG')

def main():

  initDirs()

  for root, dirs, files in os.walk(ORIGINALS_DIR):
    for name in files:
      albumName = root.split('\\')[-1]
      original = os.path.join(root, name)
      im = Image.open(original.replace('\\', '/'))

      exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in PIL.ExifTags.TAGS
      }

      caption = exif['ImageDescription']

      resizeImage(im, albumName, name)

    for name in dirs:
      initAlbumDirs(name)

if __name__ == '__main__':
  main()
