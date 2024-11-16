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

class SeniorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title
        title = Label(
            text="Senior Friendly App",
            font_size="40sp",
            size_hint=(1, 0.2)
        )
        layout.add_widget(title)

        # ScrollView to allow scrolling of buttons
        scroll_view = ScrollView(size_hint=(1, 0.8))

        # Vertical layout for apps inside the ScrollView
        apps_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        apps_layout.bind(minimum_height=apps_layout.setter('height'))

        apps = [
            ("Phone", self.open_phone),
            ("WhatsApp", self.open_whatsapp),
            ("Messages", self.open_messages),
            ("Photos", self.open_photos),
            ("Weather", self.open_weather),
            ("Calendar", self.open_calendar),
            ("Camera", self.open_camera),
            ("Music", self.open_music),
            ("Settings", self.open_settings),
            ("PhonePay", self.open_phonepay),
            ("Kannada Translator", self.voice_command)  # New button for voice commands
        ]

        for name, func in apps:
            button = Button(
                text=name,
                font_size="20sp",
                size_hint=(1, None),
                height=100,  # Set height for large, touch-friendly buttons
                on_press=func
            )
            apps_layout.add_widget(button)

        scroll_view.add_widget(apps_layout)

        layout.add_widget(scroll_view)

        # Emergency Button
        emergency_button = Button(
            text="EMERGENCY",
            font_size="30sp",
            background_color=(1, 0, 0, 1),
            size_hint=(1, 0.2),
            on_press=self.emergency_action
        )
        layout.add_widget(emergency_button)

        return layout

    def init_tts(self):
        """Initialize text-to-speech engine."""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    def speak(self, text):
        """Function to speak the given text."""
        self.engine.say(text)
        self.engine.runAndWait()

    # Placeholder functions for each app
    def open_phone(self, instance):
        self.speak("Opening Phone...")
        self.launch_app("Phone")

    def open_whatsapp(self, instance):
        self.speak("Opening WhatsApp...")
        self.launch_app("WhatsApp")

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
        self.speak("Opening Calendar...")
        self.launch_app("Calendar")

    def open_camera(self, instance):
        self.speak("Opening Camera...")
        self.launch_app("Camera")

    def open_music(self, instance):
        self.speak("Opening Music...")
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
                print(f"Opening {app_name }...")
            except Exception as e:
                print(f"Failed to open {app_name}: {str(e)}")
        elif os.name == 'nt':  # For Windows
            print(f"Attempting to open {app_name}...")

    def emergency_action(self, instance):
        print("Emergency Action Triggered!")
        self.speak("Emergency Action Triggered!")
        self.send_location_to_contact()
        self.call_emergency_contact()

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
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return
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
