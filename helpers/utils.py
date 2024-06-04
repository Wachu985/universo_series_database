from urllib.parse import urlparse

import flet as ft


def es_url(texto:str) -> bool:
    try:
        urlparse(texto)
        return True
    except ValueError:
        return False

def es_flotante_2_digitos_menor_5(valor_str):
    try:
        valor_float = float(valor_str)
        parte_decimal = str(valor_float).split('.')[1]
        return len(parte_decimal) == 1 and valor_float < 5 and '.' in valor_str
    except ValueError:
        return False
    
def validateData(element:ft.TextField,isNumeric:bool=False,optional:bool= False,haveUrl:bool=False):
        if(not optional):
            if(len(element.value) == 0):
                element.error_text = 'El campo no debe estar vacio.'
                return False;
            elif(isNumeric):
                if(not es_flotante_2_digitos_menor_5(element.value)):
                    element.error_text = 'El campo debe ser un numero valido.'
                    return False;
            elif(haveUrl):
                if(not es_url(element.value)):
                    element.error_text = 'El texto debe ser una url.'
                    return False;
            return True;
        return True;
    

    