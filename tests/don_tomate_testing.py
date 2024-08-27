import pytest
from unittest.mock import patch, MagicMock
from kivy.uix.screenmanager import ScreenManager
from don_tomate.main import DonTomateApp


@pytest.fixture
def app_instance():
    # Create an instance of your DonTomateApp
    app = DonTomateApp()
    app.build()
    return app


@pytest.fixture
def screen_manager(app_instance):
    # Mock the ScreenManager used in the app
    sm = ScreenManager()
    app_instance.build_screens(sm)
    return sm


def test_initial_timer_value(app_instance, screen_manager):
    # Select the first Pomodoro screen
    screen = screen_manager.get_screen("main")

    # Assert that the initial timer value is set correctly (25 minutes)
    assert screen.time == 25 * 60
    assert screen.label.text == "25:00"


def test_start_stop_timer(app_instance, screen_manager):
    screen = screen_manager.get_screen("main")

    # Mock the clock scheduling
    with patch("kivy.clock.Clock.schedule_interval") as mock_schedule:
        screen.start_stop(None)
        assert screen.running is True
        mock_schedule.assert_called_once()

    # Stop the timer
    screen.start_stop(None)
    assert screen.running is False


def test_timer_countdown(app_instance, screen_manager):
    screen = screen_manager.get_screen("main")

    # Start the timer and decrement time
    screen.start_stop(None)
    screen.update_time(1)

    # Check that the timer has decremented by 1 second
    assert screen.time == 25 * 60 - 1
    assert screen.label.text == "24:59"


def test_timer_completion_notification(app_instance, screen_manager):
    screen = screen_manager.get_screen("main")

    # Mock the sound playing functionality
    with patch("kivy.core.audio.SoundLoader.load") as mock_sound_loader:
        mock_sound = MagicMock()
        mock_sound_loader.return_value = mock_sound

        # Simulate the timer finishing
        screen.time = 0
        screen.running = True
        screen.update_time(1)

        assert screen.time == 0
        assert screen.label.text == "Time's up!"
        mock_sound.play.assert_called_once()


def test_reset_timer(app_instance, screen_manager):
    screen = screen_manager.get_screen("main")

    # Start and reset the timer
    screen.start_stop(None)
    screen.reset_timer(None)

    # Ensure the timer is reset to the initial value
    assert screen.time == 25 * 60
    assert screen.label.text == "25:00"
    assert screen.running is False
