from flask import Flask

def create_app():
    app = Flask(__name__)

    # register blueprints, configure database, etc.

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask
 
app = Flask(__name__)
 
@app.route("/")
def hello_world():
    return {"message": "Hello, World!"}