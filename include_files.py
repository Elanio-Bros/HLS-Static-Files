import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
from moviepy.editor import *
import sys
import datetime
import time
import os
from threading import Thread

TEMP_PATH = './temp'
# Create Files
if not os.path.exists('{}/'.format(TEMP_PATH)):
    os.mkdir('{}/'.format(TEMP_PATH))


def monitor(ffmpeg, duration, time_, time_left, process):
    per = round(time_ / duration * 100)
    sys.stdout.write(
        "\rTranscoding...(%s%%) %s left [%s%s]" %
        (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
    )
    sys.stdout.flush()


def code_videos(id, value):
    video = value

    clip = VideoFileClip(video)
    if id >= 1:
        clip = clip.subclip(67, -1)

    if id <= 1:
        clip = clip.subclip(0, clip.duration-44)

    # clip = clip.subclip(0, 60)
    file="{}/temp{}.mp4".format(TEMP_PATH, id)
    clip.write_videofile(file)
    video = ffmpeg_streaming.input(file)

    _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
    _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
    _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))

    hls = video.hls(Formats.h264(), hls_time=5)
    hls.representations(_480p, _720p, _1080p)
    hls.flags('independent_segments')
    hls.output("{}/{}/hls.m3u8".format(TEMP_PATH, value), monitor=monitor)
    os.remove(file)


for id, value in enumerate([]):
    t = Thread(target=code_videos, args=(id, value))
    t.start()
