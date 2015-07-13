import os
import subprocess
import time
import re

class audio_manager():
    def split_wav_file(self, path, number_of_parts):
        '''
            Split a wave file in number_of_parts parts.

            Args;
                path(string, optional): full path of the wave file.

            Returns;
                string containing the folder with the split audio files.
        '''
        if path == None or path == '' or path.endswith('.wav'):
            raise Exception('Invalid file.')

        stat_process = None
        stat_command = 'sox {0} -n stat'.format(path)
        length_re = re.compile('Length (seconds):(.+)\n')
        length = -1
        stat_output = ''

        try:
            stat_process = subprocess.Popen(stat_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            stat_error, stat_output = stat_process.communicate()

            if stat_output is not None:
                #TODO: fix the regular expression search pattern length_re
                length = float(length_re.search(stat_output).strip())

        except Exception, e:
            print 'Read failed. Reason: ' + unicode(e.message)

        if stat_process != None:
            stat_process.terminate()

        trim_process = None
        trim_error = ''
        trim_output = ''

        #TODO: add the files to a subfolder.
        if length > 0:
            factor = int(length)/number_of_parts
            for i in range(0, number_of_parts):
                out = os.basename(path).split('.')[0] + '_' + str(i) + '.wav'
                trim_command = 'sox {0} {1} trim {2} {3}'.format(path, out, str(i*factor), str(((i+1)*factor) - 0.001))

                try:
                    trim_process = subprocess.Popen(trim_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    trim_output, trim_error = trim_process.communicate()

                except Exception, e:
                    print 'Split failed. Reason: ' + unicode(e.message)

                if trim_process != None:
                    trim_process.terminate()
                    trim_process = None
                    trim_error = ''
                    trim_output = ''

        return os.path.join(os.getcwd())