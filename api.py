from flask import Flask, render_template
# from flask_restful import Resource, Api

app = Flask(__name__, template_folder='templates')
# api = Api(app)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)

