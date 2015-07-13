import os
import subprocess
import time

class video_manager():
    def __init__(self, video):
        '''
            Class constructor

            Args:
                video(string): full path of the file that is going to be processed.

            Returns:
                None
        '''
        self.video_path = video

    def get_audio_from_video(self, video = None):
        '''
            Generate a wave file containing the audio from a video (160kbits/s, 44100Hz, 2 channels)

            Args;
                video(string, optional): full path of the video. Overwrites the global variable.

            Returns;
                string containing the full path of the generated wave file.
        '''
        if video != None and video != '':
            self.video_path = video

        process = None
        audio_filename = 'audio_' + str(time.time()).replace('.','') + '.wav'
        convert_command = "ffmpeg -i {0} -ab 160k -ac 2 -ar 44100 -vn {1}".format(self.video_path, audio_filename)

        try:
            process = subprocess.Popen(convert_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            output, error = process.communicate()

            #It seems ffmpeg is directing the output to stderr instead of stdout...
            if error is not None:
                print 'Convertion failed. Reason: ' + unicode(error)

        except Exception, e:
            print 'Convertion failed. Reason: ' + unicode(e.message)

        if process != None:
            process.terminate()

        return os.path.join(audio_filename)