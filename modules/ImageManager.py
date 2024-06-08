import os
from modules.FileManager import FileManager as fm
from PIL import Image
from customtkinter import CTkImage
from modules.Application import Application


class ImageManager:
    """Deals with Pytext's images loading."""

    @staticmethod
    def get_image(title: str, size: tuple[int, int]) -> CTkImage:
        """Returns a CTkImage instance with the image title and size arguments loaded."""
        if ImageManager._check_if_image_exists_(title) or ImageManager._check_if_image_exists_(title, fallback=True):
            forced_theme = Application.mainapp.config["forced_theme"]

            l_img = Image.open(os.path.join(os.getcwd(), f"{title}.png"))
            d_img = Image.open(os.path.join(os.getcwd(), f"{title}_dark.png"))

            if forced_theme:
                if forced_theme == "light":
                    d_img = l_img
                elif forced_theme == "dark":
                    l_img = d_img

            return CTkImage(l_img, d_img, size)

    @staticmethod
    def _check_if_image_exists_(title: str, fallback: bool = False) -> bool:
        """Checks if image title exists in the pytext/images directory."""
        fm.move_to_directory("images") if not fallback else fm.move_to_directory("images", "fallback")
        title = f"{title}.png"
        all_images = os.listdir(os.getcwd())
        return title in all_images if title.endswith(".png") else False
