import os
import sys
import locale

import speech_recognition.speech_recognition as SpeechRecognizer
from translation.translate import Translator

class speech_recognition_manager():
    def speech_to_text(self, timestamped_segments):
        '''
            Returns a list containing timestamped texts related to each audio file provided.

            Args:
                timestamped_segments(list): list of lists containing timestamps and the path to the audio file.
                                            format: [
                                                        (1.2,1.4,'audio_samples\\trimmed\\audio_filename\\audio_filename_1.wav'),
                                                        (2.0,2.3,'audio_samples\\trimmed\\audio_filename\\audio_filename_2.wav'),
                                                        and so on.
                                                    ]

            Returns:
                list of tuples containing timestamps and the transcripted audio.
                format: [
                            (1.2,1.4,'The One Where It AII Began'),
                            (2.0,2.3,'Aquele Em Que Monica Arruma'),
                            and so on.
                        ]
        '''
        timestamped_texts = []
        recognizer = SpeechRecognizer.Recognizer()
        transcription = ''

        for timestamped_segment in timestamped_segments:
            with SpeechRecognizer.WavFile(timestamped_segment[2]) as source:
                audio = recognizer.record(source)

            for times in range(0,2):
                try:
                    transcription = recognizer.recognize(audio)
                    break
                except LookupError as error:
                    if times == 1 :
                        print("Could not understand audio")

            if transcription != '':
                timestamped_texts.append((timestamped_segment[0], timestamped_segment[1], transcription))
            transcription = ''

        return timestamped_texts

    def translate(self, timestamped_segments, from_language = 'en', to_language = 'pt'):
        timestamped_translations = []
        translator = Translator(from_lang = from_language, to_lang = to_language)
        translation = ''

        for timestamped_segment in timestamped_segments:
            translation = translator.translate(timestamped_segment[2])
            if sys.version_info.major == 2:
                translation = translation.encode(locale.getpreferredencoding())

            timestamped_translations.append((timestamped_segment[0], timestamped_segment[1], translation))
            translation = ''

        return timestamped_translations