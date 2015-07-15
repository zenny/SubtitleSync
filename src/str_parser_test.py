import os
from tools.srt_parser import srt_parser

files = os.listdir(os.path.join(os.getcwd(), 'video_samples'))
print 'Choose a file: (with extention .srt)'
i = 1
for file in files:
    print str(i) + ' - ' + os.path.basename(file)
    i += 1

chosen_file = ''
choice = raw_input('>')

try:
    chosen_file = files[int(choice)-1]
except:
    print 'Wrong choice'

filename = os.path.join('video_samples', chosen_file)
print filename


strp = srt_parser()
segments = strp.parse(filename)
for segment in segments:
    print segment    

