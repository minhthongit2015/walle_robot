# coding=utf-8

from CognitiveServicesAPIs import CognitiveServicesAPIs, BaseAPI
from FaceAPI import FaceAPI
import asyncio


face = FaceAPI()

# asyncio.get_event_loop().run_until_complete(face.analyzeImage('test/kidz1.jpg'))

# asyncio.get_event_loop().run_until_complete(face.createPersonGroup('team', 'group_01', 'Teamz'))
# asyncio.get_event_loop().run_until_complete(face.getListPersonGroups())

# asyncio.get_event_loop().run_until_complete(face.createPerson(u"Minh Thông", 'group_01', 'Trần Nguyễn Minh Thông - DHKHMT11A'))

# asyncio.get_event_loop().run_until_complete(face.getListPersonInGroup('group_01'))


# asyncio.get_event_loop().run_until_complete(face.addPersonFace('group_01', '6fb359fc-b847-4ee1-828c-a221cfa4ca86', 'test/kidz.jpg'))

# asyncio.get_event_loop().run_until_complete(face.trainPersonGroup('group_01'))

# asyncio.get_event_loop().run_until_complete(face.getTrainingStatus('group_01'))

asyncio.get_event_loop().run_until_complete(face.faceIdentify('group_01', ['fa6600d3-044f-43bb-b3f9-a857eb912c17']))

# asyncio.get_event_loop().run_until_complete(face.getPersonInfo('group_01', "6fb359fc-b847-4ee1-828c-a221cfa4ca86"))



