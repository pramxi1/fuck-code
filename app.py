from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    app.register_blueprint(auth_blueprint)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    
