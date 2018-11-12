import os
import requests
import csv
import argparse
from bs4 import BeautifulSoup

def grabarArchivo(filePath,tablaProducto):
  with open(filePath, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for linea in tablaProducto:
      writer.writerow(linea)
  return
def consultaDisponibilidad(url,palabraClave,tablaProducto):
    #response = requests.get(url+palabraClave)

    session = requests.Session()
    session.post("http://buscador.tecnomega.com/sesion.php", data=dict(
        ruc="1718760612001",
        codigo="pepp01",
        suc="G1"
    ))
    response = session.get(url+palabraClave)
    print(response.status_code)
    #print(response.content)
    producto = []
    soup = BeautifulSoup(response.content,"html.parser")
    table = soup.findAll(bgcolor="#000000");
    for row in table[1].findAll("tr"):
        if row.tr is not None:
            xx = row.tr.parent.parent.parent
            for xy in xx.findAll("td"):
                if xy.tr is None and xy.string is not None:
                    try:
                        producto.append(xy.string.strip())
                    except AttributeError as error:
                        producto.append(xy.string)
            tablaProducto.append(producto)
            producto = []
    return
#Current directory where is located the script
currentDir = os.path.dirname(__file__)
filename = "dataset.csv"
filePath = os.path.join(currentDir, filename)
url="http://buscador.tecnomega.com/index.php?buscar="
print("¿Producto que desea buscar?")
palabraClave = input()
tablaProducto = []
atributos = ["Codigo articulo","Descripcion articulo","Stock principal","Stock colon","Stock sur","Stock gye norte","Stock gye sur","Precio","Promociones"]
tablaProducto.append(atributos)
consultaDisponibilidad(url,palabraClave,tablaProducto)
grabarArchivo(filePath,tablaProducto)

print("termino FIN")
