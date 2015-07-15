import os

files = os.listdir(os.path.join(os.getcwd(), 'audio_samples'))
print 'Choose a file:'
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

chosen_file = os.path.join('audio_samples', chosen_file)
print chosen_file
    
import tools.speech_recognition.speech_recognition as sr

r = sr.Recognizer("en-US")
with sr.WavFile(chosen_file) as source:             # use "teste.wav" as the audio source
    audio = r.record(source)                        # extract audio data from the file

try:
    print("Transcription: " + r.recognize(audio))   # recognize speech using Google Speech Recognition
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")