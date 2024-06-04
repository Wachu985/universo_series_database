import flet as ft
from dotenv import load_dotenv

from screens.main_screen import main



load_dotenv()

if __name__ == '__main__':
    ft.app(main)