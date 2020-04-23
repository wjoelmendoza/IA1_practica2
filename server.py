#! /usr/bin/env python3
from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from logica.main import identificar_escudos,entreno_previo,entreno_envivo
import os
import json
import base64
app = Flask(__name__)

autor1 = {
    "nombre": "Walter",
    "apellido": "Mendoza"
    }

autor2 = {
    "nombre": "Byron",
    "apellido": "López"
    }

@app.route("/")
def index():
    return render_template("index.html",autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"})
@app.route("/entreno-previo")
def previo():
    entreno_previo("")
        
        
    return "LISTO!"


@app.route("/modelos")
def modelos():
    resp = []
    for filename in os.listdir(os.getcwd()+'/Results'):
        inf = decode_info(os.getcwd()+'/Results/'+filename+'/info.json')
        im = convert_image(os.getcwd()+'/Results/'+filename+'/chart.png')
        
        r = {'nombre':filename,'img': im,'info': inf}
        resp.append(r)
    
    return render_template("modelos.html",data=resp)

@app.route("/Entrenar", methods=['POST'])
def Entrenar():
    return render_template("modelos.html")

@app.route("/cargar_imagenes", methods=['POST'])
def cargar_imagenes():
    for filename in os.listdir(os.getcwd()+'/temporales'):
        os.unlink(os.getcwd()+'/temporales/'+filename)
  
    files = request.files
    fl = files.listvalues()
    print(fl)

    for f  in fl:
        for f2 in f:
            rec = './temporales/' + f2.filename
            f2.save(rec)
    conts = [0,0,0,0,0]
    for filename in os.listdir(os.getcwd()+'/temporales'):
        sp = filename.split('_')
        if sp[0] == 'USAC':
            conts[0] +=1
        elif sp[0]== 'Landivar':
            conts[1] += 1
        elif sp[0] == 'Mariano':
            conts[2] += 1
        elif  sp[0] == 'Marroquin':
            conts[3] +=1
        else:
            conts[4] += 1
        
    

  
    x,cont1,cont2,cont3,cont4,cont5,labels = identificar_escudos()
    

    #return json.dumps(x)
    #image = ''
    #with open("./temporales/usac_2.jpg", "rb") as img_file:
    #    image = base64.b64encode(img_file.read()).decode('utf-8')

    #return render_template("resultado.html",img=image,autor1 = {"nombre":"Walter","apellido":"Mendoza"},autor2 = {"nombre":"Byron","apellido":"Lopez"},mensaje=('','',''))
    return create_response_prediccion(x,cont1,cont2,cont3,cont4,cont5,conts,labels)

def create_response_prediccion(preddicion,contusac,contlandivar,contmariano,contmarro,cont,conts,labels):
    resp = ''
    print(preddicion)
    print('LEN PREDICCION::',len(preddicion))
    if len(labels)<6:
        for tup in preddicion:
            resp += '''
            <div class="card-deck">
            <div class="card text-white bg-primary mb-3" style="max-width: 15rem;">
                <div class="card">
                    {}
                    <div class="card-body">
                        <h5 class="card-title">{}</h5>
                    </div>
                </div>
            </div>
            </div>'''.format(get_tag_image(tup[0]),tup[1])
        return resp

    else:
        total = len(preddicion)
        totusac1 = contusac/total
        totusac2 =contusac/conts[0]
        totlandivar1 = contlandivar/total
        totlandivar2 = contlandivar/conts[1]
        totmariano1 = contmariano/total
        totmariano2 = contmariano/conts[2]
        totmarro1 = contmarro/total
        totmarro2 = contmarro / conts[3]
        return '''
        <div class="table-wrapper">
            <table class="table table-striped table-sm">
                <thead>
                    <tr>
                        <th>Universidad</th>
                        <th>exacitud 1</th>
                        <th>exactitud 2</th>
                        <th>supuestos</th>
                        <th>identificados</th>
                        
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>USAC</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                    <tr>
                        <td>Landivar</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        
                    </tr>
                    <tr>
                        <td>Mariano</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        
                    </tr>
                    <tr>
                        <td>Marroquin</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>
                </tbody>
             </table>
        </div> '''.format(totusac1,totusac2,conts[0],contusac,totlandivar1,totlandivar2,conts[1],contlandivar,totmariano1,totmariano2,conts[2],contmariano,totmarro1,totmarro2,conts[3],contmarro)


        

def get_tag_image(path):
    image = ''
    with open(path, "rb") as img_file:
        image = base64.b64encode(img_file.read()).decode('utf-8')
    return ' <img class="card-img-top" src="data:image/jpeg;base64,'+image+'" alt="Card image cap">'

def convert_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
def decode_info(path):
    with open(path, "rb") as file:
        return json.loads(file.read()) 
        
if __name__ == "__main__":
    try:
        os.mkdir("./temporales")
    except FileExistsError:
        pass

    app.run(host="0.0.0.0", port=8080, debug=True)
