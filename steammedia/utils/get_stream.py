import requests
import urllib.parse


class CameraAPI:
    def __init__(self, api_host):
        self.api_host = api_host

    def get_stream_url(self, camera_id: str):
        params = urllib.parse.urlencode({
            'access_token': '18b10eb42b8f4e48a51eab1c44fd5259',
            'channo': camera_id,
            'agreementType': 'rtsp',
            'remoteId': '10001',
            'remoteName': 'guest',
            'remoteIP': '10.200.191.204',
            'quality': 'sd'  # id:480, sd:720, hd:1080, nd:原始流不转码
        })
        url = f'http://{self.api_host}/api/videoStream/getVideoStreamUrl?' + params
        res = requests.post(url)
        return res.json()  # code：返回状态码, msg：返回信息, data：流地址, cmd：接口地址


if __name__ == '__main__':
    api_host = '10.200.152.52:8182'
    camera_id = '44030566401310403472'

    api = CameraAPI(api_host)
    res = api.get_stream_url(camera_id)
    print(res)
