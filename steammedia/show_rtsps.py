#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from utils.get_stream import CameraAPI
from utils.stream_loader import LoadStreams


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
    for id in camera_ids:
        while True:
            res = api.get_stream_url(id)
            if res['code'] == 200:
                source.append(res['data'])
                break
    print(source)

    show_w, show_h = 1920, 1080
    n = len(source)
    scale = int(np.ceil(np.sqrt(n)))
    grid_w = int(show_w / scale)
    grid_h = int(show_h / scale)

    im_show = np.zeros((show_h, show_w, 3), dtype=np.uint8)
    dataset = LoadStreams(source, grid_w, grid_h, vid_stride=1)

    for im0s in dataset:
        for i, im0 in enumerate(im0s):  # 拼接
            im_show[grid_h*(i//scale):grid_h*(1+(i//scale)), grid_w*(i%scale):grid_w*(1+(i%scale))] = im0
        cv2.imshow("im_show", im_show)
        if cv2.waitKey(1) == ord("q"):
            break
