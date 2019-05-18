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

@app.route('/busqueda', methods = ['GET', 'POST'])
def busqueda():
        if request.method == 'GET':
            return render_template("busqueda.html")
        else:
            tituloform = request.form['busqueda']
            if tituloform != '':
                payload = {'api_key': '53bcf930f2611a01d6a893b431703e79','language': language,'page' : '1','query': tituloform}
                ultimos = requests.get(URL_BASE_TMDB + 'search/movie',  params = payload)
                if ultimos.status_code == 200:
                    search = ultimos.json()
                    lista = []
                    for i in search['results']:
                        lista.append({'titulo':i['title'],'poster': i['poster_path']})
                return render_template("busqueda.html", lista = lista)


# app.run('0.0.0.0',int(port), debug=True)
app.run(debug=True)
