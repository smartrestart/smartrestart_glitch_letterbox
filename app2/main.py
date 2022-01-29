

from flask import Flask, render_template, request
from werkzeug import secure_filename
import os, json#, boto3
import subprocess
import pandas as pd
from datetime import date
import csv

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='filein/'
app = Flask(__name__, static_url_path = "/assets", static_folder = "output")

@app.route('/brain_beats_virus')
def upload_file():
   return render_template('richtext.html')
  
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        #print("Before bucket")
        #S3_BUCKET = os.environ.get('S3_BUCKET')
        #print("Entering uploader")
        f = request.files['file']
        f.save('filein/'+f.filename)
        print("request files caught")
        #f = request.form
        #for key in f.keys():
        #    for value in f.getlist(key):
        #        print(key,":",value)
        text1 = request.form['lagebeurteilung']
        text2 = request.form['value_infectious']
        text3 = request.form['viral']
        text4 = request.form['dunkelziffer']
        text5 = request.form['viruskontakt']
        print("Got all the forms")
        with open(os.path.join("app/output/", "text1.txt"), "w") as text_file:
            text_file.write(text1)
        with open(os.path.join("app/output/", "text2.txt"), "w") as text_file:
            text_file.write(text2)
        with open(os.path.join("app/output/", "text3.txt"), "w") as text_file:
            text_file.write(text3)
        with open(os.path.join("app/output/", "text4.txt"), "w") as text_file:
            text_file.write(text4)
        with open(os.path.join("app/output/", "text5.txt"), "w") as text_file:
            text_file.write(text5)
        #subprocess.call("Rscript ./easy_way.R", shell=True)
        #s3 = boto3.resource('s3')
        #s3.Bucket(S3_BUCKET).upload_file('app/output/data.csv','data.csv',ExtraArgs={'ACL':'public-read'})
        #s3.Bucket(S3_BUCKET).upload_file('app/output/lastupdate.csv','lastupdate.csv',ExtraArgs={'ACL':'public-read'})
        #s3.Bucket(S3_BUCKET).upload_file('app/output/text1.txt','text1.txt',ExtraArgs={'ACL':'public-read'})
        #s3.Bucket(S3_BUCKET).upload_file('app/output/text2.txt','text2.txt',ExtraArgs={'ACL':'public-read'})
        #s3.Bucket(S3_BUCKET).upload_file('app/output/text3.txt','text3.txt',ExtraArgs={'ACL':'public-read'})
        #s3.Bucket(S3_BUCKET).upload_file('app/output/text4.txt','text4.txt',ExtraArgs={'ACL':'public-read'})
        #s3.Bucket(S3_BUCKET).upload_file('app/output/text5.txt','text5.txt',ExtraArgs={'ACL':'public-read'})
        run_script()



        return 'Datei wurde erfolgreich gesendet.'

if __name__ == '__main__':
   app.run(debug = True)
    
