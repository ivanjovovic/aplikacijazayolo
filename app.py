from flask import Flask, render_template,request,url_for,redirect
from werkzeug.utils import secure_filename
from PIL import Image
from ultralytics import YOLO
import os

app=Flask(__name__)

UPLOAD_FOLDER='static/uploadovane_slike'
ALLOWED_EXTENSIONS={'png','jpg','jpeg','gif'}
MODEL_PATH='kuglice.pt'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

model=YOLO(MODEL_PATH)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
    return render_template('index.html')

@app.route('/uploader',methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)
    file=request.files['file']
    if file.filename=='':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        file.save(filepath)
        results=model(filepath)
        for r in results:
            im_array=r.plot()
            im=Image.fromarray(im_array[...,::-1])
            output_path=os.path.join(app.config['UPLOAD_FOLDER'],'procesirano_'+filename)
            im.save(output_path)
            return render_template('results.html',filename='uploadovane_slike/procesirano_'+filename)
        
if __name__ =='__main__':
    app.run(debug=True)