from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.animation import Animation
import requests

class ImageUploaderApp(MDApp):

    def build(self):
        self.title = "X-Ray Analyzer"
        Window.size = (400, 600)
        
        # Create a screen for the home page
        screen = MDScreen()
        
        # Create a layout to add widgets, with padding and good spacing
        layout = MDBoxLayout(orientation='vertical', spacing=30, padding=[20, 30, 20, 30])

        # Title label - X-Ray Analyzer
        title_label = MDLabel(
            text="X-Ray Analyzer",
            halign="center",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(0.1, 0.4, 0.8, 1)  # Blue color for the title
        )
        layout.add_widget(title_label)

        # Add a label with a smaller font for upload instructions
        upload_label = MDLabel(
            text="Upload an X-Ray Image to Analyze",
            halign="center",
            font_style="Subtitle1"
        )
        layout.add_widget(upload_label)

        # Button to open file manager, with centered alignment and added styling
        upload_btn = MDRaisedButton(
            text="Upload Image",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.1, 0.5, 0.7, 1),  # Custom color for the button
            size_hint=(None, None),
            size=(200, 50)
        )
        upload_btn.bind(on_release=self.open_file_manager)  # Binding the method
        layout.add_widget(upload_btn)

        # Placeholder for the image to be displayed
        self.image_widget = Image(size_hint_y=None, height=200, opacity=0)  # Start with opacity 0 for fade-in effect
        layout.add_widget(self.image_widget)

        # Spacer widget to add space before result (creates vertical space)
        spacer = Widget(size_hint_y=None, height=40)
        layout.add_widget(spacer)

        # Placeholder for the result label
        self.result_label = MDLabel(
            text="",
            halign="center",
            font_style="H5",  # Large font for result
            theme_text_color="Custom",
            text_color=(0.9, 0.2, 0.2, 1),  # Red color for the result
            bold=True
        )
        layout.add_widget(self.result_label)

        screen.add_widget(layout)
        return screen

    def open_file_manager(self, *args):
        # Initialize the file manager
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_image
        )
        # Open file manager to the user's home directory
        self.file_manager.show('/')

    def select_image(self, path):
        # Close the file manager
        self.exit_file_manager()

        # Display the selected image and animate it with a fade-in effect
        self.image_widget.source = path
        self.image_widget.reload()
        
        # Apply a fade-in animation to the image
        anim = Animation(opacity=1, duration=1)  # Fade-in effect over 1 second
        anim.start(self.image_widget)

        # Send the image to the Flask backend for processing
        self.upload_image(path)

    def upload_image(self, image_path):
        url = 'http://127.0.0.1:5000/upload'  # Your Flask app's endpoint
        with open(image_path, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(url, files=files)
            if response.ok:
                result = response.json().get('result')
                self.show_result(result)
            else:
                self.show_result("Error: Could not process image.")

    def show_result(self, result):
        # Update the result label to display the result
        self.result_label.text = result
        
        # Animate the result label with a bounce effect
        anim = Animation(font_size=50, duration=0.5) + Animation(font_size=30, duration=0.5)  # Bounce effect
        anim.start(self.result_label)

    def exit_file_manager(self, *args):
        # Close the file manager
        self.file_manager.close()

# Run the app
if __name__ == "__main__":
    ImageUploaderApp().run()
