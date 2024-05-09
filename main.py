import os
import shutil
from load_videos import Load_Videos

# Live Stream
DEFAULT_PATH = './file'
TEMP_PATH = './temp'

# clear past files
# shutil.rmtree('{}/'.format(DEFAULT_PATH), True)

# create past if is not exists
if not os.path.exists('{}/'.format(DEFAULT_PATH)):
    os.mkdir('{}/'.format(DEFAULT_PATH))

if not os.path.exists('{}/'.format(TEMP_PATH)):
    os.mkdir('{}/'.format(TEMP_PATH))

uri = None
path = None

# list reproduction
files = []

while True:
    for dir in files:
        dir = '{}/{}'.format(TEMP_PATH, dir)
        if os.path.isdir(dir) and os.path.exists(dir):
            loads = []
            for resolution in ['480p', '720p', '1080p']:
                load_videos = Load_Videos(resolution, DEFAULT_PATH, dir, uri, path)
                loads.append(load_videos)
            for load in loads:
                load.start()
            for load in loads:
                load.join()
                
            # Removido para limpeza
            shutil.rmtree(dir+"/")
