from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class LookupPopup(Popup):
    def __init__(self, lookup, lookup_response, lookup_time, success_reinforces, last_reinforce_time, review_due_time, **kwargs):
        super(LookupPopup, self).__init__(**kwargs)
        self.title = "Lookup Popup"
        self.lookup = lookup
        self.lookup_response = lookup_response
        self.lookup_time = lookup_time
        self.success_reinforces = success_reinforces
        self.last_reinforce_time = last_reinforce_time
        self.review_due_time = review_due_time

        # Create a vertical layout for the labels
        label_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=10, spacing=10)

        # Create and add labels for each parameter
        self.lookup_label = self.create_label(f"Lookup: {lookup}", (1, 0.05))
        label_layout.add_widget(self.lookup_label)
        self.lookup_time_label = self.create_label(f"Lookup time: {lookup_time}", (1, 0.05))
        label_layout.add_widget(self.lookup_time_label)
        self.success_reinforces_label = self.create_label(f"Success reinforces: {success_reinforces}", (1, 0.05))
        label_layout.add_widget(self.success_reinforces_label)
        self.last_reinforce_time_label = self.create_label(f"Last reinforce time: {last_reinforce_time}", (1, 0.05))
        label_layout.add_widget(self.last_reinforce_time_label)
        self.review_due_time_label = self.create_label(f"Review due time: {review_due_time}", (1, 0.05))
        label_layout.add_widget(self.review_due_time_label)
        self.lookup_response_label = self.create_label(f"Lookup response: {lookup_response}", (1, 0.75))
        label_layout.add_widget(self.lookup_response_label)

        # Create a horizontal layout for the buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        # Create buttons
        close_button = Button(text='Close', size_hint=(0.25, 0.5))
        read_button = Button(text='Read', size_hint=(0.25, 0.5))
        stop_read_button = Button(text='Quiet', size_hint=(0.25, 0.5))
        delete_button = Button(text='Delete', size_hint=(0.25, 0.5))

        # Bind button actions
        close_button.bind(on_release=self.dismiss)  # Close the popup
        read_button.bind(on_release=self.read_action)  # Placeholder for read action
        stop_read_button.bind(on_release=self.stop_read_action)  # Placeholder for stop read action
        delete_button.bind(on_release=self.delete_action)  # Placeholder for delete action

        # Add buttons to the button layout
        button_layout.add_widget(close_button)
        button_layout.add_widget(read_button)
        button_layout.add_widget(stop_read_button)
        button_layout.add_widget(delete_button)

        # Create the main layout and add the label and button layouts
        main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        main_layout.add_widget(label_layout)
        main_layout.add_widget(button_layout)

        self.content = main_layout  # Set the content of the popup

    def create_label(self, text, size_hint):
        label = Label(text=text, halign='left', valign='top', size_hint=size_hint, font_name='NotoSansCJK')
        label.bind(size=label.setter('text_size'))  # Allow text wrapping
        label.text_size = (label.width, None)  # Set text size for wrapping
        return label
    
    def delete_action(self, instance):
        print("Delete action triggered")  # Placeholder for delete action
        App.get_running_app().delete_lookup(self.lookup)
        self.dismiss()

    def read_action(self, instance):
        print("Read action triggered")  # Placeholder for read action
        App.get_running_app().text_to_speech(self.lookup_response)

    def stop_read_action(self, instance):
        print("Stop read action triggered")  # Placeholder for stop read action
        App.get_running_app().stop_speech()
