from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import json
import threading
from kivy.clock import mainthread
import environment as env
from appstorage import AppStorage
from listpopup import ListPopup
from testpopup import TestPopup
from llmhelper import LLMHelper
from speechrecognizer import SpeechRecognizer
from speech import Speech
from settingpopup import SettingPopup
import commands

class VocabularyAssistantApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        env.load_environment()
        self.listening_started = False
        self.lookup_started = False
        self.tts = Speech()
        self.app_storage = AppStorage.get_appstorage()
        self.llm_helper = LLMHelper()
        self.speech_recognizer = SpeechRecognizer(self.__recognition_callback, self.__start_listening_callback, self.__stop_listening_callback, self.__error_listening_callback)

    @mainthread
    def update_language_label(self, language):
        self.language_label.text = f'Language: {language}'

    @mainthread
    def update_status_label(self, text):
        self.status_label.text = f'Status: {text[0:20]}'

    @mainthread
    def update_event_label(self, text):
        self.event_label.text = f'Events: {text[0:20]}'

    @mainthread
    def update_translation_label(self, text):
        self.translation_label.text = text

    @mainthread
    def update_transcription_text(self, text):
        self.transcription_text.text = text

    def __recognition_callback(self, text):
        # Set language based on recognition result
        cmd = commands.command_in_english(text.lower())
        if cmd and cmd == 'chinese':
            self.speech_recognizer.set_language('zh-CN')
            self.tts.set_language('zh-CN')
            self.update_language_label('zh-CN')
            self.update_event_label('set current language to chinese')
        elif cmd and cmd == 'japanese':
            self.speech_recognizer.set_language('ja-JP')
            self.tts.set_language('ja-JP')
            self.update_language_label('ja-JP')
            self.update_event_label('set current language to japanese')
        elif cmd and cmd == 'korean':
            self.speech_recognizer.set_language('ko-KR')
            self.tts.set_language('ko-KR')
            self.update_language_label('ko-KR')
            self.update_event_label('set current language to korean')
        elif cmd and cmd == 'spanish':
            self.speech_recognizer.set_language('es-ES')
            self.tts.set_language('es-ES')
            self.update_language_label('es-ES')
            self.update_event_label('set current language to spanish')
        elif cmd and cmd == 'german':
            self.speech_recognizer.set_language('de-DE')
            self.tts.set_language('de-DE')
            self.update_language_label('de-DE')
            self.update_event_label('set current language to german')
        elif cmd and cmd == 'french':
            self.speech_recognizer.set_language('fr-FR')
            self.tts.set_language('fr-FR')
            self.update_language_label('fr-FR')
            self.update_event_label('set current language to french')
        elif cmd and cmd == 'english':
            self.speech_recognizer.set_language('en-US')
            self.tts.set_language('en-US')
            self.update_language_label('en-US')
            self.update_event_label('set current language to english')
        elif cmd and cmd == 'read':
            if self.transcription_text.text:
                self.text_to_speech(f"{self.transcription_text.text} {self.translation_label.text}")
                self.update_event_label("start reading")
        elif cmd and cmd == 'quiet':
            self.stop_speech()
            self.update_event_label("stop reading")
        elif cmd and cmd == 'store':
            if self.transcription_text.text:
                self.add_lookup(self.transcription_text.text, self.translation_label.text)
                self.update_event_label(f'{self.transcription_text.text} saved')
        elif cmd and cmd == 'search':
            transcription = self.transcription_text.text
            self.update_translation_label("")
            self.lookup(transcription)
        elif self.tts.speeking():
            print(f"recognized {text} when speaking")
            self.update_event_label("ignore recognition while reading")
        else:
            self.update_transcription_text(text)
            self.update_translation_label("")
            self.update_event_label(f"{text} recognized")

    def __start_listening_callback(self):
        self.update_status_label('listening...')

    def __stop_listening_callback(self):
        self.update_status_label('listening stopped')
        self.update_event_label('listening stopped')

    def __error_listening_callback(self, error_message):
        self.update_status_label('listening error')
        self.update_event_label(f'listening error: {error_message}')

    def get_translation(self, input_string):
        try:
            data = json.loads(self.llm_helper.get_translation(input_string))
            return '\n'.join([f"{key}: {value}" for key, value in data.items()])
        except Exception as ex:
            print(f"{ex}")
            self.update_event_label(f"{ex}")
            return ""

    def get_question_about(self, input_string):
        try:
            q = self.llm_helper.get_question_about(input_string)
            return q
        except Exception as ex:
            print(f"{ex}")
            self.update_event_label(f"{ex}")
            return ""
    
    def text_to_speech(self, text):
        self.tts.speak(text)  # Pass None for utteranceId if not needed

    def stop_speech(self):
        self.tts.stop()

    def get_lookups(self):
        return self.app_storage.get_all_lookups()

    def lookup(self, text):
        if self.lookup_started:
            self.update_event_label("lookup running")
            return
        
        self.lookup_started = True
        def translate():
            if text:
                translation = self.get_translation(text)
                if translation:
                    self.update_translation_label(translation)
                    self.update_event_label(f'{text} looked up')
            self.lookup_started = False
        self.update_translation_label("")
        self.update_event_label(f'translate {text}')
        threading.Thread(target=translate).start()

    def get_statistics(self):
        return self.app_storage.get_statistics()

    def get_review_lookups(self):
        return self.app_storage.get_review_lookups()

    def add_lookup(self, lookup, response):
        self.app_storage.add_lookup(lookup, response)

    def reinforce_result(self, lookup, success):
        self.app_storage.reinforce_result(lookup, success)

    def delete_lookup(self, lookup):
        self.app_storage.delete_lookup(lookup)

    def clear_lookups(self):
        self.app_storage.cleanup()

    def popup(self, title, msg, size_hint=(1, 1)):
        popup = Popup(title=title, content=Label(text=msg, halign='left', valign='top'), auto_dismiss=False, size_hint=size_hint)
        popup.content.bind(on_touch_down=lambda instance, touch: popup.dismiss())
        popup.open()

    def build(self):
        layout = FloatLayout()  # Use FloatLayout for precise positioning

        # Create a transcription label that takes 10% of the height
        self.transcription_text = TextInput(
            text='',
            size_hint=(1, 0.05),  # Takes 10% of the height
            pos_hint={'x': 0, 'y': 0.9},  # Positioned at the top
            multiline=True,
            keyboard_mode='auto',
            font_name='NotoSansCJK'
        )
        layout.add_widget(self.transcription_text)

        # Create a translation label that takes 70% of the height
        self.translation_label = Label(
            text='',
            size_hint=(1, 0.7),  # Takes 70% of the height
            pos_hint={'x': 0, 'y': 0.2},  # Positioned below the transcription label
            halign='left',  # Align text to the left
            valign='top',   # Align text to the top
            font_name='NotoSansCJK'  # Set the font to NotoSans for Chinese support
        )
        self.translation_label.bind(size=self.translation_label.setter('text_size'))  # Allow text wrapping
        self.translation_label.text_size = (self.translation_label.width, None)  # Set text size for wrapping
        layout.add_widget(self.translation_label)

        # Create buttons with height set to 1/10 of the window height
        start_button = Button(text='Start Listen', size_hint=(0.2, 0.05), pos_hint={'x': 0, 'y': 0.15})
        start_button.bind(on_press=self.on_start_listening)
        layout.add_widget(start_button)

        stop_button = Button(text='Stop Listen', size_hint=(0.2, 0.05), pos_hint={'x': 0.2, 'y': 0.15})
        stop_button.bind(on_press=self.on_stop_listening)
        layout.add_widget(stop_button)

        stopspeech_button = Button(text='Quiet', size_hint=(0.2, 0.05), pos_hint={'x': 0.4, 'y': 0.15})
        stopspeech_button.bind(on_press=self.on_stop_speech)
        layout.add_widget(stopspeech_button)

        statistics_button = Button(text='Read', size_hint=(0.2, 0.05), pos_hint={'x': 0.6, 'y': 0.15})
        statistics_button.bind(on_press=self.on_read)
        layout.add_widget(statistics_button)

        settings_button = Button(text='Settings', size_hint=(0.2, 0.05), pos_hint={'x': 0.8, 'y': 0.15})
        settings_button.bind(on_press=self.on_settings)
        layout.add_widget(settings_button)

        # Create a save button with height set to 1/10 of the window height
        save_button = Button(text='Save', size_hint=(0.20, 0.05), pos_hint={'x': 0, 'y': 0.1})
        save_button.bind(on_press=self.on_save)
        layout.add_widget(save_button)

        lookup_button = Button(text='Lookup', size_hint=(0.20, 0.05), pos_hint={'x': 0.20, 'y': 0.1})
        lookup_button.bind(on_press=self.on_lookup)
        layout.add_widget(lookup_button)

        list_button = Button(text='List', size_hint=(0.20, 0.05), pos_hint={'x': 0.4, 'y': 0.1})
        list_button.bind(on_press=self.on_list)
        layout.add_widget(list_button)

        clear_button = Button(text='Clear', size_hint=(0.20, 0.05), pos_hint={'x': 0.6, 'y': 0.1})
        clear_button.bind(on_press=self.on_clear)
        layout.add_widget(clear_button)

        test_button = Button(text='Test', size_hint=(0.20, 0.05), pos_hint={'x': 0.8, 'y': 0.1})
        test_button.bind(on_press=self.on_test)
        layout.add_widget(test_button)

        # Create a status label with height of 1/10 of the window height
        self.status_label = Label(text='Status: Ready', size_hint=(0.5, 0.05), pos_hint={'x': 0.5, 'y': 0.05}, font_name='NotoSansCJK')  # 10% height
        layout.add_widget(self.status_label)

        # Create a label to display the current language with height of 1/10 of the window height
        self.language_label = Label(text=f'Language: {self.speech_recognizer.language}', size_hint=(0.5, 0.05), pos_hint={'x': 0, 'y': 0.05}, font_name='NotoSansCJK')  # 10% height
        layout.add_widget(self.language_label)

        # Create a label to display the current events with height of 1/10 of the window height
        self.event_label = Label(text='Events: None', size_hint=(1, 0.05), pos_hint={'x': 0, 'y': 0}, font_name='NotoSansCJK')  # 10% height
        layout.add_widget(self.event_label)
        
        return layout

    def on_save(self, instance):
        save_text = self.transcription_text.text
        if save_text:
            self.add_lookup(self.transcription_text.text, self.translation_label.text)
            self.update_event_label(f'{save_text} saved')

    def on_lookup(self, instance):
        # when on_lookup is called in kivy event thread
        # schedule translate method in another thread
        # to avoid blocking event dispatching
        self.update_translation_label("")

        self.lookup(self.transcription_text.text)


    def on_list(self, instance):
        popup = ListPopup(title='Lookups')
        self.update_event_label('lookups listed')
        popup.open()

    def on_clear(self, instance):
        self.clear_lookups()
        self.update_event_label('lookups cleared')

    def on_test(self, instance):
        self.update_event_label('test')
        test_lookups = self.get_review_lookups()
        test_popup = TestPopup(test_lookups)
        test_popup.open()        

    def on_stop_speech(self, instance):
        self.stop_speech()
        self.update_event_label('speech stopped')
    
    def on_start_listening(self, instance):
        self.listening_started = True
        self.speech_recognizer.start_listening()
        self.update_event_label('listening started')

    def on_stop_listening(self, instance):
        self.listening_started = False
        self.speech_recognizer.stop_listening()
        self.update_event_label('listening stopped')

    def on_read(self, instance):
        self.text_to_speech(f"{self.transcription_text.text} {self.translation_label.text}")
        self.update_event_label("reading")

    def on_settings(self, instance):
        popup = SettingPopup()
        popup.open()
        self.update_event_label('settings')
    
    def on_pause(self):
        print("app pause")
        self.update_event_label("app paused")
        self.tts.stop()
        if self.listening_started:
            self.speech_recognizer.stop_listening()
        return True

    def on_resume(self):
        print("app resume")
        self.update_event_label("app resumed")
        if self.listening_started:
            self.speech_recognizer.start_listening()


if __name__ == '__main__':
    VocabularyAssistantApp().run()