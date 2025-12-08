import keras

mnist = keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255.0
x_test = x_test / 255.0

# Name of the model, new or existing
model_name = "unbatched"

"""# Creating a new model
model = keras.models.Sequential(
    [keras.layers.Flatten(input_shape=(28, 28)),
     keras.layers.Dense(128, "relu"), 
     keras.layers.Dropout(0.15),
     keras.layers.Dense(10, "softmax")],
     name=model_name
)
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.save(f"models/{model_name}_untrained.keras")
"""

# Loading a saved model
model = keras.models.load_model(f"models/{model_name}.keras")
assert type(model) is keras.Sequential

labels = model.metrics_names

#model.reset_metrics()
#model.fit(x_train, y_train, batch_size=32, epochs=6)
#model.save(f"models/{model_name}.keras")
scores = model.evaluate(x_test, y_test, batch_size=32, verbose="2")
results = dict(zip(labels, scores))
results["name"] = model_name

with open(f"models/log_{model_name}.json", "w") as f:
    import json
    f.writelines(json.dumps(results))
    f.close()