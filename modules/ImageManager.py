import os

from PIL import Image
from customtkinter import CTkImage

class ImageManager:
    """Deals with Pytext's images loading."""
    @staticmethod
    def get_image(title:str, size:tuple) -> CTkImage:
        """Returns a CTkImage instance with the image title and size."""
        if ImageManager._check_if_image_exists_(title):
            
            light_image = Image.open(os.path.join(os.getcwd(), f"{title}.png"))
            dark_image = Image.open(os.path.join(os.getcwd(), f"{title}_dark.png"))

            return CTkImage(light_image, dark_image, size)

    @staticmethod
    def __move_to_images_directory__():
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir("..")
        os.chdir("images")

    @staticmethod
    def _check_if_image_exists_(title:str) -> bool:
        ImageManager.__move_to_images_directory__()
        title = f"{title}.png"

        all_images = os.listdir(os.getcwd())
        return title in all_images