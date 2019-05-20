from flask import Flask, render_template,abort,request
import os,requests
app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'

port = os.environ['PORT']

language = 'es-ES'
key = os.environ['key']

@app.route('/',methods = ['GET'])
def inicio():
    pay = {'api_key': key,'language': language,'page' : '1'}
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
                if request.form['tipo'] == 'pelis':
                    payload = {'api_key': key,'language': language,'page' : '1','query': tituloform}
                    ultimos = requests.get(URL_BASE_TMDB + 'search/movie',  params = payload)
                    if ultimos.status_code == 200:
                        search = ultimos.json()
                        lista = []
                        listanoimg = []
                        noimg = None
                        for resultado in search['results']:
                            if resultado['poster_path'] != noimg:
                                lista.append({'titulo':resultado['title'],'poster': resultado['poster_path']})
                            else:
                                listanoimg.append({'titulo':resultado['title']})

                        return render_template("busqueda.html", lista = lista, listanoimg = listanoimg)
                else:
                    payload = {'api_key': '53bcf930f2611a01d6a893b431703e79','language': language,'page' : '1','query': tituloform}
                    ultimos = requests.get(URL_BASE_TMDB + 'search/tv',  params = payload)
                    if ultimos.status_code == 200:
                        search = ultimos.json()
                        lista = []
                        listanoimg = []
                        noimg = None
                        for resultado in search['results']:
                            if resultado['poster_path'] != noimg:
                                lista.append({'titulo':resultado['name'],'poster': resultado['poster_path']})
                            else:
                                listanoimg.append({'titulo':resultado['name']})
                        return render_template("busqueda.html", lista = lista,listanoimg = listanoimg)




@app.route('/contacto')
def contacto():
    return render_template("contact.html")

@app.route('/listas')
def listas():
    return render_template("listas.html")

app.run('0.0.0.0',int(port), debug=True)
# app.run(debug=True)
