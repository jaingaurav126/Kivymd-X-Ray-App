from flask import Flask, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
import os

app = Flask(__name__)
model = load_model('chest_xray.h5')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the uploaded file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Load and preprocess the image
    img = image.load_img(file_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    img_data = preprocess_input(x)

    # Make a prediction
    classes = model.predict(img_data)
    result = int(classes[0][0])

    # Clean up the uploaded file
    os.remove(file_path)

    if result == 0:
        return jsonify({'result': 'Person is Affected By PNEUMONIA'})
    else:
        return jsonify({'result': 'Result is Normal'})

if __name__ == '__main__':
    app.run(debug=True)
