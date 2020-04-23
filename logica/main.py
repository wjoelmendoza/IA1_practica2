from .DatasetsManagment.Udataset import Udataset
from .Logistic_Regression.Model import Model
from .Logistic_Regression.Data import Data
from .Logistic_Regression import Plotter
import matplotlib.pyplot as plt
import skimage.transform
import numpy as np
import cv2
import os
import json
from datetime import datetime


def entrenar_modelos_server_side(alp,lam,it):
    c = Udataset()
    #path = '/Datasets'+name+'.hdf5'
    #Cargando conjuntos de datos
    usac_train_set_x_orig, usac_train_set_y, usac_test_set_x_orig, usac_test_set_y, classes = c.load_dataset(os.getcwd()+'/logica/Datasets','USAC',True)
    landivar_train_set_x_orig, landivar_train_set_y, landivar_test_set_x_orig, landivar_test_set_y, classes = c.load_dataset(os.getcwd()+'/logica/Datasets','Landivar',True)
    mariano_train_set_x_orig, mariano_train_set_y, mariano_test_set_x_orig, mariano_test_set_y, classes = c.load_dataset(os.getcwd()+'/logica/Datasets','Mariano',True)
    marro_train_set_x_orig, marro_train_set_y, marro_test_set_x_orig, marro_test_set_y, classes = c.load_dataset(os.getcwd()+'/logica/Datasets','Marroquin',True)

    #print("---convertir imagenes a un solo arreglo::")
    #print(train_set_x_orig.shape[0])
    usac_train_set_x = usac_train_set_x_orig.reshape(usac_train_set_x_orig.shape[0], -1).T
    usac_test_set_x = usac_test_set_x_orig.reshape(usac_test_set_x_orig.shape[0], -1).T
    landivar_train_set_x = landivar_train_set_x_orig.reshape(landivar_train_set_x_orig.shape[0], -1).T
    landivar_test_set_x = landivar_test_set_x_orig.reshape(landivar_test_set_x_orig.shape[0], -1).T
    mariano_train_set_x = mariano_train_set_x_orig.reshape(mariano_train_set_x_orig.shape[0], -1).T
    mariano_test_set_x = mariano_test_set_x_orig.reshape(mariano_test_set_x_orig.shape[0], -1).T
    marro_train_set_x = marro_train_set_x_orig.reshape(marro_train_set_x_orig.shape[0], -1).T
    marro_test_set_x = marro_test_set_x_orig.reshape(marro_test_set_x_orig.shape[0], -1).T
    
    # Definir los conjuntos de datos
    usac_train_set = Data(usac_train_set_x, usac_train_set_y, 255)
    usac_test_set = Data(usac_test_set_x, usac_test_set_y, 255)
    landivar_train_set = Data(landivar_train_set_x, landivar_train_set_y, 255)
    landivar_test_set = Data(landivar_test_set_x, landivar_test_set_y, 255)
    mariano_train_set = Data(mariano_train_set_x, mariano_train_set_y, 255)
    mariano_test_set = Data(mariano_test_set_x, mariano_test_set_y, 255)
    marro_train_set = Data(marro_train_set_x, marro_train_set_y, 255)
    marro_test_set = Data(marro_test_set_x, marro_test_set_y, 255)
    # Se entrenan los modelos
    
    #print("hipers")
    #print(hipers["values"][1]["apren"],hipers["values"][1]["reg"],hipers["values"][1]["it"])
    print("Entrenando modelo USAC...............")
    usac_model = Model(usac_train_set, usac_test_set,True,alp,lam,it)
    usac_model.training()
    print("Entrenando modelo LANDIVAR...............")
    landivar_model = Model(landivar_train_set, landivar_test_set,True,alp,lam,it)
    landivar_model.training()
    print("Entrenando modelo MARIANO...............")
    mariano_model = Model(mariano_train_set, mariano_test_set,True,alp,lam,it)
    mariano_model.training()
    print("Entrenando modelo MARRO...............")
    marro_model = Model(marro_train_set, marro_test_set,True,alp,lam,it)
    marro_model.training()
    
    
    
    return [usac_model,landivar_model,mariano_model,marro_model]



def get_hiperparametros():
    return [
            {'alp':0.001,"lam":5,"it":10000},
            {'alp':0.001,"lam":10,"it":15000},
            {'alp':0.0001,"lam":5,"it":10000},
            {'alp':0.00001,"lam":10,"it":15000},
            {'alp':0.000001,"lam":15,"it":10000},
        ]

#c = Udataset()
#c.generate_datasets('/home/bj/Documentos/IA/Practica2/Dataset_Escudos',True)
########################################

###################################
#cargo h5 de las imagenes para prueba
#train2_set_x_orig, train2_set_y, test2_set_x_orig, test2_set_y, classes = c.load_dataset('jiji')
#definitive_test_x = train2_set_x_orig.reshape(train2_set_x_orig.shape[0], -1).T
#definitive_test = Data(definitive_test_x,train2_set_y)#LO TENGO QUE DIVIDIR ENTRE 255?
#result = model1.predict(definitive_test.x)
#print(result)
#print(result[0])


