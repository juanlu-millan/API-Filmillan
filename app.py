from flask import Flask, render_template,abort,request
import os,requests
app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'

# port=os.environ["PORT"]
language = 'es-ES'

@app.route('/',methods = ['GET'])
def inicio():
    pay = {'api_key': '53bcf930f2611a01d6a893b431703e79','language': language,'page' : '1'}
    ultimos = requests.get(URL_BASE_TMDB + 'movie/now_playing',  params=pay)
    if ultimos.status_code == 200:
	      cart = ultimos.json()
	      lista = []
	      for i in cart['results']:
	           lista.append({'titulo':i['title'],'poster': i['poster_path']})
	      return render_template('index.html', lista = lista)

@app.route('/busqueda')
def busqueda():
    return render_template("busqueda.html",)


# app.run('0.0.0.0',int(port), debug=True)
app.run(debug=True)
