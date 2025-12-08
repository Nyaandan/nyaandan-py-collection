import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import intro_practice.trainer as trainer
from intro_practice.Models import Model_No1

def test_tensorflow_installation():
    try:
        # Check TensorFlow version
        print("TensorFlow version:", tf.__version__)
        
        # Create a simple tensor
        a = tf.constant([[1, 2], [3, 4]])
        b = tf.constant([[5, 6], [7, 8]])
        
        # Perform a matrix multiplication
        c = tf.matmul(a, b)
        
        # Print the result
        print("Result of matrix multiplication:\n", c.numpy())
        
        print("TensorFlow installation is working correctly.")
    except Exception as e:
        print("An error occurred while testing TensorFlow installation:", str(e))

def generate_synthetic_data(num_points=100):
    m = 2.4
    b = 1.0
    x = np.linspace(0, 8, num_points)
    y = m * x + b + np.random.normal(-4.2, 4.8, x.shape)
    return x, y

def scatter_plot(x, y):
    plt.scatter(x, y, label='Data Points')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Scatter Plot of Synthetic Data')
    plt.legend()

    

if __name__ == "__main__":
    # Prepare data for training
    x, y = generate_synthetic_data(100)
    x_train = x.reshape(-1, 1).astype(np.float32)
    y_train = y.reshape(-1, 1).astype(np.float32)

    x_line = np.linspace(min(x), max(x), 100)

    models_results = {}
    model_no = 0
    while True:
        user_input = input("Train a new model? (yes/no): ").strip().lower()
        if user_input not in ['yes', 'y', '1']:
            print("Exiting the training loop.")
            break

        scatter_plot(x, y)

        # Initialize model
        model_no += 1
        model = Model_No1(name=f"LR_{model_no}", parameters={"learning_rate": 0.01}, weights=np.random.randn(1, 1), biases=np.random.randn(1))
        print(model.check_values())
        y_line = model.weights.read_value().numpy()[0][0] * x_line + model.biases.read_value().numpy()[0] if model.weights is not None and model.biases is not None else 0
        plt.plot(x_line, y_line, color="red", label='Old Model Prediction', linewidth=2)

        # Train the model
        trainer.train_model(model, x_train, y_train, epochs=20, learning_rate=0.01)
        print(model.check_values())
        y_line = model.weights.read_value().numpy()[0][0] * x_line + model.biases.read_value().numpy()[0] if model.weights is not None and model.biases is not None else 0
        plt.plot(x_line, y_line, color="green", label='New Model Prediction', linewidth=2)

        # Plot the results
        plt.legend()
        plt.show()
        