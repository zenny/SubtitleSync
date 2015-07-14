import os
from tools.srt_parser import srt_parser

filename = "sample.srt"

strp = srt_parser()
segments = strp.parse(filename)
for segment in segments:
    print segment
    print 

