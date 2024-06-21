import os
from modules.FileManager import FileManager as fm
from PIL import Image, ImageTk
from customtkinter import CTkImage
from modules.Application import Application


class ImageManager:
    """Deals with Pytext's images loading."""

    @staticmethod
    def get_image(title: str, size: tuple[int, int]):
        """Returns a Tk PhotoImage instance with the image title and size arguments loaded."""

        def check_if_image_exists(title, fallback=False):
            filename = f"{title}.png"
            if fallback:
                filename = f"{title}_dark.png"
            return os.path.exists(os.path.join(os.getcwd(), filename))

        if check_if_image_exists(title) or check_if_image_exists(title, fallback=True):
            forced_theme = Application.mainapp.user_config["forced_theme"]

            l_img_path = os.path.join(os.getcwd(), f"{title}.png")
            d_img_path = os.path.join(os.getcwd(), f"{title}_dark.png")

            l_img = Image.open(l_img_path)
            d_img = Image.open(d_img_path)

            if forced_theme:
                if forced_theme == "light":
                    d_img = l_img
                elif forced_theme == "dark":
                    l_img = d_img

            return ImageTk.PhotoImage(l_img), ImageTk.PhotoImage(d_img)

    @staticmethod
    def _check_if_image_exists_(title: str, fallback: bool = False) -> bool:
        """Checks if image title exists in the pytext/images directory."""
        fm.move_to_directory("images") if not fallback else fm.move_to_directory("images", "fallback")
        title = f"{title}.png"
        all_images = os.listdir(os.getcwd())
        return title in all_images if title.endswith(".png") else False
