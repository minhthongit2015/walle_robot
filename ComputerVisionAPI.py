# coding=utf-8

from CognitiveServicesAPIs import CognitiveServicesAPIs, BaseAPI

class ComputerVisionAPI(CognitiveServicesAPIs):
  key1 = '6f8b924831b54d66aaf566dab950197a'
  key2 = 'd7f13ebf9d534929b263f8e1a8b0f684'

  def __init__(self, apikey=''):
    CognitiveServicesAPIs.__init__(self, apikey=apikey if apikey != '' else self.key1)

  async def analyzeImage(self, imgPath='', imgRaw='', imgUrl='', Celebrities=False, Landmarks=False,
    Categories=False, Tags=False, Description=True, Faces=True, ImageType=False, Color=False, Adult=False, callback=None):
    
    analyzeAPI = BaseAPI('POST', '/vision/v1.0/analyze', {}, '', {}, 'ComputerVisionAnalyze')
    params = {}

    # Xây dựng tham số details
    params['details'] = []
    if Celebrities: params['details'].append('Celebrities')
    if Landmarks: params['details'].append('Landmarks')
    params['details'] = ','.join(params['details'])
    
    # Xây dựng tham số visualFeatures
    params['visualFeatures'] = []
    if Categories: params['visualFeatures'].append('Categories')
    if Tags: params['visualFeatures'].append('Tags')
    if Description: params['visualFeatures'].append('Description')
    if Faces: params['visualFeatures'].append('Faces')
    if ImageType: params['visualFeatures'].append('ImageType')
    if Color: params['visualFeatures'].append('Color')
    if Adult: params['visualFeatures'].append('Adult')
    params['visualFeatures'] = ','.join(params['visualFeatures'])

    analyzeAPI.params = '?' + self.parseParams(params)

    # Đính kèm file ảnh cần phân tích vào API
    if imgPath != '' or imgRaw != '' or imgUrl != '':
      self.attachFile(analyzeAPI, filePath = imgPath, fileRawData = imgRaw, fileUrl = imgUrl)

    await self.request(analyzeAPI, callback=callback)

def test():
  vision = ComputerVisionAPI()
  vision.analyzeImage('./test/test.jpg')

if __name__ == "__main__":
  test()



