#!/usr/bin/env python3

import asyncio
import websockets
import socket
import main

localIP = "0.0.0.0"
bindingPort = 4444

async def WebServerHandler(websocket, path):
  cmd = await websocket.recv()
  print("Recv: {}".format(cmd))
  
  if "wakeup" in cmd:
    await main.instance.handsake(cmd, websocket)
    # asyncio.get_event_loop().run_in_executor(None, main.instance.handsake, cmd, websocket)
  else:
    await main.instance.onCommand(cmd, websocket)
    # asyncio.get_event_loop().run_in_executor(None, main.instance.onCommand, cmd, websocket)

print("Wall-E Websocket server start on {}:{}".format(localIP, bindingPort))

start_server = websockets.serve(WebServerHandler, localIP, bindingPort)
try:
  server = asyncio.get_event_loop()
  server.run_until_complete(start_server)
  server.run_forever()
except KeyboardInterrupt:
  server.close()
  print("[SYS] > Shutdown server...")

