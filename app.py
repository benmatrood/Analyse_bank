import pickle
import  pandas as pd
import  numpy as np
from pandas import DataFrame
from flask import Flask,render_template, request, url_for, jsonify , redirect

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/output",methods=['GET','POST'])
def output():

    #ouverture du model en lecture
    f = open("model.sav", "rb")

    #chargement du model en lecture
    mdl = pickle.load(f)

    #fermeture du fichier du fichier
    f.close()

    #fonction de prediction du
    def y_pred(X):
        y_pred = mdl.predict(X)
        return(y_pred)


    #fonction qui retourne le resultat final de la prédiction
    def resultat_finale(data):
        d = np.transpose(DataFrame(data)) 
        a = y_pred(d)
        a = str(a).strip('[]')
        print(int(a))
        return(int(a))
    
    data = request.json.values()

    a= resultat_finale(data)
    if a==1:
        return '<h5>Ce client est suceptible de quitter le service de la carte bancaire</h5>
    elif  a==0:
        return'<h5>Bonne nouvelle !  Ce client ne quittras pas le service de la carte bancaire .</h5>'
    else:
        return'<h5>Nous ne parvenons pas à faire de prédiction véfiez vous informations</h5>.'
    return jsonify(phrase)


if __name__ == '__main__':
    app.run(debug=True)







