from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.animation import Animation
from kivy.core.text import LabelBase
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import os

# Registering custom fonts
LabelBase.register(name="Montserrat", fn_regular="assets/Montserrat-Bold.ttf")

class StalkMeApp(App):
    def build(self):
        self.title = "StalkMe"
        self.icon = 'path/to/icon.png'

        # Main layout with gradient background
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Background color for fallback
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        # Username input with modern design
        self.username_input = TextInput(
            hint_text='Enter Instagram username',
            hint_text_color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, 0.1),
            background_color=(0.15, 0.15, 0.15, 0.7),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            halign="center",
            font_size=20,
            padding_y=[15, 15],
            font_name="Montserrat"
        )

        # Fetch button with neumorphism effect
        generate_button = Button(
            text='Fetch Profile Picture',
            size_hint=(1, 0.1),
            background_normal='',
            background_color=(0.99, 0.35, 0.02, 1),  # Reddish orange color
            color=(1, 1, 1, 1),
            font_size=20,
            font_name="Montserrat"
        )
        generate_button.bind(on_press=self.fetch_profile_picture)
        self.add_neumorphism_effect(generate_button)
        self.add_button_effect(generate_button, (0.99, 0.35, 0.02, 1), (0.85, 0.1, 0.1, 1))

        # Download button
        download_button = Button(
            text='Download Profile Picture',
            size_hint=(1, 0.1),
            background_normal='',
            background_color=(0.6, 1, 0.6, 1),  # Light green color
            color=(0, 0, 0, 1),
            font_size=20,
            font_name="Montserrat"
        )
        download_button.bind(on_press=self.download_image)
        self.add_button_effect(download_button, (0.6, 1, 0.6, 1), (0.4, 0.8, 0.4, 1))

        # Result label
        self.result_label = Label(
            text='',
            size_hint=(1, 0.2),
            color=(1, 1, 1, 1),
            font_size=18,
            halign="center",
            font_name="Montserrat"
        )

        layout.add_widget(self.username_input)
        layout.add_widget(generate_button)
        layout.add_widget(download_button)
        layout.add_widget(self.result_label)

        return layout

    def add_neumorphism_effect(self, widget):
        with widget.canvas.before:
            Color(0.25, 0.25, 0.25, 1)
            RoundedRectangle(pos=widget.pos, size=widget.size, radius=[10])
        widget.bind(pos=self.update_shadow, size=self.update_shadow)

    def update_shadow(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.25, 0.25, 0.25, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[10])

    def add_button_effect(self, button, idle_color, pressed_color):
        def on_press(instance):
            instance.background_color = pressed_color

        def on_release(instance):
            instance.background_color = idle_color

        button.bind(on_press=on_press, on_release=on_release)

    def fetch_profile_picture(self, instance):
        username = self.username_input.text
        url = f"https://instagram.com/{username}"
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            image_tag = soup.find('meta', property='og:image')
            if image_tag:
                self.image_url = image_tag['content']  # Store the image URL
                self.show_popup(self.image_url)
            else:
                self.result_label.text = "Profile picture not found or user is private."

        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"

    def download_image(self, instance):
        if hasattr(self, 'image_url'):
            try:
                response = requests.get(self.image_url)
                response.raise_for_status()  # Check for HTTP errors

                image_data = BytesIO(response.content)
                file_path = os.path.join(os.path.expanduser("~"), 'Downloads', 'profile_image.jpg')

                # Save the image to the Downloads folder
                with open(file_path, 'wb') as file:
                    file.write(image_data.getvalue())

                self.result_label.text = f"Image downloaded to {file_path}"
            except Exception as e:
                self.result_label.text = f"Error downloading image: {str(e)}"
        else:
            self.result_label.text = "Please fetch a profile picture first."

    def show_popup(self, image_url):
        popup_layout = FloatLayout()

        # Frosted glass effect background for popup
        with popup_layout.canvas.before:
            Color(1, 1, 1, 0.2)  # Semi-transparent white for frosted glass
            RoundedRectangle(size=popup_layout.size, pos=popup_layout.pos, radius=[15])

        # Display the image with a zoom-in animation
        response = requests.get(image_url)
        image_data = BytesIO(response.content)
        profile_image = Image(texture=CoreImage(image_data, ext="jpg").texture,
                              size_hint=(0.8, 0.8),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        anim = Animation(size_hint=(1, 1), duration=0.5, t='out_back')
        anim.start(profile_image)

        # Close button with subtle highlight on hover
        close_button = Button(
            text='X',
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={'right': 0.95, 'top': 0.95},
            background_color=(1, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            font_name="Montserrat"
        )
        close_button.bind(on_press=self.close_popup)
        self.add_button_effect(close_button, (1, 0.3, 0.3, 1), (1, 0.5, 0.5, 1))

        popup_layout.add_widget(profile_image)
        popup_layout.add_widget(close_button)

        self.popup = ModalView(size_hint=(0.9, 0.9), background='', auto_dismiss=False)
        self.popup.add_widget(popup_layout)
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

if __name__ == '__main__':
    StalkMeApp().run()
