#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code gives you the past position (lat & lon) of the ISS given a time

@author: Sergio Soler
"""

#Fuente https://codereview.stackexchange.com/questions/164512/current-iss-latitude-longitude-position
#Load
import requests
from time import strftime, localtime
#Librerías para pintar los resultados
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import ciso8601 as cis
import time

session = requests.Session()

#Define the projection (this is just to see the map)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.set_global()

#Clase para determinar la posición
class LatLong:

    #Initializer
    def __init__(self, latitude, longitude, timestamp):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.time = strftime('%T', localtime(timestamp))

    def __str__(self):
        return (
            "<Latitude: {self.latitude}° |"
            " Longitude: {self.longitude}° at {self.time}>").format(self=self)

    __repr__ = __str__

    """
    Pinto el timestamp, la latitud y la longitud
    """
    def pprint(self):
        print('International Space Station position @ {}'.format(self.time))
        print('Latitude: {self.latitude}'.format(self=self))
        print('Longitude: {self.longitude}'.format(self=self))
    
    
    def ppoint(self):
        plt.plot(self.longitude, self.latitude, 'bo', markersize=1, transform=ccrs.Geodetic())
        plt.text(self.longitude + 3, self.latitude - 12, 'ISS',
        horizontalalignment='left',
        transform=ccrs.Geodetic())
        
    """
    Defino la superficie que cubre mmia en rojo
    """
    def mmia(self):
        ax.add_patch(mpatches.Circle(xy=[self.longitude, self.latitude ], radius=1.5,
                                    facecolor='red',
                                    alpha=0.2,
                                    transform=ccrs.PlateCarree())
                 )
            
    """
    Defino la superficie que cubre mxgs en verde
    """
    def mxgs(self):
        ax.add_patch(mpatches.Circle(xy=[self.longitude, self.latitude ], radius=14,
                                    facecolor='green',
                                    alpha=0.2,
                                    transform=ccrs.PlateCarree())
                 )

        plt.show()

"""
Busco una función que convierta un string de fecha en un timestamp
NOTA¡¡ Introduce la fehca en el formato "Anyo-Mes-DiaTHora:Min:Sec" ejemplo
"2014-12-05-T12:30:45"

"""
def parse_date(fecha):
    ts=cis.parse_datetime(fecha)
    return(time.mktime(ts.timetuple()))

"""
Get a JSON with the information of the ISS
INTRODUCE THE DATE IN THE LOCAL EUROPE TIME (SPAIN,FRANCE,GERMANY...)!!!!!!
"""
def _get_data_from_api(fecha):
    response = session.get("https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps="+str(parse_date(fecha))+"&units=kilometers")
    response.raise_for_status()
    return response.json()


def get_past_iss_location(fecha):
    data =_get_data_from_api(fecha)
    return LatLong(data[0]['latitude'],data[0]['longitude'],data[0]['timestamp'])


if __name__ == '__main__':
    fecha="2018-01-03T12:13:00"
    get_past_iss_location(fecha).pprint()
    get_past_iss_location(fecha).ppoint()
    get_past_iss_location(fecha).mmia()
    get_past_iss_location(fecha).mxgs()