import imdb 

ia = imdb.IMDb()

def movieid_search(query):
  id_search = ia.search_movie(query)
  return id_search 
  
def movie_search(query, list_of_search=False):
  id_list = movieid_search(query)
  first_res = ia.get_movie(id_list[0].movieID)
  url = ia.get_imdbURL(id_list[0])
  res = []
  res.append(first_res.get('cover url'))
  res.append(first_res.get('title'))
  res.append(first_res.get('rating'))
  res.append(first_res.get('genres'))
  res.append(first_res.get('runtime'))
  res.append(first_res.get('year'))
  res.append(first_res.get('kind'))
  res.append(first_res.get('plot'))
  res.append(url)
  #print(first_res)
  if list_of_search==True:
    return res, id_list 
  else:
    return res
  
