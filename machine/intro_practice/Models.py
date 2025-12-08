from typing import Any
import tensorflow as tf
import numpy as np
from keras import Model, Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D

class Model_No1:
    def __init__(self, name, parameters, weights=None, biases=None):
        self.name = name
        self.parameters = parameters
        self.weights = tf.Variable(weights) if weights is not None else None
        self.biases = tf.Variable(biases) if biases is not None else None

    def __call__(self, *args: Any) -> Any:
        return self.weights * args[0] + self.biases if self.weights is not None and self.biases is not None else None

    def train(self, data):
        print(f"Training model '{self.name}' with parameters {self.parameters} on data: {data}")

    def predict(self, input_data):
        print(f"Making predictions with model '{self.name}' on input: {input_data}")
        return [0] * len(input_data)  # Dummy prediction output
    
    def apply_gradients(self, gradients, variables, learning_rate=0.01):
        for grad, var in zip(gradients, variables):
            var.assign_sub(learning_rate * grad)

    def assign_weights(self, weights):
        if self.weights is not None:
            self.weights.assign(weights)

    def assign_biases(self, biases):
        if self.biases is not None:
            self.biases.assign(biases)

    def check_values(self):
        return (f"Model: {self.name}"
        + f"\n\tParameters: {self.parameters}"
        + f"\n\tWeights: {self.weights.read_value().numpy() if self.weights is not None else None}"
        + f"\n\tBiases: {self.biases.read_value().numpy() if self.biases is not None else None}")
    

class SmallModel(Model):
    def __init__(self):
        super(SmallModel, self).__init__()
        self.conv1 = Conv2D(16, kernel_size=(3, 3), activation='relu')
        self.flatten = Flatten()
        self.dense1 = Dense(128, activation='relu')
        self.dense2 = Dense(10, activation='softmax')

    def call(self, x):
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.dense1(x)
        return self.dense2(x)

class BigModel(Model):
    def __init__(self):
        super(BigModel, self).__init__()
        self.conv1 = Conv2D(32, kernel_size=(3, 3), activation='relu')
        self.pool1 = MaxPooling2D(pool_size=(2, 2))
        self.conv2 = Conv2D(64, kernel_size=(3, 3), activation='relu')
        self.pool2 = MaxPooling2D(pool_size=(2, 2))
        self.flatten = Flatten()
        self.dense1 = Dense(128, activation='relu')
        self.dense2 = Dense(10, activation='softmax')

    def call(self, x):
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.flatten(x)
        x = self.dense1(x)
        return self.dense2(x)
