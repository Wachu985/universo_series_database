
from flet import  Page, colors,Theme,MainAxisAlignment,ThemeMode

from screens.home_screen import homeScreen
from screens.settings_screen import settingsScreen

def main(page: Page):
    page.title = "UniversoSeries"
    page.theme = Theme(use_material3=True,color_scheme_seed=page.client_storage.get("colorScheme"))
    page.theme_mode = ThemeMode.LIGHT if page.client_storage.get("darkMode") else ThemeMode.DARK
    page.vertical_alignment = MainAxisAlignment.CENTER

    def route_change(e):
        page.views.clear()
        page.views.append(
            homeScreen(page)
        )
        if page.route == "/settings":
            page.views.append(
                settingsScreen(page)
            )
        
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)