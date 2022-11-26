# Code by Ricardo Bandeira
# History
# -------------------------
# 2022.11.13 - Init Commit

from flask import Flask, render_template, request
from filmomat import *

vecMoviesTitlelistA= []
vecMoviesIDlistA= []
vecMoviesTitlelistB= []
vecMoviesIDlistB= []
selectedMovieA = ''
selectedMovieB = ''
movieA=Movie()
movieB=Movie()
MovieC=Movie()
movieDetailsA= {}
movieDetailsB= {}
movieDetailsC= {}
vecMovieGenreNamesA= []
vecMovieGenreNamesB= []
vecMovieGenreNamesC= []
vecMovieCastNamesA= []
vecMovieCastNamesB= []
vecMovieCastNamesC= []
vecMovieCompanyNamesA= []
vecMovieCompanyNamesB= []
vecMovieCompanyNamesC= []

def callMatching(selectedMovieA,selectedMovieB):
  movieMachingDetails={}
  if (selectedMovieA != '' and selectedMovieB !=''):
    matchingMovieID = '0'
    ## 
    ## matching / search algorithm
    ##
    matchingMovieID = matchDetailed(selectedMovieA,selectedMovieB,'Recommendation',1)
    if matchingMovieID == '0': 
      matchingMovieID = matchDetailed(selectedMovieA,selectedMovieB,'Similar',1)
    if matchingMovieID == '0': 
      matchingMovieID = matchMovies(selectedMovieA,selectedMovieB,'Recommendation',1) ## Similar Check
    if matchingMovieID == '0':
      matchingMovieID = matchMovies(selectedMovieA,selectedMovieB,'Similar',1)  ## Recommendation Check
    if matchingMovieID == '0':
      matchingMovieID = matchMovies(selectedMovieA,selectedMovieB,'Recommendation',2)  ## Recommendation² Check
    if matchingMovieID == '0':
      matchingMovieID = matchMovies(selectedMovieA,selectedMovieB,'Similar',2)  ## Similar² Check
    if (matchingMovieID != '0'):
      movieMachingDetails=getMovie(matchingMovieID,'Details')
  return movieMachingDetails


def callMovieData(selectedMovieA,selectedMovieB):
  if (selectedMovieA != ''):
    global movieDetailsA,vecMovieCastNamesA,vecMovieCompanyNamesA,vecMovieGenreNamesA
    movieDetailsA = getMovie(selectedMovieA,'Details')
    vecMovieGenreNamesA = getMovieData(movieDetailsA,'Name','Genre')
    vecMovieCastNamesA = getMovieData(movieDetailsA,'Name','Cast')
    vecMovieCompanyNamesA = getMovieData(movieDetailsA,'Name','Company')
    vecMoviesTitlelistA.clear()
    vecMoviesIDlistA.clear()
  if (selectedMovieB != ''):
    global movieDetailsB,vecMovieCastNamesB,vecMovieCompanyNamesB,vecMovieGenreNamesB
    movieDetailsB = getMovie(selectedMovieB,'Details')
    vecMovieGenreNamesB = getMovieData(movieDetailsB,'Name','Genre')
    vecMovieCastNamesB = getMovieData(movieDetailsB,'Name','Cast')
    vecMovieCompanyNamesB = getMovieData(movieDetailsB,'Name','Company')
    vecMoviesTitlelistB.clear()
    vecMoviesIDlistB.clear()
  return

app= Flask(__name__)

@app.route('/', methods=['GET'])
def get_startpage():
    return render_template("index.html",layer=0,ListlenA=0, ListlenB=0)

@app.route('/A/<movieID>', methods=['GET'])
def get_movieA(movieID):
  layer=1
  global selectedMovieA
  selectedMovieA=movieID
  callMovieData(selectedMovieA,selectedMovieB)
  global movieDetailsC
  if len(vecMoviesIDlistA) == 0 and len(vecMoviesIDlistB) == 0:
    layer=2
  return render_template("index.html",layer=layer,ListlenA=len(vecMoviesIDlistA), ListlenB=len(vecMoviesIDlistB),movieA=movieDetailsA,movieB=movieDetailsB,movieC={},moviesListA = vecMoviesTitlelistA, moviesIDA = vecMoviesIDlistA,moviesListB = vecMoviesTitlelistB, moviesIDB = vecMoviesIDlistB, movieGenreA=vecMovieGenreNamesA, movieGenreB=vecMovieGenreNamesB,movieCastA=vecMovieCastNamesA,movieCastB=vecMovieCastNamesB,movieCompanyA=vecMovieCompanyNamesA,movieCompanyB=vecMovieCompanyNamesB,movieGenreC=vecMovieGenreNamesC,movieCompanyC=vecMovieCompanyNamesC,movieCastC=vecMovieCastNamesC)

