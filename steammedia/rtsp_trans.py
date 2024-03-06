#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from utils.get_stream import CameraAPI
from utils.stream_io import push_rtsp_stream


if __name__ == "__main__":
    api_host = '10.200.152.52:8182'

    camera_ids = [
        '44030566401310403472',
        '44030599001320590203',
        '44030599001326008186',
        '44030599001326008152',
        '44030500001310093828',
        '44030500001310007305',
        '44030500001310915414',
        '44030551001320002030',
        '44030599001310121009',
        '44030599001321870001',
        '44030599001310121004',
        '44030599001320056384',
        '44030557001310002007',
        '44030599001310921555',
        '44030599001320245245',
        '44030599001320201381'
    ]

    api = CameraAPI(api_host)

    source = []
    for i, id in enumerate(camera_ids):
        while True:
            res = api.get_stream_url(id)
            if res['code'] == 200:
                s = res['data']
                source.append(s)
                push_rtsp_stream(s, i)
                break
    print(source)
    while True:
        pass