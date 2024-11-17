import os
import subprocess
import pyttsx3  # Import pyttsx3 for text-to-speech functionality
import speech_recognition as sr
from geopy.geocoders import Nominatim
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from googletrans import Translator
import datetime  # Import for date and time functionality
from kivy.uix.textinput import TextInput  # Import TextInput
from kivy.clock import Clock  # Use Kivy's Clock for scheduling instead of threading
import threading
import random  # For simulated testing on non-mobile devices
from plyer import accelerometer

class SeniorApp(App):
    def build(self):
        """Build and store the main layout."""
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title
        title = Label(
            text="Senior Friendly App",
            font_size="40sp",
            size_hint=(1, 0.2)
        )
        self.main_layout.add_widget(title)

        # ScrollView for buttons
        scroll_view = ScrollView(size_hint=(1, 0.8))
        apps_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        apps_layout.bind(minimum_height=apps_layout.setter('height'))

        apps = [
            ("Phone", self.open_phone),
            ("WhatsApp", self.open_whatsapp),
            ("Messages", self.open_messages),
            ("Medicine Reminder", self.medicine_reminder),
            ("Photos", self.open_photos),
            ("Weather", self.open_weather),
            ("Calendar", self.open_calendar),
            ("Camera", self.open_camera),
            ("Music", self.open_music),
            ("Settings", self.open_settings),
            ("PhonePay", self.open_phonepay),
            ("Kannada Translator", self.voice_command)
        ]

        for name, func in apps:
            button = Button(
                text=name,
                font_size="20sp",
                size_hint=(1, None),
                height=100,
                on_press=func
            )
            apps_layout.add_widget(button)

        scroll_view.add_widget(apps_layout)
        self.main_layout.add_widget(scroll_view)

        # Emergency Button
        emergency_button = Button(
            text="EMERGENCY",
            font_size="30sp",
            background_color=(1, 0, 0, 1),
            size_hint=(1, 0.2),
            on_press=self.emergency_action
        )
        self.main_layout.add_widget(emergency_button)

        return self.main_layout

    def go_back_to_main(self, instance):
        """Navigate back to the main layout."""
        self.root.clear_widgets()  # Remove current layout
        self.root.add_widget(self.main_layout)  # Re-add the stored main layout

    def init_tts(self):
        """Initialize text-to-speech engine."""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    def speak(self, text):
        """Function to speak the given text."""
        self.engine.say(text)
        self.engine.runAndWait()

    # Medicine Reminder Feature
    def medicine_reminder(self, instance):
        """Open a window to set multiple medicine reminders."""
        self.reminder_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        title = Label(text="Set Medicine Reminders", font_size="30sp", size_hint=(1, 0.2))
        self.reminder_layout.add_widget(title)

        # Input for time and medicine name
        self.medicine_inputs = []

        def add_medicine_input():
            """Add inputs for medicine and time."""
            input_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)

            time_input = TextInput(hint_text="Time (HH:MM)", size_hint=(0.4, 1))
            medicine_input = TextInput(hint_text="Medicine Name", size_hint=(0.6, 1))

            input_layout.add_widget(time_input)
            input_layout.add_widget(medicine_input)

            self.reminder_layout.add_widget(input_layout, len(self.reminder_layout.children) - 2)
            self.medicine_inputs.append((time_input, medicine_input))

        # Add initial inputs
        add_medicine_input()

        # Add Medicine Button
        add_button = Button(
            text="Add Another Medicine",
            font_size="20sp",
            size_hint=(1, 0.2),
            on_press=lambda _: add_medicine_input()
        )
        self.reminder_layout.add_widget(add_button)

        # Set Reminder Button
        set_button = Button(
            text="Set Reminders",
            font_size="20sp",
            size_hint=(1, 0.2),
            on_press=self.set_alarms
        )
        self.reminder_layout.add_widget(set_button)

        # Back Button to return to main layout
        back_button = Button(
            text="Back",
            font_size="20sp",
            size_hint=(1, 0.2),
            on_press=self.go_back_to_main
        )
        self.reminder_layout.add_widget(back_button)

        # Replace the main app layout with the reminder layout
        self.root.clear_widgets()
        self.root.add_widget(self.reminder_layout)

    def set_alarms(self, instance):
        """Set alarms for multiple medicines."""
        now = datetime.datetime.now()
        for time_input, medicine_input in self.medicine_inputs:
            alarm_time = time_input.text
            medicine_name = medicine_input.text.strip()

            if not alarm_time or not medicine_name:
                continue  # Skip incomplete entries

            try:
                # Validate and parse time
                alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
                alarm_datetime = now.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

                if alarm_datetime < now:
                    alarm_datetime += datetime.timedelta(days=1)

                # Schedule the alarm
                delay = (alarm_datetime - now).total_seconds()
                threading.Timer(delay, self.trigger_alarm, [medicine_name]).start()

                print(f"Reminder set for {medicine_name} at {alarm_time}.")
            except Exception as e:
                print(f"Invalid time format for {medicine_name}: {str(e)}")

        self.speak("All reminders have been set.")
        self.go_back_to_main(None)

    def trigger_alarm(self, medicine_name):
        """Trigger the alarm and notify the user."""
        self.speak(f"It's time to take your medicine: {medicine_name}")
        print(f"Alarm Triggered! Take your medicine: {medicine_name}")

    # Placeholder functions for each app
    def open_phone(self, instance):
        self.speak("Opening Phone...")
        self.launch_app("Phone")
        self.listen_for_contact()

    def open_whatsapp(self, instance):
        self.speak("Opening WhatsApp...")
        self.launch_app("WhatsApp")
        self.listen_for_contact_and_message()

    def open_messages(self, instance):
        self.speak("Opening Messages...")
        self.listen_for_contact_and_message()  # Update to listen for contact and message

    def open_photos(self, instance):
        self.speak("Opening Photos...")
        self.launch_app("Photos")

    def open_weather(self, instance):
        self.speak("Opening Weather...")
        self.launch_app("Weather")

    def open_calendar(self, instance):
        """Announce the current date, day, and time."""
        now = datetime.datetime.now()
        date = now.strftime("%A, %d %B %Y")  # Example: Friday, 16 November 2024
        time = now.strftime("%I:%M %p")  # Example: 02:30 PM
        announcement = f"Today is {date}. The time is {time}."
        print(announcement)  # For debugging
        self.speak(announcement)

    def open_camera(self, instance):
        self.speak("Opening Camera...")
        self.launch_app("Camera")

    def open_music(self, instance):
        self.speak("Opening Music...\nPlaying Music")
        self.launch_app("Music")

    def open_settings(self, instance):
        self.speak("Opening Settings...")
        self.launch_app("Settings")

    def open_phonepay(self, instance):
        self.speak("Opening PhonePay...")
        self.launch_app("PhonePay")

    def launch_app(self, app_name):
        """Launch apps based on the platform."""
        if os.name == 'posix':  # For Linux / macOS
            try:
                if app_name == "Phone":
                    subprocess.call(["open", "tel://1234567890"])  # Example: open dialer
                elif app_name == "WhatsApp":
                    subprocess.call(["open", "whatsapp://"])  # Example: open WhatsApp
                # Add more app launchers as needed
                print(f"Opening {app_name}...")
            except Exception as e:
                print(f"Failed to open {app_name }: {str(e)}")
        elif os.name == 'nt':  # For Windows
            print(f"Attempting to open {app_name}...")

    def emergency_action(self, instance):
        print("Emergency Action Triggered!")
        self.speak("Emergency Action Triggered!")
        self.send_location_to_contact()
        self.call_emergency_contact()
        self.monitor_fall_detection()  # Start monitoring for falls

    def send_location_to_contact(self):
        """Simulate sending location via geopy or a real GPS system."""
        geolocator = Nominatim(user_agent="senior_app")
        location = geolocator.geocode("Current Location")  # Dummy location, can be replaced by actual GPS
        if location:
            print(f"Sending location: {location.address}")
            self.speak(f"Sending location: {location.address}")
        else:
            print("Failed to get location.")
            self.speak("Failed to get location.")

    def call_emergency_contact(self):
        """Simulate calling an emergency contact."""
        emergency_contact = "1234567890"  # Emergency contact phone number
        print(f"Calling emergency contact: {emergency_contact}")
        self.speak(f"Calling emergency contact: {emergency_contact}")
        # Add actual call functionality using an API or system command if applicable

    def monitor_fall_detection(self):
        """Monitor accelerometer data for fall detection."""
        try:
            accelerometer.enable()  # Enable accelerometer
            Clock.schedule_interval(self.check_fall, 0.5)  # Check every 0.5 seconds
        except NotImplementedError:
            print("Accelerometer not supported on this device.")
            self.speak("Fall detection not supported on your device.")
            self.simulate_fall_detection()  # Simulated testing for PCs

    def check_fall(self, dt):
        """Analyze accelerometer data to detect a fall."""
        try:
            # Use accelerometer on mobile devices
            acceleration = accelerometer.acceleration
            if acceleration is None:
                print("No accelerometer data available.")
                return
            
            x, y, z = acceleration
            magnitude = (x**2 + y**2 + z**2)**0.5  # Calculate magnitude of acceleration
            print(f"Acceleration magnitude: {magnitude:.2f}")  # Debug output

            # Threshold for fall detection
            if magnitude < 2.0 or magnitude > 20.0:
                print("Fall detected!")
                self.speak("Fall detected! Initiating emergency procedures.")
                self.call_emergency_contact()  # Call emergency contact on fall detection
        except Exception as e:
            print(f"Error reading accelerometer data: {e}")

    def simulate_fall_detection(self):
        """Simulate fall detection for testing on non-mobile devices."""
        print("Simulating fall detection on non-mobile device.")
        Clock.schedule_interval(self.simulated_fall_check, 2.0)

    def simulated_fall_check(self, dt):
        """Simulate random acceleration data for fall detection testing."""
        acceleration = (
            random.uniform(-10, 10),
            random.uniform(-10, 10),
            random.uniform(-10, 10),
        )
        print(f"Simulated acceleration: {acceleration}")
        x, y, z = acceleration
        magnitude = (x**2 + y**2 + z**2)**0.5
        if magnitude < 2.0 or magnitude > 20.0:
            print("Simulated fall detected!")
            self.speak("Simulated fall detected! Initiating emergency procedures.")
            self.call_emergency_contact()  # Call emergency contact on simulated fall detection

    def listen_for_contact(self):
        """Listen for contact and call the contact"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for the contact name...")
            audio = recognizer.listen(source)

        try:
            contact_name = recognizer.recognize_google(audio)
            print(f"Calling {contact_name}...")  # Simulate calling the contact
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def listen_for_contact_and_message(self):
        """Listen for a contact name and a message to send."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for the contact name...")
            audio = recognizer.listen(source)

        try:
            contact_name = recognizer.recognize_google(audio)
            print(f"You said: {contact_name}")
            self.listen_for_message(contact_name)  # Proceed to listen for the message
        except sr .UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def listen_for_message(self, contact_name):
        """Listen for a voice message and simulate sending it to the specified contact."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for your message...")
            audio = recognizer.listen(source)

        try:
            message = recognizer.recognize_google(audio)
            print(f"You said: {message}")
            self.send_message_to_contact(contact_name, message)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def send_message_to_contact(self, contact_name, message):
        """Simulate sending a message to a specified contact."""
        print(f"Sending message to {contact_name}: {message}")
        # Here you would implement the actual message sending logic

    def voice_command(self, instance):
        """Handle voice commands for app actions."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for voice command...")
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            self.translate_to_kannada(command)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def translate_to_kannada(self, text):
        """Translate the given text to Kannada."""
        translator = Translator()
        translation = translator.translate(text, dest='kn')
        print(f"Translation in Kannada: {translation.text}")

if __name__ == "__main__":
    app = SeniorApp()
    app.init_tts()  # Initialize TTS engine
    app.run()
