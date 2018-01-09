import numpy as np
import tensorflow as tf
import os
import time
import random

# Iterations, Training Loss, Total Time
benchmark_log = np.array([[0,0,0]])

num_iterations = 1000

txt = open('../data/text_sample.txt', 'r').read().lower()

chars = list(set(txt))
data = [chars.index(c) for c in txt]

def get_next_batch(batch_size, time_steps, data):
    x_batch = np.zeros((batch_size, time_steps))
    y_batch = np.zeros((batch_size, time_steps))

    batch_ids = range(len(data) - time_steps - 1)
    batch_id = random.sample(batch_ids, batch_size)

    for t in range(time_steps):
        x_batch[:, t] = [data[i+t] for i in batch_id]
        y_batch[:, t] = [data[i+t+1] for i in batch_id]

    return x_batch, y_batch

n_layers = 2
n_chars = len(chars)
lstm_size = 256

time_steps = 100
batch_size = 50

def make_lstm(x, lstm_init_value, n_chars, lstm_size, n_layers):
    # LSTM
    lstm = tf.contrib.rnn.MultiRNNCell(
        [tf.contrib.rnn.BasicLSTMCell(lstm_size, forget_bias=1.0, state_is_tuple=False)
         for _ in range(n_layers)],
        state_is_tuple=False)

    # Iteratively compute output of recurrent network
    out, lstm_new_state = tf.nn.dynamic_rnn(lstm, x, initial_state=lstm_init_value, dtype=tf.float32)

    # Linear activation (FC layer on top of the LSTM net)
    out_reshaped = tf.reshape(out, [-1, lstm_size])
    y = tf.layers.dense(out_reshaped, n_chars, activation=None)

    return y, tf.shape(out), lstm_new_state

sess = tf.Session()

x = tf.placeholder(tf.int32, shape=(None, None), name="x")
y_true = tf.placeholder(tf.int32, (None, None))
lstm_init_value = tf.placeholder(tf.float32, shape=(None, n_layers*2*lstm_size),
                                 name="lstm_init_value")

x_enc = tf.one_hot(x, depth=n_chars)
y_true_enc = tf.one_hot(y_true, depth=n_chars)

y_pred, out_shape, lstm_new_state = make_lstm(x_enc, lstm_init_value, n_chars, lstm_size, n_layers)

final_out = tf.reshape(tf.nn.softmax(y_pred),
                       (out_shape[0], out_shape[1], n_chars))

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=y_pred,
        labels=tf.reshape(y_true_enc, [-1, n_chars])))
tf.summary.scalar('loss', loss)

optimizer = tf.train.RMSPropOptimizer(0.003, 0.9).minimize(loss)

merged = tf.summary.merge_all()

display_step = 50

sess.run(tf.global_variables_initializer())

step = 1

# Start-time used for printing time-usage below.
start_time = time.time()

for i in range(num_iterations):

    # Get a batch of training examples.
    x_batch, y_true_batch = get_next_batch(batch_size, time_steps, data)

    # ---------------------- TRAIN -------------------------
    # optimize model
    init_value = np.zeros((x_batch.shape[0], n_layers*2*lstm_size))
    sess.run(optimizer, feed_dict={x: x_batch, y_true: y_true_batch, lstm_init_value:init_value})

    # Print status every 50 iterations.
    if (i % display_step == 0) or (i == num_iterations - 1):

        summary, l = sess.run([merged, loss], feed_dict={x: x_batch, y_true: y_true_batch, lstm_init_value:init_value})
        end_time = time.time()
        time_dif = (end_time - start_time)/60.

        # Message for network evaluation
        msg = "Optimization Iteration: {0:>6}, Training Loss: {1:>6}, Total Time: {2:>6}"
        print(msg.format(i, l,time_dif))
        benchmark_log = np.vstack((benchmark_log,np.array([[i,l,time_dif]])))
        step += 1

# Normalize time values to start at 0
benchmark_log[:,2]-=benchmark_log[1,2]

# Save the log
np.savetxt("benchmark_log.csv",benchmark_log[1:],delimiter=",",header="Iterations,Training Loss,Total Time",comments='')
