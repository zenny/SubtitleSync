import os
import sys
import copy
import functools
from tools.audio_manager import audio_manager
from tools.video_manager import video_manager
from tools.srt_parser import srt_parser
from tools.silence_detector import silence_detector
from tools.speech_recognition_manager import speech_recognition_manager
from tools.matching_manager import matching_manager
from gui import GuiManager

####################################################
#Choose video and subtitle
####################################################

'''
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
'''

class MainClass():
    
    def SyncBtnCallBack(self):
        self.CHOSEN_VIDEO = self.gui_manager.video_file_dialog.entry.get()
        self.CHOSEN_SRT = self.gui_manager.subtitle_file_dialog.entry.get()
        self.oldMain()
    
    def RunMain(self):
        SyncBtnCallBackPartial = functools.partial(MainClass.SyncBtnCallBack, self)
        self.gui_manager = GuiManager(SyncBtnCallBackPartial)
        self.gui_manager.RunSubSyncGuiMainLoop()
    
    def oldMain(self):
        ####################################################
        #Converting from video to audio
        ####################################################

        print '\nExtracting audio...'
        v_m = video_manager(os.path.join('video_samples', self.CHOSEN_VIDEO))
        AUDIO_FILE = v_m.get_audio_from_video()
        print 'Done.'
        #END

        ####################################################
        #Reading .srt file
        ####################################################

        print '\nReading subtitles...'
        strp = srt_parser()
        SUBTITLES = strp.parse_ms(os.path.join('subtitle_samples', self.CHOSEN_SRT))
        print 'Read ' + str(len(SUBTITLES)) + ' subtitles.'
        #END

        ####################################################
        #Splitting audio file on silence
        ####################################################
        print '\nDetecting speech segments...\n'
        s_d = silence_detector()
        MAP_INTERVALS = s_d.split_on_silence(AUDIO_FILE)
        print 'Found ' + str(len(MAP_INTERVALS)) + ' possible segments.'
        #END

        ####################################################
        #Transcripting audio speech segments
        ####################################################

        print '\nTranscripting speech segments...'
        s_r_m = speech_recognition_manager()
        TIMESTAMPED_TRANSCRIPTIONS = s_r_m.speech_to_text(MAP_INTERVALS)
        print "\n" + str(len(TIMESTAMPED_TRANSCRIPTIONS)) + ' out of ' + str(len(MAP_INTERVALS)) + ' successful transcriptions.\n'
        for timestamped_text in TIMESTAMPED_TRANSCRIPTIONS:
            print timestamped_text
        #END

        ####################################################
        #Translating subtitles text
        ####################################################

        print '\nTranslating subtitles...'
        TRANSLATED_SUBTITLES = s_r_m.translate(copy.deepcopy(SUBTITLES), from_language = 'pt', to_language = 'en')
        print '\n' + str(len(TRANSLATED_SUBTITLES)) + ' out of ' + str(len(SUBTITLES)) + ' successful translations.'
        for timestamped_sub in TRANSLATED_SUBTITLES:
            print timestamped_sub
        #END

        ####################################################
        #Matching subtitles with speech segments transcriptions
        ####################################################
        print '\nMatching subtitles and transcriptions...'
        m_m = matching_manager()
        CORRECTED_TIME_SUBTITLES = m_m.match_subs_trans(TRANSLATED_SUBTITLES, TIMESTAMPED_TRANSCRIPTIONS, SUBTITLES)
        #END

        ####################################################
        #Writing results
        ####################################################
        print '\nWriting synchronized subtile in file...'
        # get original subtitle text
        output_path = os.path.join(os.getcwd(), 'subtitle_samples', 'SYNC-%s'%(self.CHOSEN_SRT))
        open(output_path, 'wb').write(strp.format_ms(CORRECTED_TIME_SUBTITLES))
        print '\nEnd of synchronization...'
        #END

if __name__=='__main__':
    MainClass().RunMain()