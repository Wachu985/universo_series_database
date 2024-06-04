from flet import View,Page,AppBar,ElevatedButton,Text,colors
import flet as ft

def onClicked(color:str,page:Page):
    page.client_storage.set("colorScheme", color)
    page.theme=ft.Theme(color_scheme_seed=color)
    page.update()
def circleColor(color:str,page:Page):
    return ft.Container(shape=ft.BoxShape.CIRCLE,height=50,width=50,bgcolor=color,on_click=lambda e: onClicked(color,page) )


def changeColor(e):
    e.page.client_storage.set("darkMode",not e.page.client_storage.get("darkMode"))
    e.page.theme_mode = ft.ThemeMode.LIGHT if e.page.client_storage.get("darkMode") else ft.ThemeMode.DARK
    e.page.update()

def settingsScreen(page:Page):
    selectColorText = ft.Text('Seleccione el color de su aplicación: ')
    rowColors1 = ft.Row(
        wrap=True,
        controls=[
            circleColor(ft.colors.BROWN,page),
            circleColor(ft.colors.CYAN,page),
            circleColor(ft.colors.GREEN,page),
            circleColor(ft.colors.INDIGO,page),
            circleColor(ft.colors.LIME,page),
            circleColor(ft.colors.ORANGE,page),
            circleColor(ft.colors.PINK,page),
            circleColor(ft.colors.PURPLE,page),
            circleColor(ft.colors.RED,page),
            circleColor(ft.colors.TEAL,page),
            circleColor(ft.colors.BLUE,page),
            circleColor(ft.colors.YELLOW,page),
            circleColor(ft.colors.AMBER,page),
    ])
    developerInfo = ft.Card(
        elevation=2,
        content=ft.ListTile(title=ft.Text('Pedro José Dominguez Bonilla'),trailing=ft.Icon(ft.icons.DEVELOPER_MODE_ROUNDED),subtitle=ft.Text('Developer'),expand=True,on_click=lambda e: e.page.launch_url('https://wachu985.hopto.org')),
    )
    switchDarkMode = ft.Switch(height=70,on_change=changeColor)
    darkModeWidget = ft.Card(
        elevation=2,
        content=ft.Container(
            margin=ft.Margin(right=20,left=20,top=0,bottom=0),
            content=ft.Row(
                controls=[
                    ft.Text('Activar el modo Oscuro',expand=True),
                    switchDarkMode,
                ]
            ),
        ),
    )
    switchDarkMode.value = page.client_storage.get("darkMode")

    appColors = ft.Card(
        elevation=2,
        content=ft.Container(
            margin=ft.Margin(left=20,right=20,top=10,bottom=10),
            content=ft.Column(expand=True,alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,controls=[selectColorText,rowColors1]),
        ),
    )
    
    return View(
                "/settings",
                [
                    
                    appColors,
                    darkModeWidget,
                    developerInfo
                ],
                appbar=AppBar(title=Text("Configuraciones"),center_title=True, bgcolor=colors.SURFACE_VARIANT),
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        