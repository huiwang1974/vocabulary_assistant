from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle, StencilPush, StencilUse, StencilPop
from kivy.core.text import Label as CoreLabel
from kivy.metrics import dp
from lookuppopup import LookupPopup

class TableWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row_height = 50
        self.col_width = 250
        self.font_size = 20
        self.touch_start_pos = None  # Store the starting position of touch
        self.refresh_lookups()

    def refresh_lookups(self):
        self.data_array = App.get_running_app().get_lookups()
        self.size = (self.col_width * 6, self.row_height * (1 if not self.data_array else 1 + len(self.data_array)))
        self.update_canvas()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):  # Ensure touch starts inside the widget
            self.touch_start_pos = touch.pos  # Store start position
            return True  # Consume the event
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.touch_start_pos:
            # Calculate movement distance
            dx = abs(touch.pos[0] - self.touch_start_pos[0])
            dy = abs(touch.pos[1] - self.touch_start_pos[1])
            movement_threshold = dp(5)  # Ignore if user moved more than 5 dp

            if dx < movement_threshold and dy < movement_threshold:
                local_x, local_y = touch.pos
                if local_y < self.height - self.row_height:
                    row = int((self.height - 1 - local_y) / self.row_height) - 1
                    print(f"Tapped at: {local_x}, {local_y} (relative to InnerWidget), row: {row}")
                    print(f"touch: {touch}")
                    print(f"local_x: {local_x}, local_y: {local_y}")
                    print(f"height: {self.height}, row_height: {self.row_height}")
                    print(f"data_array: {len(self.data_array)}")
                    lookup, lookup_response, lookup_time, success_reinforces, last_reinforce_time, review_due_time = self.data_array[row]
                    print(f"Lookup: {lookup}, Lookup response: {lookup_response}, Lookup time: {lookup_time}, Success reinforces: {success_reinforces}, Last reinforce time: {last_reinforce_time}, Review due time: {review_due_time}")
                    popup = LookupPopup(
                                lookup,
                                lookup_response,
                                lookup_time,
                                success_reinforces,
                                last_reinforce_time, 
                                review_due_time,
                                size_hint=(0.9, 0.9)
                            )
                    popup.bind(on_dismiss=self.on_popup_dismiss)
                    popup.open()  # Open the popup
                    
            # Reset touch start position to avoid issues with multiple taps
            self.touch_start_pos = None
            return True  # Consume the event
        return super().on_touch_up(touch)
    
    def on_popup_dismiss(self, instance):
        self.refresh_lookups()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            print(self.pos, self.size)
            Rectangle(pos=self.pos, size=self.size)
            Color(0, 0, 0, 1)
            
            # Draw table header
            Line(points=[0, self.height - self.row_height, self.width, self.height - self.row_height], width=1)
            self.draw_text('Lookup', 0, self.height - self.row_height, font_name='NotoSansCJK-Bold')
            Line(points=[self.col_width, 0, self.col_width, self.height], width=1)
            self.draw_text('Success tests', self.col_width, self.height - self.row_height, font_name='NotoSansCJK-Bold')
            Line(points=[self.col_width*2, 0, self.col_width*2, self.height], width=1)
            self.draw_text('Last test time', self.col_width*2 , self.height - self.row_height, font_name='NotoSansCJK-Bold')
            Line(points=[self.col_width*3, 0, self.col_width*3, self.height], width=1)
            self.draw_text('Review due time', self.col_width*3, self.height - self.row_height, font_name='NotoSansCJK-Bold')
            Line(points=[self.col_width*4, 0, self.col_width*4, self.height], width=1)
            self.draw_text('Lookup time', self.col_width*4, self.height - self.row_height, font_name='NotoSansCJK-Bold')
            Line(points=[self.col_width*5, 0, self.col_width*5, self.height], width=1)
            self.draw_text('Lookup response', self.col_width*5, self.height - self.row_height, font_name='NotoSansCJK-Bold')
            
            # Draw table content
            for i, (lookup, lookup_response, lookup_time, success_reinforces, last_reinforce_time, review_due_time) in enumerate(self.data_array):
                y_pos = self.height - (i + 2) * self.row_height
                Line(points=[0, y_pos, self.width, y_pos], width=1)
                self.draw_text(str(lookup), 0, y_pos)
                self.draw_text(str(success_reinforces), self.col_width, y_pos)
                self.draw_text(str(last_reinforce_time), self.col_width*2, y_pos)
                self.draw_text(str(review_due_time), self.col_width*3, y_pos)
                self.draw_text(str(lookup_time), self.col_width*4, y_pos)
                self.draw_text(str(lookup_response)[:20], self.col_width*5, y_pos)

    def draw_text(self, text, x, y, font_name='NotoSansCJK'):
        """Draws text on the canvas at a specific position using CoreLabel."""
        text = text.replace('\n', ' ')
        label = CoreLabel(text=text, font_size=self.font_size, font_name=font_name)
        label.refresh()
        text_texture = label.texture
        text_size = label.texture.size
        print(f"text_size: {text_size}, text: {text}, x: {x}, y: {y}, label.size: {label.size}")
        with self.canvas:
            StencilPush()
            x_margin = 5
            y_margin = 5
            Rectangle(pos=(x+x_margin, y+y_margin), size=(self.col_width-x_margin*2, self.row_height-y_margin*2))
            StencilUse()
            Rectangle(texture=text_texture, pos=(x+x_margin, y+y_margin), size=text_size)
            StencilPop()

class ListPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.table = TableWidget(size_hint=(None, None))
        main_window = App.get_running_app().root
        self.scroll_view = ScrollView(size_hint=(None, None), size=(main_window.width*0.8, main_window.height*0.76), do_scroll_x=True, do_scroll_y=True)
        self.scroll_view.add_widget(self.table)
        print(self.width, self.height)
        print(self.size)
        print(self.scroll_view.size)
        self.close_button = Button(text='Close', size_hint=(None, None), size=(100, 50))
        
        self.popup_layout.add_widget(self.scroll_view)
        self.popup_layout.add_widget(self.close_button)
        
        self.content = self.popup_layout
        self.close_button.bind(on_press=self.close_popup)
    
    def close_popup(self, instance):
        self.dismiss()
