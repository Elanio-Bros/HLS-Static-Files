from threading import Thread
import time
import os
import shutil
import m3u8
from m3u8 import Segment


class Load_Files(Thread):
    def __init__(self, resolution, default_path, dir, uri, path):
        Thread.__init__(self)
        self.resolution = resolution
        self.default_path = default_path
        self.dir = dir
        self.uri = uri
        self.path = path
        self.version = '3'
        self.duration=0

    def run(self):
        __file_stream__ = "hls_{}.m3u8".format(self.resolution)
        __playlist__ = '{}/hls.m3u8'.format(self.default_path)
        __stream__ = '{}/{}'.format(self.default_path, __file_stream__)
        __temp__ = "{}/{}".format(self.dir, __file_stream__)

        file_strem = open(__stream__, "a").close()

        file_playlist = open(__playlist__, "a")
        if os.path.exists(__playlist__):
            file_playlist.truncate(0)
        file_playlist.close()

        playlist = m3u8.load(__playlist__)
        temp_playlist = m3u8.load("{}/hls.m3u8".format(self.dir))
        playlist.version = self.version
        for list in temp_playlist.playlists:
            playlist.add_playlist(list)
        playlist.dump(__playlist__)

        if os.path.exists(__stream__) and os.path.exists(__temp__):
            original = m3u8.load(__stream__)
            original.version = self.version
            
            original.dump(__stream__)
            
            media = m3u8.load(__temp__)

            for id, segment in enumerate(media.segments):
                id_seg = 0 if len(original.segments.by_key(None)) == 0 else int(
                    (original.segments[-1].uri).replace('.ts', '').replace('{}_'.format(self.resolution), ''))+1
                name_file = "{}_{}.ts".format(self.resolution, id_seg)
                file = "{}/{}".format(self.dir, segment.uri)

                if os.path.exists(file):
                    shutil.copy(file, './file/{}'.format(name_file))
                    if id_seg >= 5:
                        segment_0 = original.segments[0]
                        self.duration=segment_0.duration
                        self.uri = segment_0.uri
                        # time remove other file
                        original.segments.pop(0)
                        # get new uri segment
                        original.media_sequence = int(original.media_sequence)+1
                        # original.discontinuity_sequence = next_sequence
                    else:
                        # original.discontinuity_sequence = '0'
                        original.media_sequence = '0'
                        original.target_duration = int(segment.duration)
                        time.sleep(int(segment.duration))

                    original.add_segment(
                        Segment(name_file, duration=segment.duration, discontinuity=self.path != self.dir))

                    self.path = self.dir
                    original.target_duration = int(segment.duration) if int(segment.duration) > int(
                        original.target_duration) else int(original.target_duration)
                    original.allow_cache='NO'
                    original.dump(__stream__)
                    if self.uri != None:
                        time.sleep(self.duration)
                        os.remove('{}/{}'.format(self.default_path, self.uri))
