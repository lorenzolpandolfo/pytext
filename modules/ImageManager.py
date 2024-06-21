import os
from tkinter import PhotoImage
from modules.FileManager import FileManager as fm
from PIL import Image, ImageTk
from modules.Application import Application


class ImageManager:
    """Deals with Pytext's images loading."""

    @staticmethod
    def get_image(title: str, size: tuple[int, int]) -> PhotoImage:
        """Returns a PhotoImage instance with the image title and size arguments loaded."""
        if ImageManager._check_if_image_exists_(title) or ImageManager._check_if_image_exists_(title, fallback=True):
            forced_theme = Application.mainapp.user_config["forced_theme"]

            l_img_path = os.path.join(os.getcwd(), f"{title}.png")
            d_img_path = os.path.join(os.getcwd(), f"{title}_dark.png")

            if forced_theme:
                if forced_theme == "light":
                    d_img_path = l_img_path
                elif forced_theme == "dark":
                    l_img_path = d_img_path

            l_img_pil = Image.open(l_img_path).resize(size)
            d_img_pil = Image.open(d_img_path).resize(size)

            l_img_tk = ImageTk.PhotoImage(l_img_pil)
            return l_img_tk

    @staticmethod
    def _check_if_image_exists_(title: str, fallback: bool = False) -> bool:
        """Checks if image title exists in the pytext/images directory."""
        fm.move_to_directory("images") if not fallback else fm.move_to_directory("images", "fallback")
        title = f"{title}.png"
        all_images = os.listdir(os.getcwd())
        return title in all_images if title.endswith(".png") else False
