from flask import Flask, jsonify, request, render_template
import pickle
from model import test_model
from PIL import Image
import numpy as np
from scipy import ndimage

# app\template\index.html
app = Flask(__name__)

with open('model_params.pkl', 'rb') as file:
    model_params = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    img = Image.open(file.stream)

    # img.save('pre.png')

    gray_img = img.convert("L")

    # gray_img.save('gray.png')

    gray_img_resized = gray_img.resize((28, 28), Image.LANCZOS)

    # gray_img_resized.save('gray-resized.png')

    com = ndimage.center_of_mass(np.array(gray_img_resized))
    center = np.array(np.array(gray_img_resized).shape) / 2.0
    shift_vector = center - com
    centered_gray_img_resized = ndimage.shift(np.array(gray_img_resized), shift_vector, mode='constant', cval=0)

    # Inverting Image normalize (x / 255)
    img_array = (np.array(centered_gray_img_resized) / 255).reshape(784,1)

    result = test_model(5, img_array, model_params)
    prediction = np.argmax(result)

    probabilities = result.flatten().tolist()
    probabilities = [round(p, 4) for p in probabilities]

    return jsonify(prediction=int(prediction), probabilities=probabilities)

if __name__ == '__main__':
    app.run(debug=True)