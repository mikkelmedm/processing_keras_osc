import argparse
import math
import numpy as np
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
from pythonosc import osc_message_builder
from pythonosc import udp_client
import cv2
import pyautogui
from pythonosc import dispatcher
from pythonosc import osc_server
from PIL import Image
import time
import tensorflow as tf
import random

print("I'm working...")
model = VGG16(weights='imagenet')
graph = tf.get_default_graph()

client = udp_client.SimpleUDPClient("127.0.0.1", 1234)

def send_osc_handler(unused_addr, args, message):
    print("unused: {}".format(unused_addr))
    print("args: {}".format(args))
    print("message: {}".format(message))
    global graph
    with graph.as_default():
        im = pyautogui.screenshot(region=(0, 80, 800, 800))
        im.save('screenshot2.png')
        img_path = 'screenshot2.png'
        img = cv2.resize(cv2.imread(img_path), (224, 224))
        cv2.imwrite("cv_output.png", img)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        

        out = decode_predictions(preds, top=int(message))[0]
    
        print(out)
        output = str(out[0][1])
        cleaned = output.replace("_", " ")
        prob = str("{:.2%}".format(out[0][2]))
        print(cleaned)
        client.send_message("/isadora/1", "{}".format(cleaned))
        client.send_message("/isadora/2", "{}".format(prob))


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/filter", print)
  dispatcher.map("/matt", send_osc_handler, "Matt")

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
