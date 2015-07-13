import os
from tools.audio_manager import audio_manager
from tools.video_manager import video_manager

files = os.listdir(os.path.join(os.getcwd(), 'video_samples'))
print 'Choose a file:'
i = 1
for file in files:
    print str(i) + ' - ' + os.path.basename(file)
    i += 1

chosen_file = ''
choice = raw_input('>')

try:
    chosen_file = files[int(choice)-1]
    print chosen_file
except:
    print 'Wrong choice'

a_m = audio_manager()
v_m = video_manager(os.path.join('video_samples', unicode(chosen_file)))
audio = v_m.get_audio_from_video()

print audio

folder = a_m.split_wav_file(audio, 10)

print folder

print 'Done.'

