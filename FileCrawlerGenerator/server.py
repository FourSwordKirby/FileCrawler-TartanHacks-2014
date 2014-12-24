from flask import Flask, request, render_template
import zipfile
from generator import Cralwer

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def initPage():
    if request.method == "POST":
        unzip()
    return render_template('index.html')

def unzip():
    files = request.files['file']  
    zipFile = zipfile.ZipFile(files)
    contents = zipFile.namelist()
    dungeon_name = "temp" # Name of the dungeon that will be generated
    c = Crawler(contents, dungeon_name)
    #dungeon_data = c.get_string() # String of the entire data
    c.save_map() # Saves dungeon data to dungeon_data.txt

if __name__ == '__main__':
    app.run()
