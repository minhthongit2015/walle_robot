# coding=utf-8
"""
Gửi dữ liệu kết quả của các Cognitive Servivice tới máy tính để hiển thị
"""

import base64

class Transporter():
  def __init__(self):
    self.cmdCode = "1@"
  
  def sendImage(self, imgPath='', imgRaw=''):
    rawBase64 = ''
    if imgRaw != '': rawBase64 = imgRaw
    elif imgPath != '':
      try:
        f = open(imgPath, 'rb')
        rawBase64 = f.read()
        print('> img: {} ({} byte)'.format(imgPath, len(rawBase64)))
      except Exception as e:
        print(str(e))
        rawBase64 = ''
        pass
    return self.cmdCode + base64.b64encode(rawBase64).decode()