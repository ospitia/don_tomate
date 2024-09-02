from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from pathlib import Path
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import Screen
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
import platform
import objc
from Quartz import kCGStatusWindowLevel, kCGNormalWindowLevel

base_path = Path(__file__).parent / "don_tomate" / "Resources"

SOUND_PATH = str(base_path / "notification.wav")
PLAY = str(base_path / "play.png")
RESET = str(base_path / "reset.png")
SOUND = str(base_path / "sound.png")
PAUSE = str(base_path / "pause.png")
STOP_SOUND = str(base_path / "stop_sound.png")
SETTINGS = str(base_path / "settings.png")
ICON = str(base_path / "don_tomate.png")
NEXT = str(base_path / "next.png")
PREV = str(base_path / "prev.png")
STATUS_MENU_ICON = str(base_path / "status_menu_icon.png")

# Default window size
Window.size = (500, 300)


class ColoredBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ColoredBoxLayout, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MainScreen(Screen):
    """
    The main screen for the Pomodoro timer application.

    Attributes:
        duration (int): Duration of the timer in seconds.
        time (int): Current remaining time of the timer in seconds.
        running (bool): Indicates if the timer is currently running.
        clock_event (ClockEvent): The clock event for the timer update.
        sound (Sound): The sound to play when the timer finishes.
        mute (bool): Indicates if the sound is muted.
    """

    def __init__(
        self,
        screen="Pomodoro 1",
        duration=(5 * 1),
        dir_left_button_opacity=0,
        dir_left_button_disabled=True,
        previous_screen_name=None,
        next_screen_name="break",
        **kwargs,
    ):
        """
        gets the MainScreen started with UI components and timer settings.

        Args:
            screen (str): The name of the screen (e.g., "Pomodoro 1").
            duration (int): Duration of the timer in seconds.
            dir_left_button_opacity (float): Opacity of the left direction button.
            dir_left_button_disabled (bool): Indicates if the left direction button is disabled.
            previous_screen_name (str): Name of the previous screen.
            next_screen_name (str): Name of the next screen.
        """
        super(MainScreen, self).__init__(**kwargs)
        self.duration = duration
        self.time = self.duration

        self.running = False
        self.clock_event = None
        self.sound = None
        self.mute = None
        self.previous_screen_name = previous_screen_name
        self.next_screen_name = next_screen_name

        # Main Layout
        main_layout = BoxLayout(orientation="vertical", padding=2, spacing=20)

        # Background color (white or light color)
        main_layout.canvas.before.clear()
        with main_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light pastel gray
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Timer display
        self.label_name = Label(text=screen, font_size="30sp", color=(0, 0, 0, 1))

        # Timer display
        self.label = Label(text=self.format_time(self.time), font_size="40sp", color=(0, 0, 0, 1))

        # Control buttons with icons
        self.start_stop_button = Button(
            background_normal=PLAY,
            on_press=self.start_stop,
        )

        # Settings button
        self.settings_button = Button(background_normal=SETTINGS, on_press=self.open_settings)

        # Sound/Stop Sound button
        self.stop_sound_button = Button(
            background_normal=SOUND,
            on_press=self.stop_sound,
            disabled=True,
            disabled_color=(0.95, 0.95, 0.95, 1),
            color=(0.95, 0.95, 0.95, 1),
            opacity=0,
        )

        # Reset button
        self.reset_button = Button(
            background_normal=RESET,
            on_press=self.reset_timer,
        )

        # next button
        self.right_screen_button = Button(
            background_normal=NEXT,
            on_press=self.next_screen,
        )

        self.left_screen_button = Button(
            background_normal=PREV,
            on_press=self.previous_screen,
            disabled=True,
        )
        self.left_screen_button.opacity = dir_left_button_opacity
        self.left_screen_button.disabled = dir_left_button_disabled

        # Layout for top-right buttons
        top_buttons_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=0.1,
            top=True,
        )

        top_right_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            height=80,
            width=240,
            pos_hint={"right": 1, "top": 1},
        )
        empty_box = BoxLayout(orientation="horizontal", size_hint_x=0.7)
        top_right_layout.add_widget(self.stop_sound_button)
        top_right_layout.add_widget(self.reset_button)
        top_right_layout.add_widget(self.settings_button)
        top_buttons_layout.add_widget(empty_box)
        top_buttons_layout.add_widget(top_right_layout)

        HB = BoxLayout(orientation="horizontal", size_hint_y=0.7, spacing=10)

        main_screen_place_holder = BoxLayout(orientation="vertical", size_hint_x=0.8, spacing=10)
        empty_lower_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.15,
        )
        empty_upper_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.1,
        )

        name_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.25,
        )
        time_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.25,
        )
        controls_box = BoxLayout(orientation="horizontal", size_hint_y=0.25, spacing=5)

        name_box.add_widget(self.label_name)
        time_box.add_widget(self.label)

        controls_empty_right_box = BoxLayout(
            orientation="horizontal",
            size_hint_x=0.45,
        )
        control_button_box = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center": 1},
        )
        control_button_box.add_widget(self.start_stop_button)
        controls_empty_left_box = BoxLayout(
            orientation="horizontal",
            size_hint_x=0.45,
        )
        controls_box.add_widget(controls_empty_right_box)
        controls_box.add_widget(control_button_box)
        controls_box.add_widget(controls_empty_left_box)

        main_screen_place_holder.add_widget(name_box)
        main_screen_place_holder.add_widget(time_box)
        main_screen_place_holder.add_widget(empty_upper_box)
        main_screen_place_holder.add_widget(controls_box)
        main_screen_place_holder.add_widget(empty_lower_box)

        self.left_button_placeholder = BoxLayout(
            orientation="vertical", size_hint_x=0.15, spacing=10
        )
        self.left_upper_empty_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.37,
        )
        self.left_lower_empty_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.37,
        )
        self.left_direction_button_placeholder = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(100, 100),
        )
        self.left_button_placeholder.add_widget(self.left_upper_empty_box)
        self.left_direction_button_placeholder.add_widget(self.left_screen_button)
        self.left_button_placeholder.add_widget(self.left_direction_button_placeholder)
        self.left_button_placeholder.add_widget(self.left_lower_empty_box)

        self.right_button_placeholder = BoxLayout(
            orientation="vertical", size_hint_x=0.15, spacing=10
        )
        self.upper_empty_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.37,
        )
        self.lower_empty_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.37,
        )
        self.direction_button_placeholder = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"right": 1},
        )
        self.right_button_placeholder.add_widget(self.upper_empty_box)
        self.direction_button_placeholder.add_widget(self.right_screen_button)
        self.right_button_placeholder.add_widget(self.direction_button_placeholder)
        self.right_button_placeholder.add_widget(self.lower_empty_box)

        HB.add_widget(self.left_button_placeholder)

        HB.add_widget(main_screen_place_holder)
        HB.add_widget(self.right_button_placeholder)
        main_layout.add_widget(top_buttons_layout)
        main_layout.add_widget(HB)

        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        """
        Updates the background rectangle size and position based on the layout.

        Args:
            instance: The instance of the widget calling this method.
            value: The new value for size or position.
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def format_time(self, seconds):
        """
        Formats the given time in seconds to a string in the format MM:SS.

        Args:
            seconds (int): The time in seconds.

        Returns:
            str: The formatted time string.
        """
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def start_stop(self, instance):
        """
        Starts or stops the timer when the start/stop button is pressed.

        Args:
            instance: The button instance that triggered this method.
        """
        app = App.get_running_app()

        if self.running:
            self.running = False
            self.start_stop_button.background_normal = PLAY
            if self.clock_event:
                self.clock_event.cancel()
                self.clock_event = None
            app.current_timer = None  # Clear the current timer
        else:
            # check if the previous timer is not finished yet
            current_screen_pos = app.screens.index(self.name)
            if current_screen_pos == 0 and (sum(app.timers_status.values()) == 0):
                pass
            elif app.current_timer == self and app.timers_status.get(
                app.screens[current_screen_pos]
            ):
                pass
            elif app.timers_status.get(app.screens[current_screen_pos - 1]):
                pass
            else:
                return

            self.running = True
            app.current_timer = self  # Set the current timer to this one
            self.start_stop_button.background_normal = PAUSE
            if self.sound or self.mute:
                self.soft_reset(None)
            else:
                self.clock_event = Clock.schedule_interval(self.update_time, 1)

    def reset_timer(self, instance):
        """
        Resets the timer to its initial duration and stops any running clock events.

        Args:
            instance: The button instance that triggered this method.
        """
        self.soft_reset(None, reset=True)
        app = App.get_running_app()
        app.current_timer = None  # Clear the current timer

    def soft_reset(self, instance, **kwargs):
        """
        Soft resets the timer without clearing the current timer. Stops sound and updates the UI.

        Args:
            instance: The button instance that triggered this method.
            **kwargs: Additional keyword arguments.
        """
        self.running = False
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None
        self.time = self.duration
        self.label.text = self.format_time(self.time)
        self.start_stop_button.background_normal = PLAY
        if not kwargs.get("reset") or self.sound:
            self.stop_sound(None)
            # self.mute = True if kwargs.get("inactive_stop") else None
            app = App.get_running_app()
            if sum(app.timers_status.values()) == len(app.screens):
                app.rebuild_screens(app.n_pomodoros)
        self.stop_sound_button.disabled = True
        self.stop_sound_button.opacity = 0
        self.stop_sound_button.background_normal = SOUND

    def update_time(self, dt):
        """
        Updates the timer every second. Stops the timer when time is up.

        Args:
            dt (float): The time delta since the last update.
        """
        if self.running:
            if self.time > 0:
                self.time -= 1
                self.label.text = self.format_time(self.time)
            else:
                self.running = False
                self.label.text = "Time's up!"
                self.notify_time()
                self.sound.bind(
                    on_stop=lambda instance=None, inactive_stop=True: self.stop_sound(
                        instance=instance,  # inactive_stop=inactive_stop
                    )
                )

    def notify_time(self):
        """
        Plays the notification sound when the timer finishes.
        """
        self.sound = SoundLoader.load(SOUND_PATH)
        if self.sound:
            self.sound.play()
            self.stop_sound_button.disabled = False
            self.stop_sound_button.opacity = 1
        else:
            print("Sound file not found!")

    def stop_sound(self, instance):
        """
        Stops the sound if it is playing and updates the mute state.

        Args:
            instance: The button instance that triggered this method.
        """
        if self.sound:
            self.sound.stop()
            self.mute = True
        if self.mute:
            self.stop_sound_button.background_normal = STOP_SOUND
            self.sound = None
        else:
            self.stop_sound_button.disabled = True
        app = App.get_running_app()
        app.timers_status[self.name] = True
        self.next_screen(None)

    def open_settings(self, instance):
        """
        Opens the settings screen when the settings button is pressed.

        Args:
            instance: The button instance that triggered this method.
        """
        self.manager.transition = SlideTransition(direction="left")
        app = App.get_running_app()
        app.prev_screen = self.manager.current
        self.manager.current = "settings"

    def next_screen(self, instance):
        """
        Transitions to the next screen when the next button is pressed.

        Args:
            instance: The button instance that triggered this method.
        """
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.next_screen_name

    def previous_screen(self, instance):
        """
        Transitions to the previous screen when the previous button is pressed.

        Args:
            instance: The button instance that triggered this method.
        """
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.previous_screen_name


class SettingsScreen(Screen):
    """
    The settings screen for customizing timer options and other configurations.

    Attributes:
        time_options (dict): A dictionary of available timer options.
        selected_times (dict): A dictionary of the selected times for each timer.
        n_pomodoros (int): The number of Pomodoro cycles.
        tree_nodes (dict): A dictionary to store references to TreeViewLabel nodes.
    """

    def __init__(self, time_options, selected_times, n_pomodoros, **kwargs):
        """
        gets the SettingsScreen started for the timer options and other settings.

        Args:
            time_options (dict): A dictionary of available timer options.
            selected_times (dict): A dictionary of the selected times for each timer.
            n_pomodoros (int): The number of Pomodoro cycles.
        """
        super(SettingsScreen, self).__init__(**kwargs)
        self.time_options = time_options
        self.selected_times = selected_times
        self.n_pomodoros = n_pomodoros
        self.tree_nodes = {}

        # Create a ScrollView for the TreeView
        scrollview = ScrollView(size_hint=(1, 1))

        # Create the TreeView
        treeview = TreeView(root_options=dict(text="Settings"), hide_root=True, size_hint_y=None)
        treeview.bind(minimum_height=treeview.setter("height"))

        # Timer options
        self.add_timer_options(treeview)

        # Add the numbers of pomodoros
        tree_node = treeview.add_node(TreeViewLabel(text="Cycles"))
        for n_cycles in [1, 2, 3, 4, 5, 6]:
            cycles_node = treeview.add_node(TreeViewLabel(text=str(n_cycles)), tree_node)

            # Highlight the selected option
            if n_cycles == self.n_pomodoros:
                cycles_node.color = (0.3, 0.5, 1, 1)

            # Bind the selection action
            cycles_node.bind(
                on_touch_down=lambda instance, touch, opt=cycles_node: self.select_cycles(
                    instance, touch, opt
                )
            )

        # Always on Top option
        self.always_on_top_node = treeview.add_node(TreeViewLabel(text="Float on Top On"))
        self.always_on_top_node.bind(on_touch_down=self.toggle_always_on_top)

        # Transparency option
        self.transparency_node = treeview.add_node(TreeViewLabel(text="Translucent On"))
        self.transparency_node.bind(on_touch_down=self.toggle_transparency)

        # Done button
        done_node = treeview.add_node(TreeViewLabel(text="Done"))
        done_node.bind(on_touch_down=self.done_settings)

        scrollview.add_widget(treeview)
        self.add_widget(scrollview)

    def update_node_text(self, node, text):
        """
        Updates the text of a TreeViewLabel node.

        Args:
            node (TreeViewLabel): The node to update.
            text (str): The new text for the node.
        """
        node.text = text

    def toggle_always_on_top(self, instance, touch):
        """
        Toggles the "Always on Top" window option.

        Args:
            instance (TreeViewLabel): The node that was touched.
            touch: The touch event instance.
        """
        if instance.collide_point(*touch.pos):
            if platform.system() == "Darwin":
                NSApplication = objc.lookUpClass("NSApplication")
                app = NSApplication.sharedApplication()
                window = app.windows()[0]  # Get the main window

                current_text = self.always_on_top_node.text
                if "On" in current_text:
                    window.setLevel_(kCGStatusWindowLevel)  # Set to "Always on Top"
                    self.update_node_text(self.always_on_top_node, "Float on Top Off")
                else:
                    window.setLevel_(kCGNormalWindowLevel)  # Set back to normal
                    self.update_node_text(self.always_on_top_node, "Float on Top On")

    def toggle_transparency(self, instance, touch):
        """
        Toggles the window transparency option.

        Args:
            instance (TreeViewLabel): The node that was touched.
            touch: The touch event instance.
        """
        if instance.collide_point(*touch.pos):
            current_text = self.transparency_node.text
            if "On" in current_text:
                Window.opacity = 0.8  # Adjust opacity as needed
                self.update_node_text(self.transparency_node, "Translucent Off")
            else:
                Window.opacity = 1  # Reset opacity to full
                self.update_node_text(self.transparency_node, "Translucent On")

    def add_timer_options(self, treeview):
        """
        Adds timer options to the TreeView.

        Args:
            treeview (TreeView): The TreeView to which the timer options are added.
        """
        root_node = treeview.add_node(TreeViewLabel(text="Custom timers"))

        for option, time_options in self.time_options.items():
            tree_node = treeview.add_node(TreeViewLabel(text=option), root_node)

            for time_option in time_options:
                time_node = treeview.add_node(TreeViewLabel(text=time_option), tree_node)

                # Store reference to the TreeViewLabel node
                self.tree_nodes[(option, time_option)] = time_node

                # Highlight the selected time
                if self.selected_times[option] == time_option:
                    time_node.color = (0.3, 0.5, 1, 1)

                # Bind the selection action
                time_node.bind(
                    on_touch_down=lambda instance, touch, opt=option, time_opt=time_option: self.select_time(
                        instance, touch, opt, time_opt
                    )
                )

    def done_settings(self, instance, touch):
        """
        Saves settings and returns to the previous screen.

        Args:
            instance (TreeViewLabel): The node that was touched.
            touch: The touch event instance.
        """
        self.manager.transition = SlideTransition(direction="right")
        if instance.collide_point(*touch.pos):
            app = App.get_running_app()
            self.manager.current = app.prev_screen

    def select_time(self, instance, touch, screen, time):
        """
        Selects a specific timer option and updates the TreeView to reflect the selection.

        Args:
            instance (TreeViewLabel): The node that was touched.
            touch: The touch event instance.
            screen (str): The name of the screen associated with the timer (e.g., "Pomodoro 1").
            time (str): The selected time option (e.g., "25 min").
        """
        if instance.collide_point(*touch.pos):
            app = App.get_running_app()
            # Reset the color of the previous selection
            previous_time = app.selected_times[screen]
            if (screen, previous_time) in self.tree_nodes:
                self.tree_nodes[(screen, previous_time)].color = (
                    1,
                    1,
                    1,
                    1,
                )  # Default color

            # Update the selected time
            self.selected_times[screen] = time

            # Highlight the new selection
            self.tree_nodes[(screen, time)].color = (0.3, 0.5, 1, 1)

            # Update the actual application timer values
            screen_map = app.screen_map
            selected_screen = screen_map[screen]
            selected_time = time.split(":")[0]
            app.root.get_screen(selected_screen).duration = int(selected_time) * 60
            app.root.get_screen(selected_screen).time = int(selected_time) * 60
            app.root.get_screen(selected_screen).label.text = app.root.get_screen(
                "main"
            ).format_time(int(selected_time) * 60)
            app.root.get_screen(selected_screen).reset_timer(None)

    def select_cycles(self, instance, touch, n_cycles):
        """
        Handles the selection of the number of Pomodoro cycles (n_cycles) in the settings screen.

        Args:
            instance (kivy.uix.treeview.TreeViewLabel): The TreeViewLabel instance that was touched.
            touch (kivy.input.motionevent.MotionEvent): The touch event that triggered the method.
            n_cycles (int): The selected number of Pomodoro cycles.
        """
        if instance.collide_point(*touch.pos):
            app = App.get_running_app()
            self.n_pomodoros = int(n_cycles.text)  # Update the number of Pomodoros
            app.rebuild_screens(
                self.n_pomodoros
            )  # Rebuild screens with the new number of Pomodoros


class DonTomateApp(App):
    """
    The main application class for the Don Tomate Pomodoro app.
    Manages the app's screens, timers, and settings.
    """

    def build(self, n_pomodoros=4):
        """
        Builds the main application interface, including the screen manager and initial screens.

        Args:
            n_pomodoros (int): The number of Pomodoro cycles (default is 4).

        Returns:
            ScreenManager: The screen manager containing all the screens of the app.
        """
        self.icon = ICON
        self.screen_map = {}
        self.time_options = {}
        self.selected_times = {}
        self.n_pomodoros = n_pomodoros
        self.current_timer = None
        self.timers_status = {}
        self.screens = ["main", "long_break"]
        self.make_screen_mapping()

        sm = ScreenManager()
        sm = self.build_screens(sm)

        sm.add_widget(
            SettingsScreen(
                name="settings",
                time_options=self.time_options,
                selected_times=self.selected_times,
                n_pomodoros=self.n_pomodoros,
            )
        )
        return sm

    def make_screen_mapping(self):
        """
        Creates mappings for the screen names, time options, and selected times
        based on the number of Pomodoro cycles. This mapping is used to manage
        transitions between different screens in the app.
        """
        pomodoro_time_options = [
            "05:00",
            "10:00",
            "15:00",
            "20:00",
            "25:00",
            "30:00",
        ]
        break_time_options = [
            "05:00",
            "10:00",
            "15:00",
            "20:00",
            "25:00",
            "30:00",
        ]
        screen_map, time_options, selected_times = {}, {}, {}
        for i in range(self.n_pomodoros + 1):
            if i == 0:
                screen_map["Pomodoro 1"] = "main"
                time_options["Pomodoro 1"] = pomodoro_time_options
                selected_times["Pomodoro 1"] = "25:00"
            elif i == self.n_pomodoros:
                screen_map["Long Break"] = "long_break"
                time_options["Long Break"] = break_time_options
                selected_times["Long Break"] = "15:00"
            else:
                screen_map[f"Short Break {i}"] = f"break_{i}"
                time_options[f"Short Break {i}"] = break_time_options
                selected_times[f"Short Break {i}"] = "05:00"
                screen_map[f"Pomodoro {i + 1}"] = f"main_{i + 1}"
                time_options[f"Pomodoro {i + 1}"] = pomodoro_time_options
                selected_times[f"Pomodoro {i + 1}"] = "25:00"

        self.screen_map = screen_map
        self.time_options = time_options
        self.selected_times = selected_times
        self.screens = list(screen_map.values())

    def build_screens(self, sm):
        """
        Creates and adds all the Pomodoro, break, and long break screens to the screen manager.

        Args:
            sm (ScreenManager): The screen manager to which the screens will be added.

        Returns:
            ScreenManager: The updated screen manager with all the screens added.
        """
        if self.n_pomodoros == 1:
            next_screen_name = "long_break"
        else:
            next_screen_name = "break_1"

        sm.add_widget(
            MainScreen(
                name="main",
                screen="Pomodoro 1",
                duration=25 * 60,
                previous_screen_name="long_break",
                next_screen_name=next_screen_name,
            )
        )

        idx = 0
        for screen, name in self.screen_map.items():
            if idx == 0:
                pass
            elif idx + 1 == len(self.screens):
                sm.add_widget(
                    MainScreen(
                        name="long_break",
                        screen="Long Break",
                        duration=30 * 60,
                        dir_left_button_opacity=100,
                        dir_left_button_disabled=False,
                        previous_screen_name=self.screens[idx - 1],
                        next_screen_name="main",
                    )
                )
            else:
                duration = 5 * 60 if "break" in name else 25 * 60
                sm.add_widget(
                    MainScreen(
                        name=name,
                        screen=screen,
                        duration=duration,
                        dir_left_button_opacity=100,
                        dir_left_button_disabled=False,
                        previous_screen_name=self.screens[idx - 1],
                        next_screen_name=self.screens[idx + 1],
                    )
                )

            idx += 1

        return sm

    def rebuild_screens(self, n_pomodoros):
        """
        Rebuild the screens in the application based on the updated number of Pomodoros.

        Args:
            n_pomodoros (int): The number of Pomodoro cycles to set up.
        """
        self.current_timer = None
        self.timers_status = {}
        self.n_pomodoros = n_pomodoros
        self.make_screen_mapping()  # Recreate the screen mappings based on the new number of Pomodoros
        self.screens = list(self.screen_map.values())

        sm = self.root
        sm.clear_widgets()  # Remove all previous screens

        sm = self.build_screens(sm)  # Rebuild the screens

        sm.add_widget(
            SettingsScreen(
                name="settings",
                time_options=self.time_options,
                selected_times=self.selected_times,
                n_pomodoros=n_pomodoros,
            )
        )  # Add the settings screen back
        sm.current = "main"  # Return to the main screen after rebuilding


if __name__ == "__main__":
    DonTomateApp().run()
