#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
# import os
import time
# from pathlib import Path
from threading import Thread
import cv2
import numpy as np


class LoadStreams:
    def __init__(self, sources, grid_w, grid_h, vid_stride=1):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.vid_stride = vid_stride
        # sources = Path(sources).read_text().rsplit() if os.path.isfile(sources) else [sources]
        n = len(sources)

        self.void_img = self.create_void_img(self.grid_w, self.grid_h)

        self.imgs, self.fps, self.frames, self.threads = [None] * n, [0] * n, [0] * n, [None] * n
        for i, s in enumerate(sources):
            st = f"{i + 1}/{n}: {s} "

            s = eval(s) if s.isnumeric() else s

            cap = cv2.VideoCapture(s)
            assert cap.isOpened(), f"{st}打开失败 {s}"
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            self.frames[i] = max(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 0) or float("inf")
            self.fps[i] = max((fps if math.isfinite(fps) else 0) % 100, 0) or 30

            _, self.imgs[i] = cap.read()
            self.threads[i] = Thread(target=self.update, args=([i, cap, s]), daemon=True)
            print(f"{st}打开成功(帧长度{self.frames[i]}，帧尺寸{w}x{h}，{self.fps[i]:.2f} FPS)")
            self.threads[i].start()

    def create_void_img(self, w, h):
        void_img = np.zeros((720, 1280, 3), dtype=np.uint8)
        void_img = cv2.putText(void_img, 'no signal', (500, 360), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
        void_img = cv2.resize(void_img, (w, h))
        return void_img

    def update(self, i, cap, stream):
        n, f = 0, self.frames[i]
        while cap.isOpened() and n < f:
            n += 1
            cap.grab()  # .read() = .grab() + .retrieve()
            if n % self.vid_stride == 0:
                success, im = cap.retrieve()
                if success:
                    self.imgs[i] = im
                else:
                    # print("rtsp摄像头无响应")

                    self.imgs[i] = self.void_img
                    # try:
                    #     cap.open(stream)
                    # except:
                    #     print("rtsp摄像头重连失败, 再次尝试连接...")
            time.sleep(0.0)

    def __iter__(self):
        self.count = -1
        return self

    def __next__(self):
        self.count += 1
        if not all(x.is_alive() for x in self.threads) or cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            raise StopIteration

        im0 = self.imgs.copy()
        im0 = [cv2.resize(x, (self.grid_w, self.grid_h)) for x in im0]
        return im0
