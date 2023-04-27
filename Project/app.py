from flask import Flask, render_template, request
from difflib import SequenceMatcher
import os 
import requests
from bs4 import BeautifulSoup
import urllib.request
import datetime
from werkzeug.utils import secure_filename
import shutil
from urllib.request import Request, urlopen

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

def scrap():
    f = open(r"links.txt", "r")
    line = f.readlines()
    for j in range(5):
        print(line[j])
        try:
            req = Request(line[j], headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urlopen(req).read(), features="lxml")
        except:
            pass
        print("Hello") 
        bodyHTML = soup.get_text()
        stamp = datetime.datetime.now().strftime('%d-%H-%M-%S')
        filename = 'data-%s.txt'%stamp

        write_file = open('../Project/data/'+filename, "w+", encoding="utf-8")
        write_file.write(bodyHTML)
        write_file.close()
      
    f.close()

@app.route("/result", methods=['POST', "GET"])
def result():
    output = request.form.to_dict()

    path = "C:/Users/HP/Desktop/Project/data"

    if os.path.exists(path):
        shutil.rmtree(path)
    if request.method == 'POST':
        f = request.files['file']
        print(f)
        file_name = secure_filename(f.filename)
        os.mkdir("../Project/data")

        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print("File does not exist.")
        f.save(os.path.join("../Project/data/", file_name))
      
    print(file_name)

    f = open('../Project/data/'+file_name, "r", encoding="utf8", errors="ignore")
    name = f.readline()
    
    if os.path.exists("../Project/links.txt"):
        os.remove("../Project/links.txt")
    else:
        print("File does not exist.")
    l = open("../Project/links.txt", "w+")
    for j in search(name, num=5, stop=5, pause=2):
        l.writelines(j + "\n")
    l.close()
    scrap()

    f = open(r"../Project/links.txt", "r")
    line = f.readlines()
    array = []
    file_name1 = []
    
    def compare(f2, file_name):
        first_file = open(file_name,"r")
        second_file = open(f2, encoding="utf8")

        file1 = first_file.read()
        file2 = second_file.read()

        ab = SequenceMatcher(None, file1, file2).ratio()
        result = int(ab*100)
        array.append(result)
        file_name1.append(f2)

        f.close()
        second_file.close()

        print(f"{result}% Plagiarized Content {f2}")
    
    path = r"C:\Users\HP\Desktop\Project\data"

    os.chdir(path)

    for file in os.listdir():
        if file.endswith(".txt"):
            compare(file, file_name)
    
    return render_template('result.html', array=array, file_name=line, length=len(array))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
