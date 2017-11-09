# coding=utf-8

from CognitiveServicesAPIs import CognitiveServicesAPIs, BaseAPI
from FaceAPI import FaceAPI
import asyncio


face = FaceAPI()

# asyncio.get_event_loop().run_until_complete(face.analyzeImage('test/kidz1.jpg'))

# asyncio.get_event_loop().run_until_complete(face.createPersonGroup('team', 'group_01', 'Teamz'))
# asyncio.get_event_loop().run_until_complete(face.getListPersonGroups())

asyncio.get_event_loop().run_until_complete(face.createPerson(u"Thầy Tôn Long Phước", 'group_01', 'ThS. Tôn Long Phước - '))

# asyncio.get_event_loop().run_until_complete(face.getListPersonInGroup('group_01'))

# Saved personId
# Trần Nguyễn Minh Thông: 6fb359fc-b847-4ee1-828c-a221cfa4ca86
# Đào Minh Sơn: dbad558b-cacf-4ffc-9303-27598e84ecdc
# Lê Quốc Cương: 86b3170b-2c21-4d09-96b3-90c016e3aa57

# asyncio.get_event_loop().run_until_complete(face.addPersonFace('group_01', 'dbad558b-cacf-4ffc-9303-27598e84ecdc', 'test/son.jpg'))

# asyncio.get_event_loop().run_until_complete(face.trainPersonGroup('group_01'))

# asyncio.get_event_loop().run_until_complete(face.getTrainingStatus('group_01'))

# asyncio.get_event_loop().run_until_complete(face.faceIdentify('group_01', ['fa6600d3-044f-43bb-b3f9-a857eb912c17']))

# asyncio.get_event_loop().run_until_complete(face.getPersonInfo('group_01', "dbad558b-cacf-4ffc-9303-27598e84ecdc"))



