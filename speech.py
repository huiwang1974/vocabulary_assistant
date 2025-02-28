from jnius import autoclass

TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
Locale = autoclass('java.util.Locale')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

class Speech:
    def __init__(self):
        self.tts = TextToSpeech(PythonActivity.mActivity, None)
        self.set_language('en-US')

    def speak(self, text):
        self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)

    def stop(self):
        self.tts.stop()

    def speeking(self):
        return self.tts.isSpeaking()

    def set_language(self, language):
        p1, p2 = language.split('-')
        self.tts.setLanguage(Locale(p1, p2))
