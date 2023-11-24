# https://github.com/yt-dlp/yt-dlp/pull/7151/files

from .common import InfoExtractor
from ..utils import js_to_json, ExtractorError
from urllib.parse import urlencode


class MegaClIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mega\.cl/senal-en-vivo'

    def _real_extract(self, url):
        display_id = 'mega-cl-vivo'
        webpage = self._download_webpage(url, display_id)

        video = self._search_json(r'var\s+video\s*=', webpage, 'videodata', display_id, end_pattern=';var', transform_source=js_to_json)
        accesstoken_query = {
            'id': video['id'],
            'ua': self._downloader.params.get('http_headers').get('User-Agent'),
            'type': video['type'],
            'process': 'access_token',
            'key': video['serverKey'],
        }
        accesstoken_webpage = self._download_webpage('https://api.mega.cl/api/v1/mdstrm', display_id, headers={'Origin': 'https://www.mega.cl'}, query=accesstoken_query)

        if accesstoken_webpage == "false":
            raise ExtractorError('Couldnt get access token', video_id=display_id)

        accesstoken = self._parse_json(accesstoken_webpage, display_id)
        params = urlencode({
            'jsapi': 'true',
            'loop': video['loop'],
            'autoplay': video['autoplay'],
            'volume': '0',
            'player': video['player'],
            'access_token': accesstoken['access_token'],
        })

        return self.url_result(
            f'https://mdstrm.com/live-stream/{video["id"]}?{params}',
            display_id=display_id, url_transparent=True)
