from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class SeniorApp(App):
    def build(self):

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title
        title = Label(
            text="Senior Friendly App",
            font_size="40sp",
            size_hint=(1, 0.2),
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
        ]

        for name, func in apps:
            button = Button(
                text=name,
                font_size="20sp",
                size_hint=(1, None),
                background_color = (1, 1, 1, 1),
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

    # Placeholder functions for each app
    def open_phone(self, instance):
        print("Opening Phone...")

    def open_whatsapp(self, instance):
        print("Opening WhatsApp...")

    def open_messages(self, instance):
        print("Opening Messages...")

    def open_photos(self, instance):
        print("Opening Photos...")

    def open_weather(self, instance):
        print("Opening Weather...")

    def open_calendar(self, instance):
        print("Opening Calendar...")

    def open_camera(self, instance):
        print("Opening Camera...")

    def open_music(self, instance):
        print("Opening Music...")

    def open_settings(self, instance):
        print("Opening Settings...")

    def open_phonepay(self, instance):
        print("Opening PhonePay...")

    def emergency_action(self, instance):
        print("Emergency Action Triggered!")
        # Call emergency contact and send location here

if __name__ == "__main__":
    SeniorApp().run()
