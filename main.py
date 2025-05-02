from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    response = {
        "number": 9633582042,
        "message": "Hello from Flask!",
        "status": "success"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)