from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "If a man never contradicts himself, the reason must be that he virtually never says anything at all... Erwin Schrodinger"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
