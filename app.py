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
                                lista.append({'titulo':resultado['title'],'id':resultado['id'],'poster': resultado['poster_path']})
                            else:
                                listanoimg.append({'titulo':resultado['title'],'id':resultado['id']})

                        return render_template("busqueda.html", lista = lista, listanoimg = listanoimg, busqueda = tituloform)
                else:
                    payload = {'api_key': 'key','language': language,'page' : '1','query': tituloform}
                    ultimos = requests.get(URL_BASE_TMDB + 'search/tv',  params = payload)
                    if ultimos.status_code == 200:
                        search = ultimos.json()
                        lista = []
                        listanoimg = []
                        noimg = None
                        for resultado in search['results']:
                            if resultado['poster_path'] != noimg:
                                lista.append({'titulo':resultado['name'],'id':resultado['id'],'poster': resultado['poster_path']})
                            else:
                                listanoimg.append({'titulo':resultado['name'],'id':resultado['id']})
                        return render_template("busqueda.html", lista = lista,listanoimg = listanoimg, busqueda = tituloform)

@app.route('/pelicula/<id>')
def info(id):
    error = None
    payload = {'api_key': key,'language': language}
    info = requests.get(URL_BASE_TMDB + 'movie/' + id,  params = payload)
    if info.status_code == 200:
        infopeli = info.json()
        pelisinfo = {'titulo':infopeli['title'],'poster':infopeli['poster_path'],'sinopsis':infopeli['overview'],'year':infopeli['release_date'],'notatmdb':infopeli['vote_average']}
        return render_template("id.html" , lista = pelisinfo,  error = error)




@app.route('/contacto')
def contacto():
    return render_template("contact.html")

@app.route('/listas')
def listas():
    return render_template("listas.html")

app.run('0.0.0.0',int(port), debug=True)
# app.run(debug=True)
