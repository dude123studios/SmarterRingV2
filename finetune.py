from model.facenet_loader import model
from finetuning.prepare_data import pairs1, pairs2, labels
import tensorflow as tf

optimizer = tf.keras.optimizers.Adam(learning_rate=6e-4)


@tf.function
def train_step(imgA, imgB, label):
    with tf.GradientTape() as tape:
        outA = model(imgA)
        outB = model(imgB)
        x_norm = tf.sqrt(tf.reduce_sum(tf.square(outA), axis=1))
        y_norm = tf.sqrt(tf.reduce_sum(tf.square(outB), axis=1))
        z = tf.reduce_sum(outA * outB, axis=1)
        m = x_norm * y_norm + 1e-9
        cosine = z / m
        loss = tf.keras.losses.binary_crossentropy(label, cosine)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss


epochs = 10

for i in range(1, epochs + 1):
    loss = 0
    for pair1, pair2, label in zip(pairs1, pairs2, labels):
        loss += train_step(pair1, pair2, label).numpy()
    print('EPOCH: {}/{}, LOSS: {:.4f}'.format(i, 5, loss.tolist()[0]))

# model.save('model/files/facenet_keras.h5')
