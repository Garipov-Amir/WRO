import tensorflow as tf
import numpy as np
from tensorflow import keras

model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd', loss='mean_squared_error')

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

model = keras.Sequential([
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
    ])

model.compile(optimizer = keras.optimizers.Adam(), 
    loss = 'sparse_categorical_crossentropy',
    metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=40)

test_loss, test_acc = model.evaluate(test_images, test_labels)

model.evaluate(test_images, test_labels)
