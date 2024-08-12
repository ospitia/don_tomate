from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from pathlib import Path


TIME = 1 * 5
base_path = Path(__file__).parent / 'don_tomate' / 'Resources'

SOUND_PATH = str(base_path / 'notification.wav')
PLAY = str(base_path / 'play.png')
RESET = str(base_path / 'reset.png')
SOUND = str(base_path / 'sound.png')
PAUSE = str(base_path / 'pause.png')
STOP_SOUND = str(base_path / 'stop_sound.png')
ICON = str(base_path / 'don_tomate.png')

# default window size
Window.size = (400, 300)


class DonTomateApp(App):
    def build(self):
        self.time = TIME
        self.running = False
        self.clock_event = None
        self.sound = None
        self.mute = None
        self.icon = ICON

        # Main Layout
        main_layout = FloatLayout()

        # background color (white or light color)
        main_layout.canvas.before.clear()
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light pastel gray
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Timer display
        self.label = Label(text=self.format_time(self.time), font_size='40sp', size_hint=(0.6, None), height=50,
                           color=(0, 0, 0, 1))
        self.label.pos_hint = {'center_x': 0.5, 'center_y': 0.7}

        # Control buttons with icons
        self.start_stop_button = Button(background_normal=PLAY, on_press=self.start_stop, size_hint=(None, None),
                                        size=(100, 100))
        self.reset_button = Button(background_normal=RESET, on_press=self.reset_timer, size_hint=(None, None),
                                   size=(100, 100))
        self.stop_sound_button = Button(background_normal=SOUND, on_press=self.stop_sound, size_hint=(None, None),
                                        size=(100, 100), disabled=True, disabled_color=(0.95, 0.95, 0.95, 1),
                                        color=(0.95, 0.95, 0.95, 1), opacity=0)

        # Layout for buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(300, 50), spacing=10)
        button_layout.add_widget(self.start_stop_button)
        button_layout.add_widget(self.reset_button)
        button_layout.add_widget(self.stop_sound_button)
        button_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Centering the button layout

        # Add widgets to the main layout
        main_layout.add_widget(self.label)
        main_layout.add_widget(button_layout)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f'{minutes:02}:{seconds:02}'

    def start_stop(self, instance):
        if self.running:
            self.running = False
            self.start_stop_button.background_normal = PLAY
            if self.clock_event:
                self.clock_event.cancel()
                self.clock_event = None
        else:
            self.running = True
            self.start_stop_button.background_normal = PAUSE
            if self.sound or self.mute:
                self.running = False
                if self.clock_event:
                    self.clock_event.cancel()
                    self.clock_event = None
                self.time = TIME
                self.label.text = self.format_time(self.time)
                self.start_stop_button.background_normal = PLAY
                self.stop_sound(None)
                self.mute = None
                self.stop_sound_button.disabled = True
                self.stop_sound_button.opacity = 0
                self.stop_sound_button.background_normal = SOUND
            else:
                self.clock_event = Clock.schedule_interval(self.update_time, 1)

    def reset_timer(self, instance):
        self.running = False
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None
        self.time = TIME
        self.label.text = self.format_time(self.time)
        self.start_stop_button.background_normal = PLAY
        self.stop_sound(None)
        self.mute = None
        self.stop_sound_button.disabled = True
        self.stop_sound_button.opacity = 0
        self.stop_sound_button.background_normal = SOUND

    def update_time(self, dt):
        if self.running:
            if self.time > 0:
                self.time -= 1
                self.label.text = self.format_time(self.time)
            else:
                self.running = False
                self.label.text = "Time's up!"
                self.notify_time()

    def notify_time(self):
        self.sound = SoundLoader.load(SOUND_PATH)
        if self.sound:
            self.sound.play()
            self.stop_sound_button.disabled = False
            self.stop_sound_button.opacity = 1
        else:
            print("Sound file not found!")

    def stop_sound(self, instance):
        if self.sound:
            self.sound.stop()
            self.mute = True
        if self.mute:
            self.stop_sound_button.background_normal = STOP_SOUND
            self.sound = None
        else:
            self.stop_sound_button.disabled = True


if __name__ == '__main__':
    DonTomateApp().run()