def entreno_previo(flag):
    hipers = get_hiperparametros()
    for hip in hipers:
        modelos = entrenar_modelos_server_side(hip['alp'],hip['lam'],hip['it'])
        print("###########LEN MODELOS")
        print(len(modelos))
        imagen = Plotter.show_Model(modelos)
        #GUARDO LA INFO DE LA CORRIDA...
        fp = os.path.join('Results','entreno_'+flag+'_'+str(hip['alp'])+'_'+str(hip['lam'])+'_'+str(hip['it']))
        os.mkdir(fp)
        imagen.savefig(fp+'/chart.png')
        info = [
            {'nombre':'Modelo1','exactitud-entreno':modelos[0].train_accuracy,'exactitud-validacion':modelos[0].test_accuracy},
            {'nombre':'Modelo2','exactitud-entreno':modelos[1].train_accuracy,'exactitud-validacion':modelos[1].test_accuracy},
            {'nombre':'Modelo3','exactitud-entreno':modelos[2].train_accuracy,'exactitud-validacion':modelos[2].test_accuracy},
            {'nombre':'Modelo4','exactitud-entreno':modelos[3].train_accuracy,'exactitud-validacion':modelos[3].test_accuracy},
        ]
        with open(fp+'/info.json','w') as ff:
            json.dump(info,ff)

   

def identificar_escudos():
    #leer la cantidad de imagenes en el archivo
    files = os.listdir(os.getcwd()+'/temporales')
    #CREO EL .H5 PARA EL DATASET DE LAS IMAGENES
    c = Udataset()
    labels = c.generate_dataset_for_prediction()
    return predecir_escudos(labels)
    
def predecir_escudos(labels):
    contusac = 0
    contlandivar = 0
    contmariano = 0
    contmarro = 0
    cont = 0
    usados = []
    resultados = []
    #cargo h5 de las imagenes para prueba
    c = Udataset()
    train_set_x_orig, train_set_y,classes = c.load_dataset(os.getcwd()+'/temporales','dataset-test',False)
    definitive_test_x = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
    definitive_test = Data(definitive_test_x,train_set_y,255)#LO TENGO QUE DIVIDIR ENTRE 255?
    
    modelos = entrenar_modelos_server_side(0.001,5,1500)
     
    results = modelos[0].predict(definitive_test.x)#USAC
    print("RESULTADO PREDICCION::")
    print(results[0])
    for ii in range(len(results[0])):
        res = results[0][ii]
        if res == 1:
            #if ii not in usados:
            resultados.append((labels[ii],'USAC'))
            usados.append(ii)
            contusac += 1
        
    results = modelos[1].predict(definitive_test.x)#LANDIVAR
    print("RESULTADO PREDICCION::")
    print(results[0])
    
    for ii in range(len(results[0])):
        res = results[0][ii]
        if res == 1:
            #if ii not in usados:
            resultados.append((labels[ii],'LANDIVAR'))
            usados.append(ii)
            contlandivar += 1
    
    results = modelos[2].predict(definitive_test.x)#MARIANO
    print("RESULTADO PREDICCION::")
    print(results[0])
    
    for ii in range(len(results[0])):
        res = results[0][ii]
        if res == 1:
            #if ii not in usados:
            resultados.append((labels[ii],'MARIANO'))
            usados.append(ii)
            contmariano += 1
    
    results = modelos[3].predict(definitive_test.x)#MARRO
    print("RESULTADO PREDICCION::")
    print(results[0])
    
    for ii in range(len(results[0])):
        res = results[0][ii]
        if res == 1:
            #if ii not in usados:
            resultados.append((labels[ii],'MARRO'))
            usados.append(ii)
            contmarro += 1
    
    print("En usados::::",usados)
    for index in range(len(labels)):
        if index not in usados:
            print("not in:",index,usados)
            resultados.append((labels[index],'ERROR'))
            cont += 1

    return resultados, contusac,contlandivar,contmariano,contmarro,cont,labels    

    # = model1.predict(definitive_test.x)
#prissnt(result)
#print(result[0])
def entreno_envivo(alp,lam,it):
    modelos = entrenar_modelos_server_side(alp,lam,it)
    imagen = Plotter.show_Model(modelos)
    #GUARDO LA INFO DE LA CORRIDA...
    fp = os.path.join('Results','entreno_envivo_'+str(alp)+'_'+str(lam)+"_"+str(it))
    os.mkdir(fp)
    imagen.savefig(fp+'/chart.png')
    info = [
        {'nombre':'Modelo1','exactitud-entreno':modelos[0].train_accuracy,'exactitud-validacion':modelos[0].test_accuracy},
        {'nombre':'Modelo2','exactitud-entreno':modelos[1].train_accuracy,'exactitud-validacion':modelos[1].test_accuracy},
        {'nombre':'Modelo3','exactitud-entreno':modelos[2].train_accuracy,'exactitud-validacion':modelos[2].test_accuracy},
        {'nombre':'Modelo4','exactitud-entreno':modelos[3].train_accuracy,'exactitud-validacion':modelos[3].test_accuracy},
    ]
    with open(fp+'/info.json','w') as ff:
        json.dump(info,ff)

#entreno_envivo()