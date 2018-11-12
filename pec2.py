import os
import requests
import csv
import argparse
from bs4 import BeautifulSoup

# Funcion para grabar archivo
def grabarArchivo(archivo,tablaProducto):
  with open(archivo, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for linea in tablaProducto:
      writer.writerow(linea)
  return
# funcion para consular productos
def consultaDisponibilidad(url,palabraClave,tablaProducto):
    # iniciamos sesion en la pagina web
    session = requests.Session()
    session.post("http://buscador.tecnomega.com/sesion.php", data=dict(
        ruc="1718760612001",
        codigo="pepp01",
        suc="G1"
    ))
    response = session.get(url+palabraClave)
    print(response.status_code)
    producto = []
    soup = BeautifulSoup(response.content,"html.parser")
    table = soup.findAll(bgcolor="#000000");
    # Recorremos los tags que necesitamos para el dataset
    for row in table[1].findAll("tr"):
        if row.tr is not None:
            xx = row.tr.parent.parent.parent
            for xy in xx.findAll("td"):
                if xy.tr is None and xy.string is not None:
                    try:
                        # Eliminamos los espacios en blanco generados al inicio y final de cada atributo del articulo
                        producto.append(xy.string.strip())
                    except AttributeError as error:
                        # En caso de error no se elimina ningun espacio
                        producto.append(xy.string)
            # Se carga los datos en la tablaProducto
            tablaProducto.append(producto)
            producto = []
    return
# Directorio del script
dir_dataset = os.path.dirname(__file__)
dataset = "dataset.csv"
archivo_dataset = os.path.join(dir_dataset, dataset)
# Url para hacer el raspado web.
url="http://buscador.tecnomega.com/index.php?buscar="
# referencia de articulo a buscar
print("¿Producto que desea buscar?")
palabraClave = input()
tablaProducto = []
atributos = ["Codigo articulo","Descripcion articulo","Stock principal","Stock colon","Stock sur","Stock gye norte","Stock gye sur","Precio","Promociones"]
tablaProducto.append(atributos)
consultaDisponibilidad(url,palabraClave,tablaProducto)
grabarArchivo(archivo_dataset,tablaProducto)

print("termino FIN")
