from flask import Flask, render_template,abort,request
import os,requests
app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'

port = os.environ['PORT']

language = 'es-ES'
key = os.environ['key']
noimg = None


@app.route('/',methods = ['GET'])
def inicio():
    pay = {'api_key': key,'language': language,'page' : '1'}
    ultimos = requests.get(URL_BASE_TMDB + 'movie/now_playing',  params=pay)

    if ultimos.status_code == 200:
        cart = ultimos.json()
        lista = []
        for i in cart['results']:
            lista.append({'titulo':i['title'],'poster': i['poster_path'],'id':i['id']})
            # info(int(i['id']),"pelicula")
        return render_template('index.html', lista = lista)

@app.route('/busqueda', methods = ['GET', 'POST'])
def busqueda():
        if request.method == 'GET':
            return render_template("busqueda.html")
        else:
            tituloform = request.form['busqueda']
            if tituloform != '':
                if request.form['selec'] == 'pelicula':
                    payload = {'api_key': key,'language': language,'page' : '1','query': tituloform}
                    ultimos = requests.get(URL_BASE_TMDB + 'search/movie',  params = payload)
                    if ultimos.status_code == 200:
                        search = ultimos.json()
                        lista = []
                        listanoimg = []
                        for resultado in search['results']:
                            if resultado['poster_path'] != noimg:
                                lista.append({'titulo':resultado['title'],'id':resultado['id'],'poster': resultado['poster_path']})
                            else:
                                listanoimg.append({'titulo':resultado['title'],'id':resultado['id']})

                        return render_template("busqueda.html", lista = lista, seleccion = request.form['selec'] , listanoimg = listanoimg, busqueda = tituloform)
                else:
                    payload = {'api_key': key,'language': language,'page' : '1','query': tituloform}
                    ultimos = requests.get(URL_BASE_TMDB + 'search/tv',  params = payload)
                    if ultimos.status_code == 200:
                        search = ultimos.json()
                        lista = []
                        listanoimg = []
                        for resultado in search['results']:
                            if resultado['poster_path'] != noimg:
                                lista.append({'titulo':resultado['name'],'id':resultado['id'],'poster': resultado['poster_path']})
                            else:
                                listanoimg.append({'titulo':resultado['name'],'id':resultado['id']})
                        return render_template("busqueda.html", lista = lista,listanoimg = listanoimg, seleccion = request.form['selec'] , busqueda = tituloform)
            else:
                fallo = "Debes introducir algo en la Búsqueda."
                return render_template("busqueda.html", error = fallo)
@app.route('/<selec>/<id>')
def info(id,selec):
    error = None
    payload = {'api_key': key,'language': language}
    info = requests.get(URL_BASE_TMDB + 'movie/' + id,  params = payload)
    if selec == "pelicula":
        if info.status_code == 200:
            infopeli = info.json()
            pelisinfo = {'titulo':infopeli['title'],'poster':infopeli['poster_path'],'sinopsis':infopeli['overview'],'year':infopeli['release_date'],'notatmdb':infopeli['vote_average']}
            payact = {'api_key': key}
            acto = requests.get(URL_BASE_TMDB + 'movie/' + id +'/credits', params = payact)
            if acto.status_code == 200:
                actores = acto.json()
                reparto = actores['cast']
                infoactor = []
                for actor in reparto:
                    if actor['profile_path'] != noimg:
                        infoactor.append({'actores':actor["name"],'fotos':actor['profile_path']})
                infoactor = infoactor[0:8]
                return render_template("id.html" , lista = pelisinfo, reparto = infoactor ,  error = error)

    else:
        info = requests.get(URL_BASE_TMDB + 'tv/' + id,  params = payload)
        if info.status_code == 200:
            infoserie = info.json()
            seriesinfo = {'titulo':infoserie['name'],'poster':infoserie['poster_path'],'sinopsis':infoserie['overview'],'year':infoserie['first_air_date'],'notatmdb':infoserie['vote_average']}
            payact = {'api_key': key}
            acto = requests.get(URL_BASE_TMDB + 'tv/' + id +'/credits', params = payact)
            if acto.status_code == 200:
                actores = acto.json()
                reparto = actores['cast']
                infoactor = []
                for actor in reparto:
                    if actor['profile_path'] != noimg:
                        infoactor.append({'actores':actor["name"],'fotos':actor['profile_path']})
                infoactor = infoactor[0:8]
                return render_template("id.html" , lista = seriesinfo, reparto = infoactor ,  error = error)



@app.route('/contacto')
def contacto():
    return render_template("contact.html")

@app.route('/listas')
def listas():
    return render_template("listas.html")

app.run('0.0.0.0',int(port), debug=True)
# app.run(debug=True)