@app.route('/B/<movieID>', methods=['GET'])
def get_movieB(movieID):
  layer=1
  global selectedMovieB
  selectedMovieB=movieID
  callMovieData(selectedMovieA,selectedMovieB)
  global movieDetailsC
  if len(vecMoviesIDlistA) == 0 and len(vecMoviesIDlistB) == 0:
    layer=2
  return render_template("index.html",layer=layer,ListlenA=len(vecMoviesIDlistA), ListlenB=len(vecMoviesIDlistB),movieA=movieDetailsA,movieB=movieDetailsB,movieC={}, moviesListA = vecMoviesTitlelistA, moviesIDA = vecMoviesIDlistA,moviesListB = vecMoviesTitlelistB, moviesIDB = vecMoviesIDlistB,movieGenreA=vecMovieGenreNamesA, movieGenreB=vecMovieGenreNamesB,movieCastA=vecMovieCastNamesA,movieCastB=vecMovieCastNamesB,movieCompanyA=vecMovieCompanyNamesA,movieCompanyB=vecMovieCompanyNamesB,movieGenreC=vecMovieGenreNamesC,movieCompanyC=vecMovieCompanyNamesC,movieCastC=vecMovieCastNamesC)

@app.route('/C', methods=['GET'])
def get_matched():
  global movieDetailsC
  movieDetailsC = callMatching(selectedMovieA,selectedMovieB)
  vecMovieGenreNamesC=getMovieData(movieDetailsC,'Name','Genre')
  vecMovieCompanyNamesC=getMovieData(movieDetailsC,'Name','Company')
  vecMovieCastNamesC=getMovieData(movieDetailsC,'Name','Cast')
  return render_template("index.html",layer=3,ListlenA=len(vecMoviesIDlistA), ListlenB=len(vecMoviesIDlistB),movieA=movieDetailsA,movieB=movieDetailsB,movieC=movieDetailsC, moviesListA = vecMoviesTitlelistA, moviesIDA = vecMoviesIDlistA,moviesListB = vecMoviesTitlelistB, moviesIDB = vecMoviesIDlistB, movieGenreA=vecMovieGenreNamesA, movieGenreB=vecMovieGenreNamesB,movieCastA=vecMovieCastNamesA,movieCastB=vecMovieCastNamesB,movieCompanyA=vecMovieCompanyNamesA,movieCompanyB=vecMovieCompanyNamesB,movieGenreC=vecMovieGenreNamesC,movieCompanyC=vecMovieCompanyNamesC,movieCastC=vecMovieCastNamesC)

@app.route('/', methods=['POST'])
def post_startpage():
           strSearchMovieA = request.form['seachmovienameA']
           strSearchMovieB = request.form['seachmovienameB']
           tmdb = TMDb()
           tmdb.api_key = myTMDB_APIKEY
           tmdb.language = myTMDB_LANGUAGE
           tmdb.debug = True
           movieA = Movie()
           movieB = Movie()
           
           if strSearchMovieA != '':
            global selectedMovieA
            selectedMovieA = ''
            movieslistA = movieA.search(strSearchMovieA)
            vecMoviesTitlelistA.clear
            vecMoviesIDlistA.clear
            
            for movie in movieslistA:
             vecMoviesTitlelistA.append(movie.title)
             vecMoviesIDlistA.append(movie.id)
           
           if strSearchMovieB != '':
            global selectedMovieB
            selectedMovieB = ''
            movieslistB = movieB.search(strSearchMovieB)
            vecMoviesTitlelistA.clear
            vecMoviesIDlistA.clear
            
            for movie in movieslistB:
             vecMoviesTitlelistB.append(movie.title)
             vecMoviesIDlistB.append(movie.id)
           
           return render_template("index.html",layer=1,ListlenA =len(vecMoviesIDlistA),ListlenB =len(vecMoviesIDlistB),movieA=movieDetailsA,movieB=movieDetailsB, movieC={},moviesListA = vecMoviesTitlelistA, moviesIDA = vecMoviesIDlistA, moviesListB = vecMoviesTitlelistB, moviesIDB = vecMoviesIDlistB,movieGenreA=vecMovieGenreNamesA, movieGenreB=vecMovieGenreNamesB,movieCastA=vecMovieCastNamesA,movieCastB=vecMovieCastNamesB,movieCompanyA=vecMovieCompanyNamesA,movieCompanyB=vecMovieCompanyNamesB)

app.run(host="0.0.0.0",use_reloader = True, debug = True)
 
