
## IMPORTS ##
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
from re import fullmatch
import time
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager import *
import PySimpleGUI as sg
import os
import pandas as pd
from datetime import date
#import undetected_chromedriver as uc

#Por hacer!
#Guardar en caso de que se cierre la pestaña 
#Eliminar las listbox para ingresar nuevos datos -LISTO-

#Variables
list1 = []
numeros = []
browser = "Chrome"
msj = f''
font = ("Arial",15)
#Obtain the user
sg.set_options(font=font)
pcuser=os.getlogin()

def modify_number(phone_no):
    #Quitarmos espacios/guiones/parentesis
    phone_no = phone_no.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return phone_no

def validate_number(phone_no):
    def check_number(number):
        return "+" in number or "_" in number

    if not check_number(number=phone_no):
        raise Exception("Country Code Missing in Phone Number!")

    if not fullmatch(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", phone_no):
        raise Exception("Invalid Phone Number.")
    return True

def set_browser(browser):
    install = lambda dm : dm.install()

    try:
        #Cancelamos el login por mensaje
        opciones = Options()
        
        opciones.add_argument(argument)
        opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
        opciones.add_experimental_option('useAutomationExtension', False)

        #opciones.add_argument('--disable-dev-shm-usage')
        #opciones.capabilities["ignoreProtectedModeSettings"] = True
        #opciones.add_argument("--no-sandbox")
        #opciones.add_experimental_option("detach", True)
        #opciones.add_argument(r"--user-data-dir=C:\\Users\\leash\\AppData\\Local\\Microsoft\\Edge\\User Data")

        if (browser == "Edge"):
            bm = EdgeChromiumDriverManager()
            return webdriver.Edge(service=Service(install(bm)),options=opciones)
        
        elif (browser == "Chrome"):
            #uc.Chrome()
            bm = ChromeDriverManager()      
            #return webdriver.Chrome(executable_path=r'C:\webdriver\chromedriver.exe',options=opciones)
            return webdriver.Chrome(service=Service(install(bm)),options=opciones,executable_path=chromeuser)
        
        elif (browser == "Firefox"):
            bm = GeckoDriverManager()
            return webdriver.Firefox(service=Service(install(bm)))
        
        elif (browser == "Opera"):
            bm = OperaDriverManager()
            return webdriver.Opera(service=Service(install(bm)))
        
        #elif (browser == "Brave"):
        #    bm = ChromeDriverManager(chrome_type=ChromeType.BRAVE)
        #    return webdriver.Chrome(service=Service(install(bm)))
    except:
        raise Exception("Browser not found")


NumEnviar_layout=[[sg.Button("Quitar", enable_events=True, key="-BUTTON2-"),
                         sg.Listbox(values=numeros, size=(30,6), key="-numeros-")]]

NumIngresado_layout = [[sg.Listbox(values=list1, size=(30,6), enable_events=True, key="-LIST-"),
                         sg.Button("Añadir", enable_events=True, key="-BUTTON-")]]

#Layout de la ventana
layout = [[sg.Text("Demo")], 
                [sg.Text('Seleccione su sistema operativo', size=(40,1))],
                [sg.Radio('Windows',"OS", default=True, key="-WINDOWS-"),sg.Radio('MacOS',"OS", default=False, key="-MACOS-")],     
                [sg.Text('Ingresar Numero:', size=(40,1))],
                [sg.Text('En formato +56 9 1234 5678', size=(40,1))],
                [sg.Input(size=30, key='c')],
                [sg.Button(button_text='Ingresar', button_type=7)],
                [sg.Frame("Numeros Ingresados",NumIngresado_layout),sg.Frame("Enviar Mensaje A:",NumEnviar_layout)],
                [sg.Button(button_text='ELIMINAR NUMERO', button_type=7)],
                [sg.Text("Texto a Enviar:"), sg.Multiline (size=(40,6),key='c2'),sg.Button(button_text='Previsualizar', button_type=7)],
                [sg.Button(button_text='Enviar Mensajes', button_type=7)],
                [sg.Cancel("Exit")]]  

window = sg.Window("Whatsapp BOT", layout=layout, background_color="#272533", size=(850, 760),resizable=True)

def crear_csv(numeros):#create a csv based on phone numbers
    #we request the list to create a csv from it   
    df=pd.DataFrame(numeros, columns=["numeros"])
    df["Estado"]=0
    guardar_csv(df)
def actualizar_csv(index,estado): #Update the state of numbers
    fecha=str(date.today())
    df=pd.read_csv("Enviados"+fecha+".csv")
    if estado == "Positivo":
        df.at[index,"Estado"]="Enviado"
    if estado == "Negativo":
        df.at[index,"Estado"] = "No enviado"
    guardar_csv(df)    
def guardar_csv(df):#saves the csv based on date
    fecha=str(date.today())
    df.to_csv("Enviados"+fecha+".csv",index=False)

while True: #ACTION BUTTONS
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    #OS
    if values["-WINDOWS-"] == True: 
        argument=r"--user-data-dir=C:\\Users\\"+pcuser+r"\\AppData\Local\Google\Chrome\User Data"
        chromeuser=r"user-data-dir=C:\\Users\\"+str(pcuser)+r"\\AppData\Local\Google\Chrome\User Data"
    if values["-MACOS-"] == True:
        chromeuser= r"user-data-dir=chrome-data"
        argument = r"--user-data-dir=chrome-data"
    
    if event=="Previsualizar":#PREVIEW
        msj=values['c2']
        sg.Popup("Previsualización del mensaje: \n",msj)

    if event == 'Ingresar': #Ingresamos el numero ingresado a la lista
        list1.append(values['c'])
        window['-LIST-'].update((list1))
        #print(list1)

    if event == "-BUTTON-": #Pasar de ingresador a enviar
        INDEX = int(''.join(map(str, window["-LIST-"].get_indexes())))
        numeros.append(list1.pop(INDEX))
        window["-numeros-"].update(numeros)
        window["-LIST-"].update(list1)
    
    if event == "ELIMINAR NUMERO": #Eliminar numeros de la lista de ingresados
        INDEX = int(''.join(map(str, window["-LIST-"].get_indexes())))
        list1.pop(INDEX)
        window["-numeros-"].update(numeros)
        window["-LIST-"].update(list1)

    if event == "-BUTTON2-":#Pasamos de enviar a ingresados
        INDEX = int(''.join(map(str, window["-numeros-"].get_indexes())))
        list1.append(numeros.pop(INDEX))
        window["-numeros-"].update(numeros)
        window["-LIST-"].update(list1)
        #print(list1)


    if event == "Enviar Mensajes":
        msj=values['c2']
        crear_csv(numeros)
        for contactos in range(len(numeros)):
            phone_no = numeros[contactos]
            phone_no = modify_number(phone_no)

            if (validate_number(phone_no)):

                # Loads browser
                driver = set_browser(browser)
                for i in range(1):
                    try: 
                        #Mensaje!
                        message = msj
                        # Goes to site
                        #print("Abrir url")
                        site = f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}"

                        driver.get(site)
                        time.sleep(6) 
                        
                        #print("url abierta")
                        
                        # Uses XPATH to find a send button
                        element = lambda d : d.find_elements(by=By.XPATH, value="//div//button/span[@data-icon='send']")
                        
                        # Waits until send is found (in case of login)
                        loaded = WebDriverWait(driver, 2200).until(method=element, message="User never signed in")
                        
                        
                        # Loads a send button
                        driver.implicitly_wait(40)
                        send = element(driver)[0]
                        
                        # Clicks the send button
                        send.click()
                        actualizar_csv(contactos,"Positivo")
                        #print("Mensaje Enviado")
                        
                        # Sleeps for 5 secs to allow time for text to send before closing window
                        time.sleep(6) 
                        # Closes window
                        #print("Cerramos La sesion")
                        driver.close()
                    except:
                        actualizar_csv(contactos,"Negativo")
                        time.sleep(6) 
                        driver.close()


        



window.close()