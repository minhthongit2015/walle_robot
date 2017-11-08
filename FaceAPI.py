
from CognitiveServicesAPIs import CognitiveServicesAPIs, BaseAPI

class FaceAPI(CognitiveServicesAPIs):
  key1 = "fe11114262d64b7eaa145a1d8c41c4d2"
  key2 = "fa7a6b4f7b4e4cdcafdc58dc8fec23f0"

  def __init__(self, apikey=''):
    CognitiveServicesAPIs.__init__(self, apikey=apikey if apikey != '' else self.key1)
    self.name = "Face API"

  async def analyzeImage(self, imgPath='', imgRaw='', imgUrl='', returnFaceId=True, returnFaceLandmarks=False, age=True, gender=True, headPose=True, smile=True, facialHair=True, glasses=True, emotion=True, hair=True, makeup=True, occlusion=True, accessories=True, blur=True, exposure=True, noise=True, callback=None):
    faceDetectAPI = BaseAPI('POST', '/face/v1.0/detect', {}, '', {}, 'FaceDetect')
    params = {}

    if returnFaceId: params['returnFaceId'] = 'true'
    if returnFaceLandmarks: params['returnFaceLandmarks'] = 'true'

    # Xây dựng tham số returnFaceAttributes
    params['returnFaceAttributes'] = []
    if age: params['returnFaceAttributes'].append('age')
    if gender: params['returnFaceAttributes'].append('gender')
    if headPose: params['returnFaceAttributes'].append('headPose')
    if smile: params['returnFaceAttributes'].append('smile')
    if facialHair: params['returnFaceAttributes'].append('facialHair')
    if glasses: params['returnFaceAttributes'].append('glasses')
    if emotion: params['returnFaceAttributes'].append('emotion')
    if hair: params['returnFaceAttributes'].append('hair')
    if makeup: params['returnFaceAttributes'].append('makeup')
    if occlusion: params['returnFaceAttributes'].append('occlusion')
    if accessories: params['returnFaceAttributes'].append('accessories')
    if blur: params['returnFaceAttributes'].append('blur')
    if exposure: params['returnFaceAttributes'].append('exposure')
    if noise: params['returnFaceAttributes'].append('noise')
    params['returnFaceAttributes'] = ','.join(params['returnFaceAttributes'])
    
    # Ghép các tham số lại
    faceDetectAPI.params = '?' + self.parseParams(params)

    # Đính kèm file ảnh cần phân tích vào API
    if  imgPath != ''  or  imgRaw != ''  or  imgUrl != '':
      self.attachFile(faceDetectAPI, filePath = imgPath, fileRawData = imgRaw, fileUrl = imgUrl)
    await self.request(faceDetectAPI, callback=callback)

  async def createPersonGroup(self, name, groupId, userData='', callback=None):
    createGroupAPI = BaseAPI('PUT', '/face/v1.0/persongroups/%s' % groupId, '', '', {}, 'createPersonGroup')
    createGroupAPI.body = self.paramsToJSON( {'name': name, 'userData': userData} )
    await self.request(createGroupAPI, callback=callback)

  async def getListPersonGroups(self, start=0, top=10, callback=None):
    getListPersonGroupsAPI = BaseAPI('GET', '/face/v1.0/persongroups', {}, '', {}, 'getListPersonGroups')
    getListPersonGroupsAPI.params = '?' + self.parseParams({'start': start, 'top': top})
    await self.request(getListPersonGroupsAPI, callback=callback)

  async def createPerson(self, name, personGroupId, userData='', callback=None):
    createPersonAPI = BaseAPI('POST', '/face/v1.0/persongroups/{}/persons'.format(personGroupId), '', '', {}, 'createPerson')
    createPersonAPI.body = self.paramsToJSON( {'name': name, 'userData': userData} )
    await self.request(createPersonAPI, callback=callback)
  
  async def getListPersonInGroup(self, personGroupId, start='', top=1000, callback=None):
    getListPersonInGroupAPI = BaseAPI('GET', '/face/v1.0/persongroups/{}/persons'.format(personGroupId), {}, '', {}, 'getListPersonGroups')
    getListPersonInGroupAPI.params = '?' + self.parseParams({'start': start, 'top': top})
    await self.request(getListPersonInGroupAPI, callback=callback)
  

  async def addPersonFace(self, personGroupId, personId, imgPath='', imgRaw='', imgUrl='', userData='', targetFace=[], callback=None):
    addPersonFaceAPI = BaseAPI('POST',
      '/face/v1.0/persongroups/{}/persons/{}/persistedFaces'.format(personGroupId, personId), {}, '', {}, 'addPersonFace')

    if userData: addPersonFaceAPI.params['userData'] = userData
    if targetFace: addPersonFaceAPI.params['targetFace'] = ','.join(targetFace)
    addPersonFaceAPI.params = '?' + self.parseParams(addPersonFaceAPI.params)

    if imgPath != '' or imgRaw != '' or imgUrl != '':
      self.attachFile(addPersonFaceAPI, filePath = imgPath, fileRawData = imgRaw, fileUrl = imgUrl)
      
    await self.request(addPersonFaceAPI, callback=callback)

  async def trainPersonGroup(self, personGroupId, callback=None):
    trainPersonGroupAPI = BaseAPI('POST', '/face/v1.0/persongroups/{}/train'.format(personGroupId), '', '', {}, 'trainPersonGroup')
    await self.request(trainPersonGroupAPI, callback=callback)

  async def getTrainingStatus(self, personGroupId, callback=None):
    getTrainingStatusAPI = BaseAPI('GET', '/face/v1.0/persongroups/{}/training'.format(personGroupId), '', '', {}, 'getTrainingStatus')
    await self.request(getTrainingStatusAPI, callback=callback)

  #########################################################
  async def faceIdentify(self, personGroupId, faceIds, maxNumOfCandidatesReturned=1, confidenceThreshold=0.5,callback=None):
    faceIdentifyAPI = BaseAPI('POST', '/face/v1.0/identify', '', '', {'Content-Type': 'application/json'}, 'faceIdentify')
    self.personGroupId = personGroupId
    faceIdentifyAPI.body = self.paramsToJSON( {'faceIds': faceIds, 'personGroupId': personGroupId, 'maxNumOfCandidatesReturned': maxNumOfCandidatesReturned, 'confidenceThreshold': confidenceThreshold } )
    await self.request(faceIdentifyAPI, callback=callback)
    
  async def getPersonInfo(self, personGroupId, personId, callback=None):
    getPersonInfoAPI = BaseAPI('GET', '/face/v1.0/persongroups/{}/persons/{}'.format(personGroupId, personId), '', '', {}, 'getPersonInfo')
    await self.request(getPersonInfoAPI, callback=callback)
    

