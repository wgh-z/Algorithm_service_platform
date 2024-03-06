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
        '44030599001326008152'
    ]

    api = CameraAPI(api_host)

    source = []
    for id in camera_ids:
        res = api.get_stream_url(id)
        if res['code'] == 200:
            source.append(res['data'])
    print(source)

    # source = [
    #     "rtsp://127.0.0.1:8554/stream1",
    #     "rtsp://127.0.0.1:8554/stream2",
    #     "rtsp://127.0.0.1:8554/stream3",
    #     "rtsp://127.0.0.1:8554/stream4",
    # ]
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
