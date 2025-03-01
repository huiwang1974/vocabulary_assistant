import json
import threading
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class TestPopup(Popup):
    def __init__(self, lookups, **kwargs):
        super(TestPopup, self).__init__(**kwargs)
        self.showing_question = False
        self.title = "Test Popup"
        self.size_hint = (0.9, 0.8)  # Width 90% and height 80% of the window
        self.lookups = lookups
        self.current_lookup_idx = 0
        # Create a layout for the popup
        layout = FloatLayout()

        # Create a label with text wrapping
        self.label = Label(
            text='',
            size_hint=(1, 0.8),  # Width will be 90% of the popup width
            pos_hint={'x': 0, 'y': 0.2},
            halign='left',  # Align text to the right
            valign='top',  # Align text to the top
            font_name='NotoSansCJK'
        )
        self.label.bind(size=self.label.setter('text_size'))  # Allow text wrapping
        self.label.text_size = (self.label.width, None)  # Set text size for wrapping

        layout.add_widget(self.label)

        # Create a text input box
        self.text_input = TextInput(size_hint=(1, 0.05), pos_hint={'x': 0, 'y': 0.10})
        layout.add_widget(self.text_input)

        # Create a button
        button = Button(text='Submit', size_hint=(0.5, 0.05), pos_hint={'x': 0, 'y': 0.025})
        button.bind(on_release=self.on_button_click)
        layout.add_widget(button)

        close_button = Button(text='Close', size_hint=(0.25, 0.05), pos_hint={'x': 0.5, 'y': 0.025})
        close_button.bind(on_release=self.on_close_click)
        layout.add_widget(close_button)

        next_button = Button(text='Next', size_hint=(0.25, 0.05), pos_hint={'x': 0.75, 'y': 0.025})
        next_button.bind(on_release=self.on_next_click)
        layout.add_widget(next_button)

        self.content = layout  # Set the layout as the content of the popup
        self.show_question()

    @mainthread
    def update_label(self, question, answer):
        self.label.text = question
        self.text_input.text = answer

    def show_question(self):
        if self.showing_question:
            self.update_label("showing question", "")
            return
        self.showing_question = True
        def show():
            if self.lookups:
                lookup = self.lookups[self.current_lookup_idx][0]
                lookup_response = self.lookups[self.current_lookup_idx][1]
                question = App.get_running_app().get_question_about(f"{lookup} {lookup_response}")
                if question:
                    data = json.loads(question)
                    self.question = data['question'] + '\n' + '\n'.join([f"{k}: {v}" for k, v in data['options'].items()])
                    self.answer = data['answer']
                    self.lookup = lookup
                    self.update_label(self.question, '')
                else:
                    self.update_label('Error getting questions', '')
            else:
                self.update_label('No lookup due for review.', '')        
            self.showing_question = False
        threading.Thread(target=show).start()

    def on_close_click(self, instance):
        self.dismiss()  # Close the popup

    def on_next_click(self, instance):
        if self.lookups:
            self.current_lookup_idx = (self.current_lookup_idx + 1) % len(self.lookups)
        self.show_question()

    def on_button_click(self, instance):
        # Print a message and close the popup
        print("Button clicked! Text input:", self.text_input.text)
        if self.text_input.text.strip().lower() == self.answer.strip().lower():
            App.get_running_app().reinforce_result(self.lookup, True)
            App.get_running_app().popup(title="Result", msg="Correct!", size_hint=(0.5, 0.5))
        else:
            App.get_running_app().reinforce_result(self.lookup, False)
            App.get_running_app().popup(title="Result", msg="Incorrect!", size_hint=(0.5, 0.5))
        