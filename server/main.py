from flask import Flask, request, jsonify

app = Flask(__name__)
data = []
@app.route('/foo', methods=['POST', 'GET'])
def foo():
    global data
    data = request.json
    print(data['speed'])
    print()
    return jsonify(data)

@app.route('/api', methods=['POST', 'GET'])
def api():
    return jsonify(data['speed'][-1])

if __name__ == "__main__":
    app.run(host='192.168.1.17')
