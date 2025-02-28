import environment as env
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class SettingPopup(Popup):
    def __init__(self, **kwargs):
        super(SettingPopup, self).__init__(**kwargs)
        self.title = "Settings"
        self.size_hint = (0.8, 0.8)  # Set the size of the popup

        # Create a vertical layout for the popup
        layout = FloatLayout(size_hint = (1, 1))

        # Create the first label and text input for OpenAI API Key
        self.label_api_key = Label(text="OpenAI API Key:", valign='top', halign='left', size_hint = (1, 0.035), pos_hint = {'x': 0, 'y': 0.95}, text_size=(None,None))
        self.label_api_key.bind(size=self.label_api_key.setter('text_size')) 
        self.text_input_api_key = TextInput(size_hint = (1, 0.15), pos_hint = {'x': 0, 'y': 0.8})
        layout.add_widget(self.label_api_key)
        layout.add_widget(self.text_input_api_key)

        # Create the second label and text input for OpenAI Org ID
        self.label_org_id = Label(text="OpenAI Org ID:", valign='top', halign='left', size_hint = (1, 0.035), pos_hint = {'x': 0, 'y': 0.75}, text_size=(None,None))
        self.label_org_id.bind(size=self.label_org_id.setter('text_size')) 
        self.text_input_org_id = TextInput(size_hint = (1, 0.15), pos_hint = {'x': 0, 'y': 0.6})
        layout.add_widget(self.label_org_id)
        layout.add_widget(self.text_input_org_id)

        # Create the third label and text input for Learning Curve Min Interval
        self.label_min_interval = Label(text="Learn Curve Min Intvl:", valign='top', halign='left', size_hint = (1, 0.035), pos_hint = {'x': 0, 'y': 0.55}, text_size=(None,None))
        self.label_min_interval.bind(size=self.label_min_interval.setter('text_size')) 
        self.text_input_min_interval = TextInput(size_hint = (1, 0.15), pos_hint = {'x': 0, 'y': 0.4})
        layout.add_widget(self.label_min_interval)
        layout.add_widget(self.text_input_min_interval)

        # Create the fourth label and text input for Learning Curve Max Interval
        self.label_max_interval = Label(text="Learn Curve Max Intvl:", valign='top', halign='left', size_hint = (1, 0.035), pos_hint = {'x': 0, 'y': 0.35}, text_size=(None,None))
        self.label_max_interval.bind(size=self.label_max_interval.setter('text_size')) 
        self.text_input_max_interval = TextInput(size_hint = (1, 0.15), pos_hint = {'x': 0, 'y': 0.2})
        layout.add_widget(self.label_max_interval)
        layout.add_widget(self.text_input_max_interval)

        # Create a horizontal layout for the buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint = (1, 0.1), pos_hint = {'x': 0, 'y': 0}, spacing=10)

        # Create Apply button
        apply_button = Button(text='Apply', size_hint = (0.5, 0.5), pos_hint = {'x': 0, 'y': 0.25})
        apply_button.bind(on_release=self.on_apply)

        # Create Cancel button
        cancel_button = Button(text='Cancel', size_hint = (0.5, 0.5), pos_hint = {'x': 0.5, 'y': 0.25})
        cancel_button.bind(on_release=self.dismiss)  # Close the popup

        # Add buttons to the button layout
        button_layout.add_widget(apply_button)
        button_layout.add_widget(cancel_button)

        # Add the button layout to the main layout
        layout.add_widget(button_layout)

        self.content = layout  # Set the layout as the content of the popup
        
        self.update_ui()

    def update_ui(self):
        self.text_input_api_key.text = env.get_openai_api_key()
        self.text_input_org_id.text = env.get_openai_organization_id()
        self.text_input_min_interval.text = str(env.get_learning_curve_basetime())
        self.text_input_max_interval.text = str(env.get_learning_curve_maxtime())

    def on_apply(self, instance):
        # Handle the apply action (e.g., print the values)
        print("OpenAI API Key:", self.text_input_api_key.text)
        print("OpenAI Org ID:", self.text_input_org_id.text)
        print("Learning Curve Min Interval:", self.text_input_min_interval.text)
        print("Learning Curve Max Interval:", self.text_input_max_interval.text)
        env.set_openai_api_key(self.text_input_api_key.text)
        env.set_openai_organization_id(self.text_input_org_id.text)
        env.set_learning_curve_basetime(float(self.text_input_min_interval.text))
        env.set_learning_curve_maxtime(float(self.text_input_max_interval.text))
        env.store_settings()
        self.dismiss()  # Close the popup after applying settings
