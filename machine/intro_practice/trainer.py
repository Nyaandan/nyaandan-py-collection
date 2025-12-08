import tensorflow as tf
from intro_practice.Models import Model_No1

def calculate_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

def train_model(model, data, labels, epochs=10, learning_rate=0.01):
    losses = []
    for epoch in range(epochs):
        loss = train_step(model, data, labels, learning_rate)
        losses.append(loss.numpy())
        if (epoch == 0) or (epoch == epochs - 1):
            print(f"Epoch {epoch + 1}, Loss: {loss.numpy()}")
    return losses

def train_step(model, data, labels, learning_rate):
    with tf.GradientTape() as tape:
        predictions = model(data)
        loss = calculate_loss(labels, predictions)

    model_state = [model.weights, model.biases]
    gradients = tape.gradient(loss, model_state)
    model.apply_gradients(gradients, model_state, learning_rate)
    return loss
