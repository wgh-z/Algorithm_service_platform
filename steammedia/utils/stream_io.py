import subprocess


def push_rtsp_stream(source, stream_id=0):
    command = [
        'ffmpeg',
        '-re',  # 以本地帧速率发送流
        '-stream_loop', '-1',  # 循环播放
        '-i', source,
        '-rtsp_transport', 'tcp',  # 传输协议
        '-bufsize', '1000000k',
        '-preset:v', 'ultrafast',
        '-tune:v', 'zerolatency',
        '-vcodec', 'copy',
        # '-acodec', 'aac',
        '-f', 'rtsp',
        'rtsp://127.0.0.1:8554/stream' + str(stream_id)
    ]
    subprocess.Popen(command)


if __name__ == "__main__":
    source = [
        r'D:\Projects\python\47.Head-count-optimization-mt\Highway-incident\1.mp4',
        r'D:\Projects\python\47.Head-count-optimization-mt\Highway-incident\2.mp4',
        r'D:\Projects\python\47.Head-count-optimization-mt\Highway-incident\3.mp4',
        r'D:\Projects\python\47.Head-count-optimization-mt\Highway-incident\4.mp4',
    ]
    for i, s in enumerate(source):
        push_rtsp_stream(s, i)
    while True:
        pass
