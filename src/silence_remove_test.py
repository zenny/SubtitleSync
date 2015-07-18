import os
import subprocess
import re

process = None
audio_filename = 'audio_143701482948007.wav'
convert_command = "ffmpeg -i {0} -af silencedetect=n=0.12:d=0.5 -f null -".format(audio_filename)
# convert_command = "ffmpeg -i {0} -af silenceremove=1:0.15:0.029:-1:0.15:0.029 out.wav".format(audio_filename)

print "\n #### Running convert_command ####"
print convert_command
print ""

try:
    process = subprocess.Popen(convert_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, error = process.communicate()
    
    #It seems ffmpeg is directing the output to stderr instead of stdout...
    if error is not None:
        print error
        error = filter( lambda a : len(a)>0, re.compile("[ \r\n,]").split(error))
        
        start_audio = [0.0]
        end_audio = []
        total_time = 0 
        
        for idx in range(0,len(error)) :
            if error[idx] == "silence_start:" :
                end_audio.append(float(error[idx+1]))
            if error[idx] == "silence_end:" :
                start_audio.append(float(error[idx+1]))
            if error[idx] == "Duration:" :
                total_time = float(error[idx+1].split(":")[2])
                
        end_audio.append(total_time)
        
        print start_audio
        print end_audio
        
        for idx in range(0,len(start_audio)):
            s = start_audio[idx]
            d = end_audio[idx] - s
            trim_command = "sox {0} out_audio_{1}.wav trim {2} {3}".format(audio_filename, idx+1, s, d)
            process = subprocess.Popen(trim_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            output, error = process.communicate()
            
except Exception, e:
    print 'Exception when converting file. Reason: ' + unicode(e.message)

if process != None:
    process.terminate()
