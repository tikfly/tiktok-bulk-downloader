import requests

class TiktokDownloader():
  def __init__(self, x_api_key: str):
    self.tiktok_api_url = 'https://tiktok-api23.p.rapidapi.com'
    self.headers = {
      'x-rapidapi-host': 'tiktok-api23.p.rapidapi.com',
      'x-rapidapi-key': x_api_key
    }

  def request(self, url: str, params: dict):
    try:
      res = requests.get(
        url,
        params=params,
        headers=self.headers
      )
      res.raise_for_status()
      data = res.json()

      return data
    except Exception as err:
      print(err)
      return None
    
  def get_user_sec_uid(self, unique_id: str):
    url = f'{self.tiktok_api_url}/api/user/info'
    params = {
      'uniqueId': unique_id
    }

    data = self.request(url, params)

    if not data:
      return None
    
    user_sec_uid = data.get('userInfo', {}).get('user', {}).get('secUid')

    return user_sec_uid

  def download_user_videos(
    self,
    user_sec_uid: str,
    min_cursor: int = 0,
    max_cursor: int = 0
  ):
    url = f'{self.tiktok_api_url}/api/download/user/video'
    params = {
      'secUid': user_sec_uid,
      'minCursor': min_cursor,
      'maxCursor': max_cursor
    }

    data = self.request(url, params)

    return data
    