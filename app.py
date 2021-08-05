import pickle
import  pandas as pd
import  numpy as np
from pandas import DataFrame
from flask import Flask,render_template, request, url_for, jsonify , redirect
from flaskext.mysql import MySQL 
import pymysql
import re
import random

app = Flask(__name__)

mysql = MySQL()
   
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'prediction'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

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
        phrase ='<h5>Ce client est suceptible de quitter le service de la carte bancaire</h5>'
    elif  a==0:
        phrase='<h5>Bonne nouvelle !  Ce client ne quittras pas le service de la carte bancaire .</h5>'
    else:
        phrase='<h5>Nous ne parvenons pas à faire de prédiction véfiez vous informations</h5>.'
    return jsonify(phrase)

@app.route("/echantillon",methods=['GET', 'POST'])
def echantillon():
    if request.method == 'POST': 
        def toto():
            nb_ehantillon = int(request.form['input_number'])
            return nb_ehantillon
    return render_template('echantillon.html',toto =toto())


#retourne le datafame selectionner depuis la db au bon format
def fdata_final():
    conn = mysql.connect()
    cursor =conn.cursor()
    nb = 20
    cursor.execute("SELECT  Months_on_book,Months_Inactive_12_mon,Credit_Limit,Avg_Open_To_Buy,Total_Amt_Chng_Q4_Q1,Total_Trans_Amt,Total_Trans_Ct,Total_Ct_Chng_Q4_Q1, Attrition_Flag FROM  client order by rand() LIMIT {} ".format(nb))   
    data = cursor.fetchall()
    cursor.close()

   
    # print (type(data))
    # data=np.array(data)
    # data=pd.DataFrame(data, columns=['Months_Inactive_12_mon','Months_Inactive_12_mon','Credit_Limit','Avg_Open_To_Buy','Total_Amt_Chng_Q4_Q1','Total_Trans_Amt','Total_Trans_Ct','Total_Ct_Chng_Q4_Q1','Attrition_Flag'])
    # data = DataFrame(data)
    return(data)



def retoune_prediction():
    #ouverture du model en lecture
    f = open("model.sav", "rb")
    #chargement du model en lecture
    mdl = pickle.load(f)
    #fermeture du fichier du fichier
    f.close()
    #fonction de prediction 
    data=np.array(fdata_final())
    data=pd.DataFrame(data, columns=['Months_Inactive_12_mon','Months_Inactive_12_mon','Credit_Limit','Avg_Open_To_Buy','Total_Amt_Chng_Q4_Q1','Total_Trans_Amt','Total_Trans_Ct','Total_Ct_Chng_Q4_Q1','Attrition_Flag'])
    data = DataFrame(data)
    
    d = data.drop('Attrition_Flag',axis=1)
    y_pred = mdl.predict(d)
    y_pred = np.array(y_pred)
    y_pred = pd.DataFrame(y_pred, columns=['Prédiction'])
    y_pred =DataFrame(y_pred)
    print(type(y_pred))
    return y_pred



@app.route("/home",methods=['GET', 'POST'])
def output_1():
    # fdata_final() 
    # rst = pd.concat([fdata_final(),retoune_prediction()], axis=1)
    headings = ('Months_Inactive_12_mon','Months_Inactive_12_mon','Credit_Limit','Avg_Open_To_Buy','Total_Amt_Chng_Q4_Q1','Total_Trans_Amt','Total_Trans_Ct','Total_Ct_Chng_Q4_Q1','Attrition_Flag')
    retoune_prediction()
    return render_template('home.html',headings= headings ,data=fdata_final(),y_pred=retoune_prediction())    





   






if __name__ == '__main__':
    app.run(debug=True)







