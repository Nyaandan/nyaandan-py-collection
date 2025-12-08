import pickle
from intro_practice.Models import Model_No1

def save_progress(model, filename):
    with open(filename, 'wb') as f:
        pickle.dump({
            'name': model.name,
            'parameters': model.parameters,
            'weights': model.weights.numpy() if model.weights is not None else None,
            'biases': model.biases.numpy() if model.biases is not None else None
        }, f)

def load_progress(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
        return Model_No1(
            name=data['name'],
            parameters=data['parameters'],
            weights=data['weights'],
            biases=data['biases']
        )