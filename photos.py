from PIL import Image
import os
import PIL.ExifTags
import json
import datetime

ROOT_DIR = 'images_test'
ORIGINALS_DIR = os.path.join(ROOT_DIR, 'originals')
THUMBNAILS_DIR = os.path.join(ROOT_DIR, 'thumbnails')
LARGE_IMAGES_DIR = os.path.join(ROOT_DIR, 'largeImages')

THUMBNAIL_SIZE = 375, 600
LARGE_IMAGE_SIZE = 1200, 1200

# MONTH_DIC = {'January': 01, 'Feburary': 02, 'March': 03, 'April': 04, 'May': 05, 'June', }

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

  # thumbnail.save(targetThumbnail, 'JPEG')
  # large.save(targetLarge, 'JPEG')

def main():

  initDirs()

  albumsData = {}
  albumsData['albums'] = []

  for root, dirs, files in os.walk(ORIGINALS_DIR):
    for name in files:
      if not name.startswith('.') and os.path.isfile(os.path.join(root, name)):
        albumID = root.split('/')[-1]
        original = os.path.join(root, name)
        im = Image.open(original)

        # get exif info
        exif = {
          PIL.ExifTags.TAGS[k]: v
          for k, v in im._getexif().items()
          if k in PIL.ExifTags.TAGS
        }

        try:
          caption = exif['ImageDescription']
        except KeyError:
          print('No ImageDescription Available for', name )
          caption = ''

        # resizeImage(im, albumID, name)

        thumbnail = im.copy()
        thumbnail.thumbnail(THUMBNAIL_SIZE)

        large = im.copy()
        large.thumbnail(LARGE_IMAGE_SIZE)

        targetThumbnail = os.path.join(THUMBNAILS_DIR, albumID, name)
        targetLarge = os.path.join(LARGE_IMAGES_DIR, albumID, name)
        thumbnail.save(targetThumbnail, 'JPEG')
        large.save(targetLarge, 'JPEG')

        # print(large.size)

        photoData = {}
        photoData['caption'] = caption
        photoData['src'] = targetLarge
        photoData['width'] = large.size[0]
        photoData['height'] = large.size[1]

        thumbnailData = {}
        thumbnailData['src'] = targetThumbnail
        thumbnailData['width'] = thumbnail.size[0]
        thumbnailData['height'] = thumbnail.size[1]

        photoData['thumbnail'] = thumbnailData

        # print(photoData)
        for album in albumsData['albums']:
          if album['albumID'] == albumID:
            album['photos'].append(photoData)
        # my_list = filter(lambda x: x.attribute == value, albumsData['albums'])

    for name in dirs:
      initAlbumDirs(name)

      albumData = {}
      arr = name.split('_')

      dt = datetime.datetime.strptime(''.join(arr[-2:]), '%B%Y')
      # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()

      # print(timestamp)
      albumData['albumName'] = ' '.join(arr[:-2])
      albumData['timeStamp'] = str(dt)
      albumData['albumID'] = name
      albumData['date'] = ', '.join(arr[-2:])
      albumData['photos'] = []
      albumsData['albums'].append(albumData)

  # print(json.dumps(albumsData))

  with open('images_test/data.json', 'w') as outfile:
    json.dump(albumsData, outfile)

if __name__ == '__main__':
  main()
