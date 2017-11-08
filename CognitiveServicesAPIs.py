# coding=utf-8

import http.client as httplib
import urllib
import base64
import json

class BaseAPI:
  def __init__(self, method='post', path='', params={}, body='', headers={}, name=''):
    self.method = method
    self.path = path
    self.params = params
    self.headers = headers
    self.body = body
    self.name = name

class CognitiveServicesAPIs:
  """
  Lớp cơ bản hỗ trợ điều khiển luồng API
  """

  _server = "westcentralus.api.cognitive.microsoft.com"
  _apiKey = '5bc766066d5e4b74be61d088a6826a7f'
  _headers = { 'Ocp-Apim-Subscription-Key': _apiKey }

  def __init__(self, server="westcentralus.api.cognitive.microsoft.com", apikey=''):
    self.setServer(server)
    self.addKey(apikey)

  def setServer(self, server):
    self._server = server

  def addKey(self, apikey):
    self._apiKey = apikey
    self._headers = { 'Ocp-Apim-Subscription-Key': self._apiKey }

  def _defaultHandler(self, res):
    res = res.read().decode("utf-8", "strict")
    if len(res) <= 0:
      print("Response nothing")
      return
    try:
      parsed = json.loads(str(res))
      print(json.dumps(parsed, sort_keys=True, indent=2, ensure_ascii=False))
    except:
      print(res)
      raise

  async def request(self, api, callback=None, keepalive=False):
    # Gắn header mặc định vào với header của api
    headers = self._headers
    for header in api.headers: headers[header] = api.headers[header]

    self.conn = httplib.HTTPSConnection(self._server)
    self.conn.request(api.method, api.path + api.params, api.body, headers)

    res = self.conn.getresponse()
    if callback != None: await callback(res, api)
    else: self._defaultHandler(res)

    if not keepalive: self.conn.close()
      
    return self.conn

  ###############
  # Some Helper #
  ###############
  def attachFile(self, api, filePath='', fileRawData='', fileUrl=''):
    if filePath != '':
      api.headers['Content-Type'] = 'application/octet-stream'
      api.headers['Content-Disposition'] = 'attachment; filename=payload.jpg'
      try:
        with open(filePath, 'rb') as f: api.body = f.read()
      except Exception as e:
        print(e)
    elif fileRawData != '':
      api.body = fileRawData
      api.headers['Content-Type'] = 'application/octet-stream'
      api.headers['Content-Disposition'] = 'attachment; filename=payload.jpg'
    elif fileUrl != '':
      api.body = self.paramsToJSON(api.params)
      api.headers['Content-Type'] = 'application/json'

  def parseParams(self, params):
    return urllib.parse.urlencode(params)

  def paramsToJSON(self, params):
    return json.dumps(params)

  def parseResult(self, response=None, responseBytes='', responseStr=''):
    if response != None: return json.loads(response.read().decode("utf-8", "strict"))
    if len(responseBytes) > 0: return json.loads(responseBytes.decode("utf-8", "strict"))
    elif len(responseStr) > 0: return json.loads(responseStr)