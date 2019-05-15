from flask import Flask, render_template,abort
app = Flask(__name__)

port=os.environ["PORT"]

@app.route('/')
def inicio():
	return render_template("index.html")

@app.route('/busqueda')
def busqueda():
	return render_template("busqueda.html")


app.run('0.0.0.0',int(port), debug=True)
