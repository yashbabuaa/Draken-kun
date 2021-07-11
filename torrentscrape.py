from py1337x import py1337x

torrents= py1337x(proxy='1337xx.to')

class thirteenX:
  def __init__(self, query, torrentId):
    self.query = query
    self.torrentId = torrentId
    
  def search(query):
    search = torrents.search(query)
    parser = search.get('items')
    result = []
    for i in parser:
      res = []
      res.append(i.get('name')) #name
      res.append(i.get('link')) #link
      res.append(i.get('size')) # size
      result.append(res)
    return result
      
  def get_info(torrentId):
    info = torrents.info(torrentId=torrentId)
    return [info.get('name'), info.get('category'), info.get('leechers'), info.get('seeders'), info.get('magnetLink'), info.get('size')]
    