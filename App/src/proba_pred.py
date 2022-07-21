import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
from itertools import chain

def preprocess(image): 
  return tf.keras.applications.xception.preprocess_input(image)

def prediction(model, img_path="IMG.png", target_size=(299,299)):
  
  prediction = []
  img = image.load_img(img_path, target_size=target_size)
  img_array = image.img_to_array(img)
  img_batch = np.expand_dims(img_array, axis=0)
  preprocessed_image = preprocess(img_batch)
  prediction = model.predict(preprocessed_image)
  return {prediction.argmax(): prediction}
  
def minimal_normalized_distance(predictions: dict, first_tops=3):
  MND = {}
  for filename, prediction in predictions.items():
    ind = list(np.argpartition(prediction[0], -first_tops)[-first_tops:])
    tops = prediction[0][ind]
    tops = (max(tops)-tops)/max(tops)
    MND[filename] = (min(list(np.partition(tops, 1)[1:])))**2
  return MND

def min_trust_level(predictions: dict, print=False):
  trust_scale = {0:"presque certain",1:"très probable", 2:"probable", 3:"peu problable", 4:"très incertain"}
  MNDs = minimal_normalized_distance(predictions)
  trust = {}
  for filename, MND in MNDs.items():
    if print:
      print("MND : " + str(MND))
    thresholds = [0.8, 0.6, 0.4, 0.2, 0]
    for i in range(5):
      if MND > thresholds[i]:
        trust[filename] = trust_scale[i]
        break
  return trust

def n_most_probable(predictions: dict, first_tops=3):
  from itertools import chain
  import numpy as np
  nfirst_tops = []
  for prediction in predictions.values():
    del_arr = prediction[0]
    for _ in range(first_tops):
      topmax = del_arr.max()
      nfirst_tops.append(np.where(prediction[0]==topmax)[0])
      del_arr = np.delete(del_arr, del_arr == topmax, axis=0)
  return list(chain(*nfirst_tops))