def run_script():
  print("normal")
  chbase5 = pd.read_excel ("filein/Corona_Virus_2020_actual.xlsx",engine="openpyxl",sheet_name="CH base Impf",skiprows=45,usecols=[0,21,22,24,26,45,49,51,86,88])

  new_cols=["Datum","Viral_Pot","Dunkelziffer","V24","Value_Infectious","V45","Free_Viral","Geimpfte","Viralität_in_Proz","Viralität_pro_X"]
  new_names_map = {chbase5.columns[i]:new_cols[i] for i in range(len(new_cols))}
  chbase5.rename(new_names_map, axis=1, inplace=True)

  chbase5.Viralität_pro_X=chbase5.Viralität_pro_X/25
  chbase5.Viralität_in_Proz=chbase5.Viralität_in_Proz*100
  chbase5['Menschen_mit_Viruskontakt']=chbase5.V45*chbase5.V24*100

  chbase5.Geimpfte=chbase5.Geimpfte.fillna(0)

  print(chbase5.size)
  chbase5.dropna(subset=['Datum'],inplace=True)
  chbase5.dropna(subset=['Viral_Pot'],inplace=True)
  print(chbase5.size)

  chbase5=chbase5[["Datum","Viral_Pot","Value_Infectious","Free_Viral","Viralität_in_Proz","Viralität_pro_X","Dunkelziffer","Menschen_mit_Viruskontakt","Geimpfte"]]


  print("Plus")
  chbaseplus5 = pd.read_excel ("filein/Corona_Virus_2020_actual.xlsx",engine="openpyxl",sheet_name="CH base+ Impf",skiprows=45,usecols=[0,21,22,24,26,45,49,51,86,88])

  new_cols=["Datum","Viral_Pot_Plus","Dunkelziffer_Plus","V24","Value_Infectious_Plus","V45","Free_Viral_Plus","Geimpfte_Plus","Viralität_in_Proz_Plus","Viralität_pro_X_Plus"]
  new_names_map = {chbaseplus5.columns[i]:new_cols[i] for i in range(len(new_cols))}
  chbaseplus5.rename(new_names_map, axis=1, inplace=True)

  chbaseplus5.Viralität_pro_X_Plus=chbaseplus5.Viralität_pro_X_Plus/25
  chbaseplus5.Viralität_in_Proz_Plus=chbaseplus5.Viralität_in_Proz_Plus*100
  chbaseplus5['Menschen_mit_Viruskontakt_Plus']=chbaseplus5.V45*chbaseplus5.V24*100

  chbaseplus5.Geimpfte_Plus=chbaseplus5.Geimpfte_Plus.fillna(0)

  print(chbaseplus5.size)
  chbaseplus5.dropna(subset=['Datum'],inplace=True)
  chbaseplus5.dropna(subset=['Viral_Pot_Plus'],inplace=True)
  print(chbaseplus5.size)

  chbaseplus5=chbaseplus5[["Datum","Viral_Pot_Plus","Value_Infectious_Plus","Free_Viral_Plus","Viralität_in_Proz_Plus","Viralität_pro_X_Plus","Dunkelziffer_Plus","Menschen_mit_Viruskontakt_Plus","Geimpfte_Plus"]]


  print("Opt")
  chbaseopt5 = pd.read_excel ("filein/Corona_Virus_2020_actual.xlsx",engine="openpyxl",sheet_name="CH opt Impf ",skiprows=45,usecols=[0,21,22,24,26,45,49,51,86,88])

  new_cols=["Datum","Viral_Pot_Opt","Dunkelziffer_Opt","V24","Value_Infectious_Opt","V45","Free_Viral_Opt","Geimpfte_Opt","Viralität_in_Proz_Opt","Viralität_pro_X_Opt"]
  new_names_map = {chbaseopt5.columns[i]:new_cols[i] for i in range(len(new_cols))}
  chbaseopt5.rename(new_names_map, axis=1, inplace=True)

  chbaseopt5.Viralität_pro_X_Opt=chbaseopt5.Viralität_pro_X_Opt/25
  chbaseopt5.Viralität_in_Proz_Opt=chbaseopt5.Viralität_in_Proz_Opt*100
  chbaseopt5['Menschen_mit_Viruskontakt_Opt']=chbaseopt5.V45*chbaseopt5.V24*100

  chbaseopt5.Geimpfte_Opt=chbaseopt5.Geimpfte_Opt.fillna(0)

  print(chbaseopt5.size)
  chbaseopt5.dropna(subset=['Datum'],inplace=True)
  chbaseopt5.dropna(subset=['Viral_Pot_Opt'],inplace=True)
  print(chbaseopt5.size)

  chbaseopt5=chbaseopt5[["Datum","Viral_Pot_Opt","Value_Infectious_Opt","Free_Viral_Opt","Viralität_in_Proz_Opt","Viralität_pro_X_Opt","Dunkelziffer_Opt","Menschen_mit_Viruskontakt_Opt","Geimpfte_Opt"]]

  print("Pess")
  chbasepess5 = pd.read_excel ("filein/Corona_Virus_2020_actual.xlsx",engine="openpyxl",sheet_name="CH pess Impf",skiprows=45,usecols=[0,21,22,24,26,45,49,51,86,88])

  new_cols=["Datum","Viral_Pot_Pess","Dunkelziffer_Pess","V24","Value_Infectious_Pess","V45","Free_Viral_Pess","Geimpfte_Pess","Viralität_in_Proz_Pess","Viralität_pro_X_Pess"]
  new_names_map = {chbasepess5.columns[i]:new_cols[i] for i in range(len(new_cols))}
  chbasepess5.rename(new_names_map, axis=1, inplace=True)

  chbasepess5.Viralität_pro_X_Pess=chbasepess5.Viralität_pro_X_Pess/25
  chbasepess5.Viralität_in_Proz_Pess=chbasepess5.Viralität_in_Proz_Pess*100
  chbasepess5['Menschen_mit_Viruskontakt_Pess']=chbasepess5.V45*chbasepess5.V24*100

  chbasepess5.Geimpfte_Pess=chbasepess5.Geimpfte_Pess.fillna(0)

  print(chbasepess5.size)
  chbasepess5.dropna(subset=['Datum'],inplace=True)
  chbasepess5.dropna(subset=['Viral_Pot_Pess'],inplace=True)
  print(chbasepess5.size)

  chbasepess5=chbasepess5[["Datum","Viral_Pot_Pess","Value_Infectious_Pess","Free_Viral_Pess","Viralität_in_Proz_Pess","Viralität_pro_X_Pess","Dunkelziffer_Pess","Menschen_mit_Viruskontakt_Pess","Geimpfte_Pess"]]

  merged = pd.merge(chbase5,chbaseplus5, on="Datum")
  merged2 = pd.merge(chbaseopt5,chbasepess5, on="Datum")
  merged3 = pd.merge(merged,merged2, on="Datum")

  print(merged3.Dunkelziffer)
  print(merged3.Value_Infectious)

  #pd.set_option('float_format', lambda x: '%.10f' % x)
  #pd.set_option('display.float_format', lambda x: '%.10f' % x)
  merged3.to_csv("app/output/data.csv",index=False)#, float_format='%.20f')#,quoting=csv.QUOTE_MINIMAL)

  print(merged3)
  print(merged3.Value_Infectious.dtypes)

  f = open("app/output/lastupdate.csv", "w")
  date_string=date.today().strftime("%Y-%m-%d")
  f.write("lastupdate\n"+date_string)
  f.close()