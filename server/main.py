from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)
model = load_model('network.h5')


def transform(array):
    return array.reshape(array.shape[0], 1, 1)


@app.route('/foo', methods=['POST', 'GET'])
def foo():
    data = request.json
    data = data['speed']
    data = [float(i) for i in data]
    data = np.array(data)
    data = transform(data)
    data = round(float(model.predict(data)[-1, 0]), 2)
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='192.168.1.17')
