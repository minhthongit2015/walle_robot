#!/usr/bin/env python3

from controller import *
from sensors import *
from transporter import *
from ComputerVisionAPI import *
from FaceAPI import *
from picamera import PiCamera
import asyncio
import io
import socket
import struct
import time
import picamera
import threading
import cv2
import numpy

"""
@1 : dữ liệu thời gian thực từ openCV (khung các khuôn mặt)
@2 : dữ liệu phân tích từ Computer Vision API (mô tả khung cảnh)
@3 : dữ liệu phân tích từ Face API ()
"""

async def liveStreaming(socket, main):
  await main.live(socket)

class Main():
  def __init__(self):
    self.transporter = Transporter()
    self.lazer = Lazer(14)
    # self.pirSensor = PIRSensor(4, onchange=self.activeLazer)
    self.comvision = ComputerVisionAPI()
    self.face = FaceAPI()
    self.camera = PiCamera()
    self.camera.hflip = self.camera.vflip = True
    self.face_cascade = cv2.CascadeClassifier('test/haarcascade_frontalface_default.xml')

  async def handsake(self, initParams, socket):
    await socket.send("Hello I'm Wall-E!")
    print("[SYS] > Handsake done")
    parse = initParams.split("@")
    width = int(parse[1])
    height = int(parse[2])
    scale = float(parse[3])
    self.camera.resolution = (int(width*scale), int(height*scale))
    print("[SYS] > Setting Camera resolution: {}x{}".format(int(width*scale), int(height*scale)))
    await self.getListPersonGroups(socket)

  async def getListPersonGroups(self, socket):
    await self.face.getListPersonGroups(callback=lambda rs,api: self.getPersons(rs, api, socket))

  async def getPersons(self, result, api, socket):
    rsObj = self.face.parseResult(result)
    loop = asyncio.get_event_loop()
    #futures = [
    #  (await loop.run_in_executor(None, self.getListPersonInGroup, group['personGroupId'], socket)) for group in rsObj
    #]
    futures = []
    for group in rsObj:
      futures.append(await loop.run_in_executor(None, self.getListPersonInGroup, group['personGroupId'], socket))
    for response in await asyncio.gather(*futures): pass
  
  async def getListPersonInGroup(self, personGroupId, socket):
    await self.face.getListPersonInGroup(personGroupId, callback=lambda rs,api: self.sendListPersonInGroup(rs,api,personGroupId,socket))

  async def sendListPersonInGroup(self, result, api, personGroupId, socket):
    await socket.send('1@' + personGroupId + '@0@' + result.read().decode('utf-8', 'strict'))
  
  async def analyzeImage(self, socket, imgPath='', imgRaw=''):
    loop = asyncio.get_event_loop()
    futures = [
      await loop.run_in_executor(None, self.comAnalyze, socket, imgPath, imgRaw),
      await loop.run_in_executor(None, self.faceAnalyze,socket, imgPath, imgRaw)
    ]
    for response in await asyncio.gather(*futures): pass

  async def comAnalyze(self, socket, imgPath='', imgRaw=''):
    await self.comvision.analyzeImage(imgPath, imgRaw, callback=lambda rs, api: self.sendResult(rs, api, socket))
  async def faceAnalyze(self, socket, imgPath='', imgRaw=''):
    await self.face.analyzeImage(imgPath, imgRaw, callback=lambda rs, api: self.sendResult(rs, api, socket))
  
  async def sendResult(self, result, api, socket):
    rs = result.read().decode("utf-8", "strict") 
    rawImage = self.transporter.sendImage(imgRaw=api.body)
    APIType = '3' if api.name == "FaceDetect" else '2'
    await socket.send(rawImage + ('@' + APIType + '@' + rs))
    if APIType == '3':
      rsObj = self.face.parseResult(responseStr=rs)
      for face in rsObj:
        if face['faceAttributes']['smile'] > 0.5:
          self.lazer.on()
          break
        else: self.lazer.off()
      faceIds = []
      for face in rsObj: faceIds.append(face['faceId'])
      if len(faceIds) > 0:
        await self.face.faceIdentify('group_01', faceIds, callback=lambda rsz, apiz: self.sendPersonInfo(rsz, apiz, socket))

  async def sendPersonInfo(self, result, api, socket):
    rs = result.read().decode("utf-8", "strict")
    rsObj = self.face.parseResult(responseStr=rs)
    self.lazer.off()
    for face in rsObj:
      for person in face['candidates']:
        if person['personId'] == "6fb359fc-b847-4ee1-828c-a221cfa4ca86":
          self.lazer.on()
    await socket.send('1@@4@' + rs)


  async def onCommand(self, command, socket):
    command = command.lower()
    if "door" in command:
      self.lazer.toggle()
      # await self.analyzeImage(socket, imgPath="test/test/kidz.jpg")
    elif "ceiling" == command or u'chế độ phân tích' in command:
      print("[SYS] > Start Analyzing Stream")
      loop = asyncio.get_event_loop()
      futures = [ await asyncio.get_event_loop().run_in_executor(None, self.analyzeStream, socket) ]
      for response in await asyncio.gather(*futures): pass
    elif "stairs" == command:
      print("[SYS] > Start Realtime Streaming")
      loop = asyncio.get_event_loop()
      futures = [ await asyncio.get_event_loop().run_in_executor(None, self.liveStreaming, socket) ]
      for response in await asyncio.gather(*futures): pass
    elif 'hello' in command or u"xin chào" in command:
      self.lazer.on()
      await socket.send("Hello (^_^)!")
    elif u"buổi sáng" in command or "good morning" in command:
      self.lazer.on()
      await socket.send("Good morning sir!")
    elif u"ngủ ngon" in command or "good night" in command or "goodnight" in command:
      self.lazer.off()
      await socket.send("Good night!")
    elif u"tên gì" in command or "what's your name" in command:
      self.lazer.on()
      await socket.send("My name is Wall-E")
    elif u"khỏe không" in command or "how are you" in command:
      self.lazer.on()
      await socket.send("I'm fine! thank you! and you?")
    elif "tạm biệt" in command or "goodbye" in command:
      self.lazer.on()
      await socket.send("Goodbye, you will miss me..")
    elif "i love you" in command:
      self.lazer.on()
      await socket.send("I love you too.. <3")



  async def analyzeStream(self, socket):
    stream = io.BytesIO()
    last = 0
    for cap in self.camera.capture_continuous(stream, 'jpeg'):
      stream.seek(0)
      rawBin = stream.read()

      # Gửi dữ liệu lên server
      sleep = 5 - (time.time()-last)
      last = time.time()
      try:
        if sleep > 0: await asyncio.sleep(sleep)
        await self.analyzeImage(socket, imgRaw=rawBin)
      except Exception as e:
        print(e)
        print("> Connection is closed by Client!")
        break

      # Xóa bộ đệm để chuẩn bị cho frame mới
      stream.seek(0)
      stream.truncate()

  async def liveStreaming(self, socket): # @1
    #self.camera.start_preview()
    stream = io.BytesIO()
    for cap in self.camera.capture_continuous(stream, 'jpeg'):
      stream.seek(0)
      rawBin = stream.read()

      # Nhận diện khuôn mặt trong khung cảnh hiện tại
      buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
      image = cv2.imdecode(buff, 1)
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
      # if len(faces) > 0: print(faces)

      # Gửi dữ liệu lên server
      rawImage = self.transporter.sendImage(imgRaw=rawBin)
      try:
        await socket.send(rawImage+"@1@"+str(faces))
      except Exception as e:
        print("> Connection is closed by Client!")
        break
      stream.seek(0)
      stream.truncate()

instance = Main()