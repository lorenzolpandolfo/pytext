import os
from modules.FileManager import FileManager as fm
from PIL import Image
from customtkinter import CTkImage

class ImageManager:
    """Deals with Pytext's images loading."""
    @staticmethod
    def get_image(title:str, size:tuple) -> CTkImage:
        """Returns a CTkImage instance with the image title and size arguments loaded."""
        if ImageManager._check_if_image_exists_(title) or ImageManager._check_if_image_exists_(title, fallback=True):
            light_image = Image.open(os.path.join(os.getcwd(), f"{title}.png"))
            dark_image = Image.open(os.path.join(os.getcwd(), f"{title}_dark.png"))

            return CTkImage(light_image, dark_image, size)


    @staticmethod
    def _check_if_image_exists_(title:str, fallback:bool=False) -> bool:
        """Checks if a image title exists in the pytext/images directory."""
        fm.move_to_directory("images") if not fallback else fm.move_to_directory("images", "fallback")
        title = f"{title}.png"
        all_images = os.listdir(os.getcwd())
        return title in all_images if title.endswith(".png") else False