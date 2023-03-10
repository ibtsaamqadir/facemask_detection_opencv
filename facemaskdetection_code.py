"""FaceMaskDetection_Code.ipynb

Automatically generated by Colaboratory.

Mouting the Drive
"""

from google.colab import drive
drive.mount('/content/drive')

"""Changing the directory"""

cd ## Insert the path here to the working directory 

"""Import necessary packages and libraries"""

import cv2
import numpy as np
from keras.models import load_model

"""Importing cv2_imshow because colab does not support cv2.imshow()"""

from google.colab.patches import cv2_imshow

"""Loading the model trained using the Training data set and Keras """

model=load_model("./model2-009.model")

"""Python Script for using builtin webcam using Colab """

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

from IPython.display import Image

"""Using HAARCASCADE Classifier to detect face in the image captured"""

labels_dict={0:'without mask',1:'mask'}
color_dict={0:(0,0,255),1:(0,255,0)}

size = 4
classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

while True:
    try:
      filename = take_photo()
      print('Saved to {}'.format(filename))
  
      # Show the image which was just taken.
      display(Image(filename))
    except Exception as err:
      # Errors will be thrown if the user does not have a webcam or if they do not
      # grant the page permission to access it.
      print(str(err))

    img=cv2.imread('photo.jpg', cv2.IMREAD_UNCHANGED)
    img=cv2.flip(img,1,1)
    mini = cv2.resize(img, (img.shape[1] // size, img.shape[0] // size))
    faces = classifier.detectMultiScale(mini)
    for f in faces:
        (x, y, w, h) = [v * size for v in f]
        img_f = img[y:y+h, x:x+w]
        resized=cv2.resize(img_f,(150,150))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,150,150,3))
        reshaped = np.vstack([reshaped])
        result=model.predict(reshaped)
        #print(result)
        
        label=np.argmax(result,axis=1)[0]
      
        cv2.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
        cv2.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
        cv2.putText(img, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
    cv2_imshow(img)
    cv2.waitKey(0)
    stop = str(input('Press x if you want to stop executing'))
    if stop == 'x': 
        break
cv2.destroyAllWindows()

