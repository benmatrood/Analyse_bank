import pickle
import  pandas as pd
import  numpy as np
from pandas import DataFrame
from flask import Flask,render_template, request, url_for, jsonify , redirect
import re
import random
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/prediction")
def hello_word():
    return render_template('prediction.html')

@app.route("/output",methods=['GET','POST'])
def output():
    f = open("model.sav", "rb")   
    mdl = pickle.load(f)
    f.close()
    #fonction de prediction du
    def y_pred(X):
        y_pred = mdl.predict(X)
        return(y_pred)
    #fonction qui retourne le resultat final de la prédiction
    def resultat_finale(data):
        a = np.transpose(DataFrame(data)) 
        a = str(y_pred(a)).strip('[]')
        return(int(a))
    a= resultat_finale(request.json.values())
    if a==1:
        phrase ='<h5>Ce client est suceptible de quitter le service de la carte bancaire</h5>'
    elif  a==0:
        phrase='<h5>Bonne nouvelle !  Ce client ne quittras pas le service de la carte bancaire .</h5>'
    else:
        phrase='<h5>Nous ne parvenons pas à faire de prédiction véfiez vous informations</h5>.'
    return jsonify(phrase)

@app.route("/echantillon",methods=['GET', 'POST'])
def echantillon():

    return render_template('echantillon.html')

@app.route("/resultat",methods=['POST'])
def output_1():
    nb = request.form['input_number']
    conn = sqlite3.connect('db.sqlite3')
    cursor =conn.cursor()
    cursor.execute("SELECT  Months_on_book,Months_Inactive_12_mon,Credit_Limit,Avg_Open_To_Buy,Total_Amt_Chng_Q4_Q1,Total_Trans_Amt,Total_Trans_Ct,Total_Ct_Chng_Q4_Q1, Attrition_Flag FROM  data_credit_card order by random() LIMIT {} ".format(int(nb)))  
    data = cursor.fetchall()
    f_data = data
    cursor.close()
    f = open("model.sav", "rb")
    mdl = pickle.load(f)
    f.close()
    data=np.array(data)
    data=pd.DataFrame(data, columns=['Months_on_book','Months_Inactive_12_mon','Credit_Limit','Avg_Open_To_Buy','Total_Amt_Chng_Q4_Q1','Total_Trans_Amt','Total_Trans_Ct','Total_Ct_Chng_Q4_Q1','Attrition_Flag'])
    data = DataFrame(data)
    data = data.drop('Attrition_Flag',axis=1)
    y_pred = mdl.predict(data)
    y_pred = np.array(y_pred)
    y_pred = pd.DataFrame(y_pred)   
    y_pred =DataFrame(y_pred)
    f_data = DataFrame(f_data) 
    v = pd.concat([f_data,y_pred], axis=1)
    headings = ('Months_Inactive_12_mon','Months_Inactive_12_mon','Credit_Limit','Avg_Open_To_Buy','Total_Amt_Chng_Q4_Q1','Total_Trans_Amt','Total_Trans_Ct','Total_Ct_Chng_Q4_Q1','Attrition_Flag','Prediction')
    return render_template('resultat_.html',headings= headings ,data=v.values)    


if __name__ == '__main__':
    app.run(debug=True)







