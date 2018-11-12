import os
import requests
import csv
import argparse
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
#Parse command line arguments
#parser = argparse.ArgumentParser()
#parser.add_argument("--startDate", help="Enter start date of interval")
#parser.add_argument("--endDate", help="Enter end date of interval")
#args = parser.parse_args()
#Function to get prices of webpage
def queryPrices( queryURL, paramsValues,headersValues,elementList,date2Filter ):
  paramsValues['fecha']=date2Filter
  response= requests.post(queryURL, data = paramsValues, headers=headersValues)
  soup = BeautifulSoup(response.text,"html.parser")
  table=soup.find('table');
  currentIndex=0
  for row in table.findAll("tr"):
    cells = row.findAll('td')
    if (currentIndex > 0):
      #This is because exists rowspan, if not use the previous category
      if len(cells)==5:
        category=cells[0].find(text=True)
        product=cells[1].find(text=True)
        minPrice=cells[2].find(text=True)
        avgPrice=cells[3].find(text=True)
        maxPrice=cells[4].find(text=True)
      else:
        product=cells[0].find(text=True)
        minPrice=cells[1].find(text=True)
        avgPrice=cells[2].find(text=True)
        maxPrice=cells[3].find(text=True)
      element=[date2Filter,category,product,minPrice,avgPrice,maxPrice]
      elementList.append(element)
    currentIndex=currentIndex+1
  return
def consultaDisponibilidad(url,palabraClave,tablaProducto):
    response = requests.get(url+palabraClave)
    print(response.status_code)
    print(response.headers)
    producto = []
    #print(response.content)
    #soup = BeautifulSoup(response.text,"html.parser")
    soup = BeautifulSoup(response.content)
    table = soup.find(bgcolor="#000000");
    for row in table.findAll("tr"):
        #cells = row.find(valign="middle")
        #if (cells.tdprint(cells)
        if row.tr is not None:
            xx = row.tr.parent.parent.parent
            for xy in xx.findAll("td"):
                if xy.tr is None and xy.string is not None:
                    #if xy.string[0] == " ":
                    try:
                        #print(xy.string.strip())
                        producto.append(xy.string.strip())
                    except AttributeError as error:
                        #print(xy.string)
                        producto.append(xy.string)
                    #else:
                    #    print(xy.string)
                    #print(xy.find(text=True))
            tablaProducto.append(producto)
            producto = []
            #print("--------------------------------------------------")
    return
#Current directory where is located the script
currentDir = os.path.dirname(__file__)
filename = "dataset.csv"
filePath = os.path.join(currentDir, filename)
url="http://buscador.tecnomega.com/index.php?buscar="
palabraClave="proc"
currentDate=''
headerValues={}
formData={}
#Set the header values of HTTP Request
headerValues['Origin']='http://buscador.tecnomega.com/index.php'
headerValues['Referer']='http://buscador.tecnomega.com/index.php'
headerValues['Content-Type']='text/html'
headerValues['X-Requested-With']='XMLHttpRequest'
tablaProducto = []
consultaDisponibilidad(url,palabraClave,tablaProducto)
print(tablaProducto)
#print(headerValues)
#headerValues['x-elastica_gw']='2.43.0'
#Set the POST values of HTTP Request
"""formData['mercado']='*'
formData['desde']='01/11/2017'
formData['hasta']='08/11/2017'
formData['periodicidad']='dia'
formData['ajax']='true'
formData['__ajax_carga_final']='consulta'
formData['fecha']='08/11/2017'
formData['variables[0]']='precio_min'
formData['variables[1]']='precio_prom'
formData['variables[2]']='precio_max'
formData['productos[0]']='0104'#Papa
formData['productos[1]']='0611'#Limon
formData['productos[2]']='1001'#Aceite
formData['productos[3]']='0204'#Ajo
formData['productos[4]']='0207'#Apio
formData['productos[5]']='0401'#Arroz
formData['productos[6]']='1005'#Azucar
formData['productos[7]']='0212'#Cebolla
formData['productos[8]']='1105'#Huevos
formData['productos[9]']='1104'#Leche
formData['productos[10]']='1301'#Pollo
formData['productos[11]']='0228'#Tomate
formData['productos[11]']='0105'#Yuca
formData['productos[11]']='0230'#Zanahoria
#Set the startDate and endDate
startDate = datetime.strptime(args.startDate, "%d/%m/%Y")
endDate = datetime.strptime(args.endDate,"%d/%m/%Y")
priceList=[]
headerList=["Fecha","Producto","Variedad","Precio Mínimo","Precio Promedio","Precio Máximo"]
priceList.append(headerList)
while startDate <= endDate:
  currentDate = startDate.strftime('%d/%m/%Y')
  print ("Generating dataset of %s" %  currentDate)
  queryPrices(sisapUrl,formData,headerValues,priceList,currentDate)
  startDate = startDate + timedelta(days=1)

with open(filePath, 'w', newline='') as csvFile:
  writer = csv.writer(csvFile)
  for priceElement in priceList:
    writer.writerow(priceElement)"""
print("termino")
