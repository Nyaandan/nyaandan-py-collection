import keras
import numpy as np
from PIL import Image
import sys

model_name = "unbatched"
model = keras.models.load_model(f"models/{model_name}.keras")
assert type(model) is keras.Sequential

expected_shape = (1, 28, 28)
filepath = "new_data/6.png"
img = Image.open(filepath).convert('L')
img_array = np.array(img)
try:
    x = img_array.reshape(expected_shape)
except ValueError:
    print("Sample image is of incompatible size. Expected 28x28.")
    sys.exit(0)

prediction = model.predict(x)[0]
print(prediction)
assert type(prediction) is np.ndarray
print(prediction.argmax())