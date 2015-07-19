import os
import sys
from tools.audio_manager import audio_manager
from tools.video_manager import video_manager
from tools.srt_parser import srt_parser
from tools.silence_detector import silence_detector
from tools.speech_recognition_manager import speech_recognition_manager

##########################
#Choose video and subtitle
##########################
VIDEO_FILES = os.listdir(os.path.join(os.getcwd(), 'video_samples'))
SRT_FILES = os.listdir(os.path.join(os.getcwd(), 'subtitle_samples'))
i = 1
print 'Select one of the available videos:\n'
for v_file in VIDEO_FILES:
    print str(i) + ' - ' + os.path.basename(v_file)
    i += 1

v_choice = raw_input('> ')

i = 1
print '\nSelect one of the available subtitles:\n'
for s_file in SRT_FILES:
    print str(i) + ' - ' + os.path.basename(s_file)
    i += 1

s_choice = raw_input('> ')

CHOSEN_VIDEO = VIDEO_FILES[int(v_choice)-1]
CHOSEN_SRT = SRT_FILES[int(s_choice)-1]
if ((not CHOSEN_VIDEO.endswith('.mp4'))
    and not CHOSEN_VIDEO.endswith('.avi')
    or not CHOSEN_SRT.endswith('.srt')):
    print 'Invalid choice.'
    sys.exit(0)
#END

##########################
#Converting from video to audio
##########################
print '\nExtracting audio...'
v_m = video_manager(os.path.join('video_samples', CHOSEN_VIDEO))
AUDIO_FILE = v_m.get_audio_from_video()
print 'Done.'
#END

##########################
#Reading .srt file
##########################
print '\nReading subtitles...'
strp = srt_parser()
SUBTITLES = strp.parse(os.path.join('subtitle_samples', CHOSEN_SRT))
print 'Read ' + str(len(SUBTITLES)) + ' subtitles.'
#END

##########################
#Splitting audio file on silence
##########################
print '\nDetecting speech segments...'
s_d = silence_detector()
MAP_INTERVALS = s_d.split_on_silence(AUDIO_FILE)
#END

##########################
#Transcripting segments
##########################
print '\nTranscripting speech segments...'
s_r_m = speech_recognition_manager()
TIMESTAMPED_TEXTS = s_r_m.speech_to_text(MAP_INTERVALS, from_language = 'en', to_language = 'pt')
print str(len(TIMESTAMPED_TEXTS)) + ' out of ' + str(len(MAP_INTERVALS)) + ' successful transcriptions.'
for timestamped_text in TIMESTAMPED_TEXTS:
    print timestamped_text
#END

