
import uuid
from supabase import Client, create_client
from helpers.environment import Environment
from helpers.get_link import get_links
from models.season_model import SeasonModel
from models.serie_model import SerieModel


class UniversoSeriesData:
    
    def __init__(self):
        self.__environment = Environment()
        self.initSupabase()
        self.loginWithSupabase()
        
        
    def initSupabase(self):
        self.supabase: Client = create_client(self.__environment.api_url, self.__environment.api_key)
        
    def loginWithSupabase(self):
        self.supabase.auth.sign_in_with_password({"email": self.__environment.email_supabase, "password": self.__environment.password_supabase})
    
    def logoutWithSupabase(self):
        self.supabase.auth.sign_out()
    
    def getSupabaseId(self)-> int:
        try:
            response = self.supabase.table('series').select("*(count)").execute() 
            return len(response.data) + 2
        except:
            self.logoutWithSupabase()
            raise Exception('Ha ocurrido un error')



    
    def getOnlySeasonMedia(self,serieUrl:str,haveSubtitle:str,name:str,poster:str,portada:str,description:str,populate:float,trailer:str)->SerieModel:
        try:
            serieModel = SerieModel(self.getSupabaseId(),name,portada,poster,description,populate,trailer,[])
            season = SeasonModel(caps=[],name='',subtitle=[],url='')
            caps = []
            subtitle = []
            elementActual = ""

            for element in get_links(url=serieUrl,only_videos=True):
                if(len(elementActual) == 0):
                    elementActual = "Temporada 1"
                    season.name =  "Temporada 1"
                    season.url = "/".join(element[0].split("/")[3:-1])
                    caps.append(element[1])
                    if haveSubtitle:
                        sub = ".".join(element[1].split(".")[:-1])+".srt"
                        subtitle.append(sub)
                else:
                    caps.append(element[1])
                    if haveSubtitle:
                        sub = ".".join(element[1].split(".")[:-1])+".srt"
                        subtitle.append(sub)
            season.caps = caps.copy()
            season.subtitle = subtitle.copy()
            serieModel.temporadas.append(season)
            
            self.insertSeasonToSupabase(serieModel)
            return serieModel
        except:
                self.logoutWithSupabase()
                raise Exception('Ha ocurrido un error')
    
    def getMultiSeasonMedia(self,serieUrl:str,haveSubtitle:str,name:str,poster:str,portada:str,description:str,populate:float,trailer:str)->SerieModel:
        try:
            serieModel = SerieModel(self.getSupabaseId(),name,portada,poster,description,populate,trailer,[])
            season = SeasonModel(caps=[],name='',subtitle=[],url='')
            caps = []
            subtitle = []
            elementActual = ""
            for element in get_links(url=serieUrl,only_videos=True):
                if(len(elementActual) == 0):
                    elementActual = tuple(element)[2]
                    season.name =  elementActual.replace("/","")
                    season.url = "/".join(element[0].split("/")[3:-1])
                    caps.append(element[1])
                    if haveSubtitle:
                        sub = ".".join(element[1].split(".")[:-1])+".srt"
                        subtitle.append(sub)
                    else:
                        subtitle.append("")
                elif elementActual != tuple(element)[2]:
                    if len(caps) > 0:
                        season.caps = caps.copy()
                        season.subtitle = subtitle.copy()
                        serieModel.temporadas.append(season)
                    caps.clear()
                    subtitle.clear()
                    season = SeasonModel(caps=[],name='',subtitle=[],url='')
                    elementActual = tuple(element)[2]
                    season.name = elementActual.replace("/","")
                    season.url = "/".join(element[0].split("/")[3:-1])
                    caps.append(element[1])
                    if haveSubtitle:
                        sub = ".".join(element[1].split(".")[:-1])+".srt"
                        subtitle.append(sub)
                    else:
                        subtitle.append("")
                elif elementActual == tuple(element)[2]:
                    caps.append(element[1])
                    if haveSubtitle:
                        sub = ".".join(element[1].split(".")[:-1])+".srt"
                        subtitle.append(sub)
                    else:
                        subtitle.append("")
            if elementActual:
                season.caps = caps.copy()
                season.subtitle = subtitle.copy()
                serieModel.temporadas.append(season)
            self.insertSeasonToSupabase(serieModel)
            return serieModel
        except:
            self.logoutWithSupabase()
            raise Exception('Ha ocurrido un error')
    
    def insertSeasonToSupabase(self,serie:SerieModel):
        try:
            # Insertar serie
            self.supabase.table("series").insert({"id":serie.id,"name":serie.name,"poster":serie.poster,"portada":serie.portada,"populate":serie.populate,"description":serie.description,"trailer":serie.trailer}).execute()

            # Insertar temporadas
            for season in serie.temporadas:
                uuidSerie = uuid.uuid4().hex
                self.supabase.table("seasons").insert({"id":uuidSerie,"name":season.name,"url":season.url,"series_id":serie.id}).execute()

                # Insertar episodios
                for episode,subtitle in zip(season.caps,season.subtitle):
                    self.supabase.table("episodes").insert({"name":episode,"subtitle":subtitle,"season_id":uuidSerie}).execute()
            self.logoutWithSupabase()
        except:
            self.logoutWithSupabase()
            raise Exception('Ha ocurrido un error')
            
        