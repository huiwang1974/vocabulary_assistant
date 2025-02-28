from jnius import autoclass, PythonJavaClass, java_method

PythonActivity = autoclass('org.kivy.android.PythonActivity')
SpeechRecognizerAndroid = autoclass('android.speech.SpeechRecognizer')
Intent = autoclass('android.content.Intent')
RecognizerIntent = autoclass('android.speech.RecognizerIntent')
Bundle = autoclass('android.os.Bundle')
JavaString = autoclass('java.lang.String')

class RecognitionRunnable(PythonJavaClass):
    __javainterfaces__ = ['java/lang/Runnable']
    __javaclass__ = 'org/test/RecognitionRunnable'
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    @java_method('()V')
    def run(self):
        self.callback()

class SpeechListener(PythonJavaClass):
    __javainterfaces__ = ['android/speech/RecognitionListener']
    __javaclass__ = 'org/test/SpeechListener'
    
    def __init__(self, callback, restart_callback, error_callback):
        super().__init__()
        self.callback = callback
        self.restart_callback = restart_callback
        self.error_callback = error_callback

    @java_method('([B)V')
    def onBufferReceived(self, buffer):
        print("Buffer received")
        
    @java_method('(I)V')
    def onError(self, error):
        print(f"Speech recognition error: {error}")
        
        error_messages = {
            SpeechRecognizerAndroid.ERROR_AUDIO: "Audio recording error",
            SpeechRecognizerAndroid.ERROR_CLIENT: "Client side error",
            SpeechRecognizerAndroid.ERROR_INSUFFICIENT_PERMISSIONS: "Insufficient permissions",
            SpeechRecognizerAndroid.ERROR_NETWORK: "Network error",
            SpeechRecognizerAndroid.ERROR_NETWORK_TIMEOUT: "Network timeout",
            SpeechRecognizerAndroid.ERROR_NO_MATCH: "No match found",
            SpeechRecognizerAndroid.ERROR_RECOGNIZER_BUSY: "RecognitionService busy",
            SpeechRecognizerAndroid.ERROR_SERVER: "Server error",
            SpeechRecognizerAndroid.ERROR_SPEECH_TIMEOUT: "No speech input"
        }
        error_message = error_messages.get(error, f"Unknown error: {error}")
        print(f"Speech recognition error: {error_message}")
        
        # These errors are "normal" and we should restart after them
        recoverable_errors = [
            SpeechRecognizerAndroid.ERROR_NO_MATCH,
            SpeechRecognizerAndroid.ERROR_SPEECH_TIMEOUT,
            SpeechRecognizerAndroid.ERROR_NETWORK_TIMEOUT
        ]
        
        if error in recoverable_errors:
            print("Recoverable error, restarting recognition...")
            self.restart_callback()
        else:
            self.error_callback(f"Error: {error_message}")
        
    @java_method('(ILandroid/os/Bundle;)V')
    def onEvent(self, event_type, params):
        print(f"Event received {event_type}")
        
    @java_method('(Landroid/os/Bundle;)V')
    def onPartialResults(self, partial_results):
        print("partial results")
        
    @java_method('(Landroid/os/Bundle;)V')
    def onReadyForSpeech(self, params):
        print("Ready for speech")
        
    @java_method('(Landroid/os/Bundle;)V')
    def onResults(self, results):
        matches = results.getStringArrayList(SpeechRecognizerAndroid.RESULTS_RECOGNITION)
        if matches and matches.size() > 0:
            text = matches.get(0)
            print(f"Recognized text: {text}")
            self.callback(text)
        # Restart listening
        self.restart_callback()
            
    @java_method('(F)V')
    def onRmsChanged(self, rmsdB):
        print("RMS changed")
        
    @java_method('()V')
    def onEndOfSpeech(self):
        print("Speech ended")
        
    @java_method('()V')
    def onBeginningOfSpeech(self):
        print("Speech started")

class SpeechRecognizer:
    def __init__(self, recognition_callback, start_callback, stop_callback, error_callback):
        self.speech_recognizer = None
        self.speech_listener = None
        self.is_listening = False
        self.language = 'en-US'
        self.recognition_callback = recognition_callback
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.error_callback = error_callback

    def __listener_recognition_callback(self, text):
        self.recognition_callback(text)

    def __listener_error_callback(self, error_message):
        self.error_callback(f'Error: {error_message}')

    def __restart_recognizer(self):
        # Create new intent for next recognition
        intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        
        # Create a Java String for the language code
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, JavaString(self.language))
        intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, True)
        
        # Set speech timeout parameters
        intent.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 2000)
        intent.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 3000)
        intent.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 3000)
        
        # Start listening again
        print("Starting recognition again...")
        self.speech_recognizer.startListening(intent)
        self.start_callback()

    def __start_recognizer(self):
        self.speech_recognizer = SpeechRecognizerAndroid.createSpeechRecognizer(PythonActivity.mActivity)
        self.speech_listener = SpeechListener(self.__listener_recognition_callback, self.__restart_recognizer, self.__listener_error_callback)
        self.speech_recognizer.setRecognitionListener(self.speech_listener)
        self.__restart_recognizer()

    def __stop_recognizer(self):
        try:
            self.speech_recognizer.stopListening()
            self.speech_recognizer.destroy()
            self.speech_recognizer = None
            self.is_listening = False
            self.stop_callback()
        except Exception as e:
            print(f"Error stopping recognition: {str(e)}")
            self.error_callback(f'Error stopping recognition: {str(e)}')

    def set_language(self, language):
        self.language = language

    def start_listening(self):
        try:
            if not self.is_listening:
                print("Starting recognition...")
                runnable = RecognitionRunnable(self.__start_recognizer)
                PythonActivity.mActivity.runOnUiThread(runnable)
                self.is_listening = True
        except Exception as e:
            print(f"Error starting recognition: {str(e)}")
            self.error_callback(f'Error starting recognition: {str(e)}')
            self.is_listening = False
        
    def stop_listening(self):
        if self.speech_recognizer:
            try:
                runnable = RecognitionRunnable(self.__stop_recognizer)
                PythonActivity.mActivity.runOnUiThread(runnable)
            except Exception as e:
                print(f"Error stopping recognition: {str(e)}")
                self.error_callback(f'Error stopping recognition: {str(e)}')