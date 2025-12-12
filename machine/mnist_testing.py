import keras
import numpy as np
from PIL import Image

"""
model_name = "unbatched"
model = keras.models.load_model(f"models/{model_name}.keras")
assert isinstance(model, keras.Model)

expected_shape = (1, 28, 28)
filepath = "new_data/6.png"
img = Image.open(filepath).convert('L')
img_array = np.array(img.resize(expected_shape[1:3]))

x = img_array.reshape(expected_shape)
prediction = model.predict(x)
print(prediction.shape) #(1, 10)
assert type(prediction[0]) is np.ndarray
print(prediction[0].argmax())
"""

class ImageRecognitionTesting():
    def __init__(self) -> None:
        self.loaded_model: keras.Sequential
        self.sample_shape: tuple[int, ...]

    def __call__(self, img_data: np.ndarray) -> tuple[np.ndarray, np.intp]:
        x = img_data.reshape(expected_shape)
        prediction = self.loaded_model.predict(x)[0]
        assert type(prediction) is np.ndarray
        res = (prediction, prediction.argmax())
        return res

    def load_model(self, model: keras.Sequential, shape: tuple[int, ...]):
        try:
            assert type(model) is keras.Sequential
            self.loaded_model = model
            self.sample_shape = shape
        except AssertionError:
            print("Could not load model...")
        

class ModelManager():
    @classmethod
    def load_model(cls, filepath) -> keras.Model | None:
        try:
            model = keras.models.load_model(filepath)
            assert isinstance(model, keras.Model), ""
            return model
        except AssertionError:
            return None

class SampleLoader():
    @classmethod
    def load_sample(cls, filepath, shape) -> np.ndarray:
        img = Image.open(filepath).convert('L')
        img_array = np.array(img.resize(shape))
        return img_array

if __name__ == "__main__":
    test_env = ImageRecognitionTesting()    
    model_path = "models/unbatched.keras"
    model = ModelManager.load_model(model_path)
    expected_shape = (1, 28, 28)
    test_env.load_model(model, expected_shape)
    template_path = "new_data/{}.png"
    while True:
        cmd = input("Data path: ")
        if cmd == "break":
            break
        sample_path = template_path.format(cmd)
        try:
            sample = SampleLoader.load_sample(sample_path, (28, 28))
        except FileNotFoundError:
            print(f"Not found: {sample_path}")
            continue
        p, res = test_env(sample)
        print(p)
        print(res)