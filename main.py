from flask import Flask

app = Flask(__name__)

@app.route("/home")
def hello():
    return "Hello world"

app.run(host='0.0.0.0', port=3000)

