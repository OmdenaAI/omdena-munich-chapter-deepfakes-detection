from PIL import Image
import urllib3, os, io, time
import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import glob, cv2
from keras_cv_attention_models import convnext
from keras_cv_attention_models import mobilenetv3

#images_to_predict=[]
ModelLabelList=[]

MODEL_PATH = './modelfile/model.h5'
LABELS_PATH = './modelfile/model_label.txt'


def load_labels():
    with open(os.path.abspath(LABELS_PATH)) as f:
        labellist = f.read().splitlines() 
    return labellist

def normalize(image):
    image = tf.cast(image, tf.float32)
    image = tf.keras.applications.imagenet_utils.preprocess_input(image, mode='torch')
    return image

def imagepreprocessing(image):
    images_to_predict=[]
    img  = cv2.resize(image, (160, 160))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    images_to_predict.append(img)
    images_to_predict = np.array(images_to_predict)
    return images_to_predict

def modelpredict(model, model_labels, upload_image):
    predicted_labels = model.predict(upload_image)
    predicted_labels[predicted_labels<0.5]=0
    predicted_labels[predicted_labels>=0.5]=1
    #return str(ModelLabelList[int(predicted_labels.flatten()[0])]) + ' as ' + str(predicted_labels.flatten())
    return str(ModelLabelList[int(predicted_labels.flatten()[0])])

@st.cache_resource
def get_model(path):
    # Inputs, note the names are equal to the dictionary keys in the dataset
    image = tf.keras.layers.Input((160, 160, 3), name='image', dtype=tf.uint8)
    # Normalize Input
    image_norm = normalize(image)
    # CNN Prediction in range [0,1]
    x = mobilenetv3.MobileNetV3Large075(
        input_shape=(160, 160, 3),
        pretrained='imagenet',
        num_classes=0,
    )(image_norm)
    # Average Pooling BxHxWxC -> BxC
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    # Dropout to prevent Overfitting
    x = tf.keras.layers.Dropout(0.1)(x)
    # Output value between [0, 1] using Sigmoid function
    outputs = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    # Define model with inputs and outputs
    model = tf.keras.models.Model(inputs=image, outputs=outputs)
    # Load pretrained Model Weights
    model.load_weights(path)
    # Set model non-trainable
    model.trainable = False
    # Compile model
    model.compile()
    return model


model = get_model(os.path.abspath(MODEL_PATH))
ModelLabelList= load_labels()
image_file = st.file_uploader("Upload a color image to detect if its fake or real", type=["jpg","png"])
st.set_option('deprecation.showfileUploaderEncoding', False)
if image_file is None:
    st.text("Please upload a color image")
else:
    imageobj=Image.open(image_file)
    st.image(imageobj)
    img_arr = np.array(imageobj) 
    image_np_array =imagepreprocessing(img_arr)
    predicted_labels = modelpredict(model, ModelLabelList, image_np_array)
    #st.header(f"The uploaded image is {predicted_labels}")
    st.info(f"### The uploaded image is {predicted_labels}")
