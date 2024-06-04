from time import sleep
import flet as ft

from helpers.utils import es_url, validateData
from services.universo_series_data import UniversoSeriesData


def showSnackbar(e,text:str):
    e.page.snack_bar = ft.SnackBar(ft.Text(text))
    e.page.snack_bar.open = True
    e.page.update()

def homeScreen(page: ft.Page):
    def changeColor(e):
        page.client_storage.set("darkMode",not page.client_storage.get("darkMode"))
        page.theme_mode = ft.ThemeMode.LIGHT if page.client_storage.get("darkMode") else ft.ThemeMode.DARK
        page.update()
    def open_settings(e):
        page.go("/settings")
    appbar = ft.AppBar(
            elevation=4,
            center_title=True,
            leading=ft.Icon(ft.icons.MOVIE_ROUNDED),
            title=ft.Text("UniversoSeries Database"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.DARK_MODE_ROUNDED if page.client_storage.get("darkMode") else ft.icons.LIGHT_MODE_ROUNDED, style=ft.ButtonStyle(padding=2),on_click=changeColor),
                ft.IconButton(ft.icons.SETTINGS_ROUNDED, style=ft.ButtonStyle(padding=2),on_click=open_settings)
            ],
        )

    descriptionValueWidget = ft.TextField(shift_enter=True,hint_text="Escriba la descripcion de la serie.",label="Descripcion de la serie.",border_radius=ft.BorderRadius(10,10,10,10),max_lines=5)
    descriptionWidget = ft.Container(
        padding=ft.Padding(right=10,left=10,top=10,bottom=0),
        content= descriptionValueWidget,
    )
    urlSerieWidget = ft.TextField(hint_text="https://visuales.uclv.cu" ,label="Direccion de la serie",border_radius=ft.BorderRadius(10,10,10,10))
    urlSerieContainer = ft.Container(
        padding=ft.Padding(right=10,left=10,top=10,bottom=0),
        content= urlSerieWidget,
    )
    nameWidget = ft.TextField(shift_enter=True,hint_text="Escriba el nombre de la serie.",label="Nombre de la serie.",border_radius=ft.BorderRadius(10,10,10,10),expand=True)
    valorationWidget = ft.TextField(shift_enter=True,hint_text="5.0",label="Valoracion de la serie",border_radius=ft.BorderRadius(10,10,10,10),prefix_icon=ft.icons.STAR_BORDER_ROUNDED)
    rowNameValoration = ft.Row(controls=[ft.Container(width=10), nameWidget,ft.Container(width=20),valorationWidget,ft.Container(width=10)],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    posterWidget = ft.TextField(expand=True,shift_enter=True,hint_text="https://",label="Poster de la serie",border_radius=ft.BorderRadius(10,10,10,10))
    portadaWidget = ft.TextField(expand=True,shift_enter=True,hint_text="https://",label="Portada de la serie",border_radius=ft.BorderRadius(10,10,10,10))
    rowPosterPortada = ft.Row(controls=[ft.Container(width=3),posterWidget,ft.Container(width=20),portadaWidget,ft.Container(width=3)])
    trailerWidget = ft.TextField(expand=True,shift_enter=True,hint_text="https://",label="Trailer de la serie",border_radius=ft.BorderRadius(10,10,10,10))
    unicTempWidget = ft.Switch(label="¿Temporada Unica?", label_position=ft.LabelPosition.LEFT)
    haveSubtitleWidget = ft.Switch(label="¿Contiene subtitulos?", label_position=ft.LabelPosition.LEFT)
    columOther = ft.Column(controls=[unicTempWidget,haveSubtitleWidget])
    rowTrailerOther = ft.Row(controls=[ft.Container(width=3),trailerWidget,ft.Container(width=20),columOther,ft.Container(width=3)])
    devider = ft.Container(
        padding=ft.Padding(left=50,right=50,top=0,bottom=0),
        content=ft.Divider(),
    )
    
    
    dlg = ft.AlertDialog(modal=True,title=ft.Text('Subiendo...'),content=ft.Column(
            [ft.ProgressRing()],
            height=60,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ))
    
    def clearAllData(elements:list[ft.TextField]):
        for element in elements:
            element.value = None
            page.update()
    
    
    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dlg(e):
        dlg.open = False
        page.update()
    
    def createSerieMethods():
        universo = UniversoSeriesData()
        if(unicTempWidget.value):
            universo.getOnlySeasonMedia(description=descriptionValueWidget.value,haveSubtitle=haveSubtitleWidget.value,name=nameWidget.value,populate=valorationWidget.value,portada=portadaWidget.value,poster=posterWidget.value,serieUrl=urlSerieWidget.value,trailer=trailerWidget.value)
        else:
            universo.getMultiSeasonMedia(description=descriptionValueWidget.value,haveSubtitle=haveSubtitleWidget.value,name=nameWidget.value,populate=valorationWidget.value,portada=portadaWidget.value,poster=posterWidget.value,serieUrl=urlSerieWidget.value,trailer=trailerWidget.value)
    def createSerie(e):
        success = []
        errors = []
        if not validateData(portadaWidget, haveUrl=True):
            errors.append(portadaWidget)
        else:
            portadaWidget.error_text = None
            success.append(portadaWidget)
        if not validateData(nameWidget):
            errors.append(nameWidget)
        else:
            nameWidget.error_text = None
            success.append(nameWidget)
        if not validateData(posterWidget, haveUrl=True):
            errors.append(posterWidget)
        else:
            posterWidget.error_text = None
            success.append(posterWidget)
        if not validateData(trailerWidget, haveUrl=True):
            errors.append(trailerWidget)
        else:
            trailerWidget.error_text = None
            success.append(trailerWidget)
        if not validateData(valorationWidget, isNumeric=True):
            errors.append(valorationWidget)
        else:
            valorationWidget.error_text = None
            success.append(valorationWidget)
        if not validateData(descriptionValueWidget):
            errors.append(descriptionValueWidget)
        else:
            descriptionValueWidget.error_text = None
            success.append(descriptionValueWidget)
        if not validateData(urlSerieWidget):
            errors.append(urlSerieWidget)
        else:
            urlSerieWidget.error_text = None
            success.append(urlSerieWidget)
            
        if not errors:
            try:
                open_dlg(e)
                createSerieMethods()
                close_dlg(e)
                clearAllData(success)
                showSnackbar(e,"Serie agregada correctamente.")
                page.update()
            except:
                close_dlg(e)
                showSnackbar(e,"Ups... ha ocurrido un error al agregar.")
                page.update()
            
        else:
            for error in errors:
                error.update()
            for succes in success:
                succes.update()
            page.update()       
        page.update()

    addWidget = ft.ElevatedButton(icon=ft.icons.ADD_ROUNDED,text="Agregar Serie",on_click=createSerie,elevation=5)
    
    allWidgets = ft.Column(auto_scroll=True, controls=[urlSerieContainer,rowNameValoration,devider,rowPosterPortada,devider,rowTrailerOther,devider,descriptionWidget,addWidget],alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    return ft.View(
        "/",
        [
            allWidgets
        ],
        appbar,
        floating_action_button=ft.FloatingActionButton(icon=ft.icons.ADD, on_click=createSerie)
    )
    