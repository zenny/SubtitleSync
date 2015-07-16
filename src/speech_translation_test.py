import os
import sys
import tools.speech_recognition.speech_recognition as SpeechRecognizer
from tools.translation.translate import Translator
import locale

##############################################
# choose input file
##############################################

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
    sys.exit(0)

##############################################
# Recognize speech
##############################################
    
chosen_file = os.path.join('audio_samples', chosen_file)
print chosen_file
    
recognizer = SpeechRecognizer.Recognizer()
with SpeechRecognizer.WavFile(chosen_file) as source:   # use "teste.wav" as the audio source
    audio = recognizer.record(source)                   # extract audio data from the file

for times in range(0,10):    
    try:
        transcription = recognizer.recognize(audio)
        print("Transcription: " + transcription)            # recognize speech using Google Speech Recognition
        break
    except LookupError as error:                            # speech is unintelligible
        print(error.args)
        if times == 9 :
            print("Could not understand audio")
            sys.exit(0)
    
##############################################
# Translate text
##############################################

translator = Translator(from_lang="en", to_lang="pt")

translation = translator.translate(transcription)
if sys.version_info.major == 2:
    translation = translation.encode(locale.getpreferredencoding())
    
sys.stdout.write("Translated transcription:\n")
sys.stdout.write(translation)
sys.stdout.write("\n")

    