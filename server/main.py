from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)
data = 0
model = load_model('network.h5')


def transform(array):
    return array.reshape(array.shape[0], 1, 1)


@app.route('/foo', methods=['POST', 'GET'])
def foo():
    global data
    data2 = request.json
    data2 = data2['speed']
    data2 = [float(i) for i in data2]
    data2 = np.array(data2)
    data2 = transform(data2)
    data = round(float(model.predict(data2)[-1, 0]), 2)
    return jsonify(data)


@app.route('/api', methods=['POST', 'GET'])
def api():
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='192.168.43.200')
