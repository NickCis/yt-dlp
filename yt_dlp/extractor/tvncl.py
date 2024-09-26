# https://live.tvn.cl/
from .common import InfoExtractor
from ..utils import js_to_json
from urllib.parse import urlencode


class TVNClIE(InfoExtractor):
    _VALID_URL = r'https?://live\.tvn\.cl'

    def _real_extract(self, url):
        display_id = 'live-tvn-cl'
        webpage = self._download_webpage(url, display_id)

        params = self._search_json(r'var\s+params\s*=', webpage, 'params', display_id, transform_source=js_to_json)
        query = urlencode({
            'jsapi': 'true',
            'loop': 'false',
            'autoplay': params['autoplay'],
            'volume': '0',
            'player': params['player'],
            'access_token': params['access_token'],
        })

        return self.url_result(
            f'https://mdstrm.com/live-stream/{params["id"]}?{query}',
            display_id=display_id, url_transparent=True)
