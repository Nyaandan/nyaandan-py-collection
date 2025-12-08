import tensorflow as tf
import keras
from intro_practice.Models import BigModel, SmallModel

mnist = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255.0
x_test = x_test / 255.0
x_train = x_train.reshape((*x_train.shape, 1))
x_test = x_test.reshape((*x_test.shape, 1))
train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(60000).batch(32)
test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)


loss_object = keras.losses.SparseCategoricalCrossentropy()
optimizer = keras.optimizers.Adam()
train_loss = keras.metrics.Mean(name='train_loss')
train_accuracy = keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')
test_loss = keras.metrics.Mean(name='test_loss')
test_accuracy = keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')

@tf.function
def train_step(model, images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables)) if gradients else None
    train_loss(loss)
    train_accuracy(labels, predictions)

@tf.function
def test_step(model, images, labels):
    predictions = model(images, training=False)
    t_loss = loss_object(labels, predictions)
    test_loss(t_loss)
    test_accuracy(labels, predictions)

small_model = SmallModel()
big_model = BigModel()
EPOCHS = 5
header = 'Model\tEpoch\tLoss\tAccuracy\tTest Loss\tTest Accuracy\n'
results = [header]

model = big_model
model_name = "X2-1"

for epoch in range(EPOCHS):
    train_loss.reset_state()
    train_accuracy.reset_state()
    test_loss.reset_state()
    test_accuracy.reset_state()

    for images, labels in train_dataset:
        train_step(model, images, labels)

    for test_images, test_labels in test_dataset:
        test_step(model, test_images, test_labels)

    template = '\n{}\t{}\t{:.4f}\t{:.2f}\t{:.4f}\t{:.2f}'
    entry = (template.format(
        model_name,
        epoch + 1,
        train_loss.result(),
        train_accuracy.result() * 100,
        test_loss.result(),
        test_accuracy.result() * 100))
    results.append(entry)

with open("test_results.txt", 'at') as f:
    f.writelines(results)
    f.close()