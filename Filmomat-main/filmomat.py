# Code by Ricardo Bandeira
# functions for filmomat
# -------------------------
# 2022.11.23 - Init Commit

from tmdbv3api import TMDb, Movie

intMaxCompanies=1
intMaxGenres=2
intMaxCasts=3

myTMDB_APIKEY = '13c3fb95f6bf0ec08852cb5eedb568ab'
myTMDB_LANGUAGE = 'en'
myTMDB_DEBUG = True

def createConnection2TMDb():
  tmdb = TMDb()
  tmdb.api_key = myTMDB_APIKEY
  tmdb.language = myTMDB_LANGUAGE
  tmdb.debug = myTMDB_DEBUG
  movie = Movie()
  return movie

def getMovie(movieID,searchPattern='Recommendation'):
  movie = createConnection2TMDb()
  if searchPattern.lower() == 'similar':
      return movie.similar(movieID)
  elif searchPattern.lower() =='details':
      return movie.details(movieID)
  else:
      return movie.recommendations(movieID)

def getMovieData(movieDetail,dataField='name',dataTyp='Genre'):
  global intMaxGenres
  global intMaxCompanies
  global intMaxCasts
  
  vecNames=[]
  if dataTyp.lower() == 'cast':
    if len(movieDetail.casts.cast) < intMaxCasts:
      intMaxLoop=len(movieDetail.casts.cast)
    else:
      intMaxLoop=intMaxCasts
  elif dataTyp.lower() == 'company':
    if len(movieDetail.production_companies) < intMaxCompanies:
      intMaxLoop=len(movieDetail.production_companies)
    else:
      intMaxLoop=intMaxCompanies
  else:
    if len(movieDetail.genres) < intMaxGenres:
      intMaxLoop=len(movieDetail.genres)
    else:
      intMaxLoop=intMaxGenres

  for i in range(0,intMaxLoop):
    if dataTyp.lower() == 'cast':
      if dataField.lower() == 'name':
        vecNames.append(movieDetail.casts.cast[i].name)
      else:
        vecNames.append(movieDetail.casts.cast[i].id)
    elif dataTyp.lower() == 'company':
      if dataField.lower() == 'name':
        vecNames.append(movieDetail.production_companies[i].name)
      else:
        vecNames.append(movieDetail.production_companies[i].id)
    else:
      if dataField.lower() == 'name':
        vecNames.append(movieDetail.genres[i].name)
      else:
        vecNames.append(movieDetail.genres[i].id)
  return vecNames

def getMoviesAllDetails(movies):
  vecMovies=[]
  
  if type(movies) != list:
    movie = movies
    movies = []
    movies.append(movie)

  for movie in movies:
    vecMovie=[]
    movieDetails = getMovie(movie.id,'details')
    movieGenre = getMovieData(movieDetails,'id','Genre')
    movieCast = getMovieData(movieDetails,'id','Cast')
    movieCompany = getMovieData(movieDetails,'id','Company')
    vecMovie.append(movie.id)
    vecMovie.append(movieGenre)
    vecMovie.append(movieCast)
    vecMovie.append(movieCompany)
    vecMovies.append(vecMovie)
  return vecMovies


def matchDetailed(selectedMovieA,selectedMovieB,searchPattern,loops=1):
  movieID = "0"
 
  vecMovieA = getMoviesAllDetails(getMovie(selectedMovieA,'details'))[0] 
  vecMovieB = getMoviesAllDetails(getMovie(selectedMovieB,'details'))[0]
  
  vecMatchedGenre = list(set(vecMovieA[1]) & set(vecMovieB[1])) 
  vecMatchedCast = list(set(vecMovieA[2]) & set(vecMovieB[2]))
  vecMatchedCompany = list(set(vecMovieA[3]) & set(vecMovieB[3]))

  if len(vecMatchedGenre) > 0 or len(vecMatchedCompany) >0 or len(vecMatchedCast)>0:
    moviesA = getMovie(selectedMovieA,searchPattern) + getMovie(selectedMovieB,searchPattern)
    vecMovies=getMoviesAllDetails(moviesA)

    vecMatched = []
    for vecMovie in vecMovies:
      if vecMovie[0] != vecMovieA[0] and vecMovie[0] != vecMovieB[0]:
        vecMatched.append(vecMovie)
    vecMovies=[]
    vecMovies=vecMatched
    vecMatched=[]

    if len(vecMatchedGenre) > 0: 
      vecMatched = []
      for vecMovie in vecMovies:
        if len(list(set(vecMatchedGenre) & set(vecMovie[1]))) > 0:
          vecMatched.append(vecMovie)
      if len(vecMatched) > 0:
        vecMovies=[]
        vecMovies = vecMatched
    
    if len(vecMatchedCompany) > 0:
      vecMatched=[]
      for vecMovie in vecMovies:
        if len(list(set(vecMatchedCompany) & set(vecMovie[3]))) > 0:
          vecMatched.append(vecMovie)
      if len(vecMatched) > 0:
        vecMovies=[]
        vecMovies = vecMatched
            
    if len(vecMatchedCast) > 0:
      vecMatched=[]
      for vecMovie in vecMovies:
        if len(list(set(vecMatchedCast) & set(vecMovie[2]))) > 0:
            vecMatched.append(vecMovie)
        if len(vecMatched) > 0:
          vecMovies=[]
          vecMovies = vecMatched
          vecMatched=[]

    movieID=vecMovies[0][0]
  return movieID


def matchMovies(selectedMovieA,selectedMovieB,searchPattern,loops):
  movieID = "0"
  vecMovie=[]
  vecMovieA=[]
  vecMovieB=[]
  
  moviesA = getMovie(selectedMovieA,searchPattern)
  moviesB = getMovie(selectedMovieB,searchPattern)
  
  if loops > 1:
    for movie in moviesA:
      moviesAA  = getMovie(movie.id,searchPattern)
      for movieA in moviesAA:
        vecMovieA.append(movieA.id)
    for movie in moviesB:
      moviesBB  = getMovie(movie.id,searchPattern)
      for movieB in moviesBB:
        vecMovieB.append(movieB.id)
  else:       
    for movie in moviesA:
      vecMovieA.append(movie.id)
    for movie in moviesB:
      vecMovieB.append(movie.id)

  vecMovie = list(set(vecMovieA) & set(vecMovieB))

  if len(vecMovie) > 0:
   movieID = vecMovie[0]
  
  return movieID