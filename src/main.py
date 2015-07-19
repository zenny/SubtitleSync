import os
import sys
from tools.audio_manager import audio_manager
from tools.video_manager import video_manager
from tools.srt_parser import srt_parser
from tools.silence_detector import silence_detector

video_files = os.listdir(os.path.join(os.getcwd(), 'video_samples'))
srt_files = os.listdir(os.path.join(os.getcwd(), 'subtitle_samples'))
i = 1
print 'Select one of the available videos:\n'
for v_file in video_files:
    print str(i) + ' - ' + os.path.basename(v_file)
    i += 1

chosen_video = ''
v_choice = raw_input('>')

i = 1
print '\nSelect one of the available subtitles:\n'
for s_file in srt_files:
    print str(i) + ' - ' + os.path.basename(s_file)
    i += 1

chosen_srt = ''
s_choice = raw_input('>')

chosen_video = video_files[int(v_choice)-1]
chosen_srt = srt_files[int(s_choice)-1]
if not chosen_video.endswith('.mp4') or not chosen_srt.endswith('.srt'):
    print 'Invalid choice.'
    sys.exit(0)

print '\nExtracting audio...'
v_m = video_manager(os.path.join('video_samples', chosen_video))
audio = v_m.get_audio_from_video()
print 'Done.'

print '\nReading subtitles...'
strp = srt_parser()
subtitles = strp.parse(os.path.join('subtitle_samples', chosen_srt))
print 'Read ' + str(len(subtitles)) + ' subtitles.'

print '\nDetecting audio speeches.'
s_d = silence_detector()
s_d.split_on_silence(audio)