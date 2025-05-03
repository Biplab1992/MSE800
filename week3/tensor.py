import tensorflow as tf # type: ignore
(x_bird, y_bird), (x_test, y_test) = tf.keras.datasets.cifar10.load-data()
print("Training data shape:", x_bird.shape,y_bird.shape)