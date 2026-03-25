import os
import ssl
import urllib.request
from TiktokDownloader import TiktokDownloader
ssl._create_default_https_context = ssl._create_unverified_context

X_API_KEY = 'YOUR_API_KEY' # Your API key used to authenticate requests to the Tikfly API. Get it from the official docs: https://docs.tikfly.io/getting-started/quickstart
UNIQUE_ID = 'taylorswift' # Tiktok username of the target account
MAXIMUM_NUM_OF_VIDEOS = 100 # The maximum number of videos to download

def tiktok_bulk_download():
  print(f'🏁 Start downloading {MAXIMUM_NUM_OF_VIDEOS} videos of {UNIQUE_ID}...')

  tiktok = TiktokDownloader(X_API_KEY)

  user_sec_uid = tiktok.get_user_sec_uid(UNIQUE_ID)
  if not user_sec_uid:
    print(f'🚨 User {UNIQUE_ID} not found')
    return
  
  print(f'⚡️ User secUid: {user_sec_uid}')

  min_cursor = 0
  max_cursor = 0
  count = 0
  
  while count < MAXIMUM_NUM_OF_VIDEOS:
    res = tiktok.download_user_videos(user_sec_uid, min_cursor, max_cursor)
    if not res:
      print('🐞 Something went wrong. Please try again')
      break

    videos = res.get('itemList')
    min_cursor = res.get('minCursor')
    max_cursor = res.get('maxCursor')

    if not videos or len(videos) == 0:
      print('🚨 No more videos to download')
      break

    os.makedirs(f'data/{UNIQUE_ID}', exist_ok=True) 
    for video in videos:
      video_id = video.get('id')
      download_url = video.get('play')
      image_urls = video.get('images')

      if not video_id:
        continue
      
      if download_url:
        print(f'📥 [{count}] Downloading video {video_id}...')
        urllib.request.urlretrieve(download_url, f'data/{UNIQUE_ID}/{video_id}.mp4')
        count += 1
      elif image_urls and len(image_urls) > 0:
        for idx, img_url in enumerate(image_urls, start=1):
          print(f'📥 [{count}] Downloading slideshow video {video_id}_{idx}')
          file_path = f'data/{UNIQUE_ID}/{video_id}_{idx}.png'
          urllib.request.urlretrieve(img_url, file_path)
        count += 1

  print('✅ Done')

tiktok_bulk_download()
