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

ModelLabelList=[]

MODEL_PATH = './modelfile/model.h5'
LABELS_PATH = './modelfile/model_label.txt'
ALLOWED_EXTENSIONS = ["jpg","png"]
WARNING_MESSAGE='Note: Our model was specifically trained on individual human faces, hence group images, sketches, cartoons and other similar types of images might be misclassified. Also, the deepfake images chosen were generated by 5 specific GANs, namely, AttGan, GDWCT, StarGAN, StyleGAN and StyleGAN2. Deepfake generated by any other GAN might be misclassified too.'


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
    predicted_result = dict();
    predicted_labels = model.predict(upload_image)
    predicted_result_percentage = float(predicted_labels.flatten()[0])
    predicted_labels[predicted_labels<0.5]=0
    predicted_labels[predicted_labels>=0.5]=1
    predicted_result['label'] = model_labels[int(predicted_labels.flatten()[0])]
    if int(predicted_labels.flatten()[0])==0:
        predicted_result['percentage']=round(((1-float(predicted_result_percentage))*100),2)
    if int(predicted_labels.flatten()[0])==1:
        predicted_result['percentage']=round(((float(predicted_result_percentage))*100),2)
    return predicted_result

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

HEADER_STYLE="""<style>
	    [data-testid="stToolbar"]{
	    visibility: hidden;
	    top: -50px;
	    }
        </style>
    """

model = get_model(os.path.abspath(MODEL_PATH))
ModelLabelList= load_labels()
st.markdown(HEADER_STYLE, unsafe_allow_html=True) 
st.title(f"Upload a color image to detect if its fake or real")
image_file = st.file_uploader("", type=ALLOWED_EXTENSIONS)
st.set_option('deprecation.showfileUploaderEncoding', False)
st.warning(WARNING_MESSAGE, icon="⚠️")
if image_file is not None:
    imageobj=Image.open(image_file)
    st.image(imageobj)
    img_arr = np.array(imageobj) 
    image_np_array =imagepreprocessing(img_arr)
    predicted_labels = modelpredict(model, ModelLabelList, image_np_array)
    st.info(f"### The model is {predicted_labels['percentage']}% sure that the image is {predicted_labels['label']}")
