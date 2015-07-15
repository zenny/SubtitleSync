import os
import subprocess
import re

class audio_manager():
    def split_wav_file(self, a_path, number_of_parts):
        '''
            Split a wave file in number_of_parts parts.

            Args;
                a_path(string, optional): full path of the wave file.

            Returns;
                string containing the folder with the split audio files.
        '''
        if a_path == None or a_path == '' or not a_path.endswith('.wav'):
            raise Exception('Invalid file.')

        stat_process = None
        stat_command = 'sox {0} -n stat'.format(a_path)
        length = -1
        stat_output = ''

        try:
            stat_process = subprocess.Popen(stat_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            stat_error, stat_output = stat_process.communicate()

            if stat_output is not None:
                length = float(re.findall("\d+.\d+", stat_output.split('\r\n')[1])[0])

        except Exception, e:
            print 'Read failed. Reason: ' + unicode(e.message)

        if stat_process != None:
            stat_process.terminate()

        trim_process = None
        trim_error = ''
        trim_output = ''

        if length > 0:
            offset = length/number_of_parts
            out = os.path.basename(a_path)
            folder_name = os.path.join('audio_samples', out.split('.')[0])

            if not os.path.isdir(folder_name):
                os.makedirs(folder_name)
            trim_command = 'sox {0} {1} trim {2} {3} : newfile : restart'.format(a_path, os.path.join(folder_name, out), '0', str(offset))
            
            print "\n #### Running trim_command ####"
            print trim_command
            print ""
            
            try:
                trim_process = subprocess.Popen(trim_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                trim_output, trim_error = trim_process.communicate()

            except Exception, e:
                print 'Split failed. Reason: ' + unicode(e.message)

            if trim_process != None:
                trim_process.terminate()

            return os.path.join(os.getcwd(), folder_name)
        return None