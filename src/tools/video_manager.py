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
        audio_filename = os.path.join('audio_samples', "audio_" + str(time.time()).replace('.','') + '.wav')
        convert_command = "ffmpeg -i \"{0}\" -ab 160k -ac 1 -ar 44100 -vn \"{1}\"".format(self.video_path, audio_filename)

        print "\nRunning " + convert_command

        try:
            process = subprocess.Popen(convert_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            output, error = process.communicate()

        except Exception, e:
            print 'Exception when converting file. Reason: ' + unicode(e.message)

        if process != None:
            process.terminate()

        return os.path.join(audio_filename)