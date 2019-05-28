from flask import Flask, render_template,abort,request
import os,requests
app = Flask(__name__)

URL_BASE_TMDB = 'https://api.themoviedb.org/3/'
URL_BASE_OMDB = 'http://www.omdbapi.com/?s'

port = os.environ['PORT']

language = 'es-ES'
key = os.environ['key']
keyomdb = os.environ['keyomdb']
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
                                lista.append({'titulo':resultado['title'],'id':resultado['id'],'fecha':resultado['release_date'],'poster': resultado['poster_path']})
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
                                lista.append({'titulo':resultado['name'],'id':resultado['id'],'fecha':resultado['first_air_date'],'poster': resultado['poster_path']})
                            else:
                                listanoimg.append({'titulo':resultado['name'],'id':resultado['id']})
                        return render_template("busqueda.html", lista = lista,listanoimg = listanoimg, seleccion = request.form['selec'] , busqueda = tituloform)
            else:
                fallo = "Debes introducir algo en la Búsqueda."
                return render_template("busqueda.html", error = fallo)

@app.route('/<selec>/<id>',methods = ['GET', 'POST'])
def info(id,selec):
    error = None
    payload = {'api_key': key,'language': language}
    info = requests.get(URL_BASE_TMDB + 'movie/' + id,  params = payload)
    if selec == "pelicula":
        if info.status_code == 200:
            infopeli = info.json()
            pelisinfo = {'titulo':infopeli['title'],'poster':infopeli['poster_path'],'sinopsis':infopeli['overview'],'year':infopeli['release_date'],'notatmdb':infopeli['vote_average']}
            if pelisinfo['sinopsis'] == '':
                pelisinfo['sinopsis'] = "No hay sinopsis"
            payact = {'api_key': key}
            acto = requests.get(URL_BASE_TMDB + 'movie/' + id +'/credits', params = payact)

            paynotas = {'apikey':keyomdb,'y': infopeli['release_date'][0:4],'t':infopeli['original_title'],'type':'movie'}
            peli = requests.get(URL_BASE_OMDB, params= paynotas )
            if peli.status_code == 200:
                nota=peli.json()
                if nota['Response'] != 'False':
                    puntua = []
                    notas = nota['Ratings']
                    for puntuacion in notas:
                        puntua.append ({'web':puntuacion['Source'],'valor':puntuacion['Value']})
                else:
                    puntua = [{'web':"No hay más votaciones"}]

            if acto.status_code == 200:
                actores = acto.json()
                reparto = actores['cast']
                direccion = actores['crew']

                infoactor = []
                directorinfo = []
                directornoimg = []

                for actor in reparto:
                    if actor['profile_path'] != noimg:
                        infoactor.append({'actores':actor["name"],'fotos':actor['profile_path']})
                for direc in direccion:
                    if direc['job'] == 'Director':
                        if direc['profile_path'] != noimg:
                            directorinfo.append({'director':direc["name"],'fotos':direc['profile_path']})
                        else:
                            directornoimg.append({'director':direc["name"]})
                infoactor = infoactor[0:8]
            return render_template("id.html" ,lista = pelisinfo ,reparto = infoactor ,puntuacion=puntua ,director = directorinfo, directornoimg=directornoimg ,error = error)

    else:
        info = requests.get(URL_BASE_TMDB + 'tv/' + id,  params = payload)
        if info.status_code == 200:
            infoserie = info.json()
            seriesinfo = {'titulo':infoserie['name'],'poster':infoserie['poster_path'],'sinopsis':infoserie['overview'],'year':infoserie['first_air_date'],'notatmdb':infoserie['vote_average']}
            payact = {'api_key': key}
            acto = requests.get(URL_BASE_TMDB + 'tv/' + id +'/credits', params = payact)


            paynotas = {'apikey':keyomdb,'y': infoserie['first_air_date'][0:4],'t':infoserie['original_name'],'type':'series'}
            peli = requests.get(URL_BASE_OMDB, params= paynotas )
            if peli.status_code == 200 and acto.status_code == 200:
                nota=peli.json()
                notas = nota['Ratings']
                actores = acto.json()
                reparto = actores['cast']
                direccion = actores['crew']

                infoactor = []
                puntua = []
                directorinfo = []

                for actor in reparto:
                    if actor['profile_path'] != noimg:
                        infoactor.append({'actores':actor["name"],'fotos':actor['profile_path']})
                infoactor = infoactor[0:8]
                for puntuacion in notas:
                    puntua.append ({'web':puntuacion['Source'],'valor':puntuacion['Value']})
                return render_template("id.html" ,lista = seriesinfo ,reparto = infoactor ,puntuacion=puntua ,error = error)


@app.route('/contacto')
def contacto():
    return render_template("contact.html")

app.run('0.0.0.0',int(port), debug=True)
# app.run(debug=True)
