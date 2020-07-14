import time
import random
import numpy as np
import tensorflow.compat.v1 as tf
from matplotlib import pyplot as plt

class DQNAgent:
    """ DQN agent """
    def __init__(self, models_path,states, actions, batch_size, double_q):
        tf.compat.v1.disable_eager_execution()
        self.states = states
        self.actions = actions
        self.session = tf.Session()
        self.models_path=models_path
        self.build_model()
        self.saver = tf.train.Saver(max_to_keep=10)
        self.session.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()
        self.eps = 1
        self.eps_decay = 0.99999975
        self.eps_min = 0.1
        self.gamma = 0.90
        self.batch_size = batch_size
        self.copy = 10000
        self.step = 0
        self.learn_each = 3
        self.learn_step = 0
        self.save_each = 500000
        self.double_q = double_q

        self.load_model()

    def build_model(self):
        """ Model builder function """
        self.input = tf.placeholder(dtype=tf.float32, shape=(None, ) + self.states, name='input')
        self.q_true = tf.placeholder(dtype=tf.float32, shape=[None], name='labels')
        self.a_true = tf.placeholder(dtype=tf.int32, shape=[None], name='actions')
        self.reward = tf.placeholder(dtype=tf.float32, shape=[], name='reward')
        self.input_float = tf.to_float(self.input) / 255.
        # Online network
        with tf.variable_scope('online'):
            self.conv_1 = tf.layers.conv2d(inputs=self.input_float, data_format='channels_first',filters=32, kernel_size=8, strides=4, activation=tf.nn.relu)
            self.conv_2 = tf.layers.conv2d(inputs=self.conv_1, filters=64, kernel_size=4, strides=2, activation=tf.nn.relu)
            self.conv_3 = tf.layers.conv2d(inputs=self.conv_2, filters=64, kernel_size=3, strides=1, activation=tf.nn.relu)
            self.flatten = tf.layers.flatten(inputs=self.conv_3)
            self.dense = tf.layers.dense(inputs=self.flatten, units=512, activation=tf.nn.relu)
            self.output = tf.layers.dense(inputs=self.dense, units=self.actions, name='output')
        # Target network
        with tf.variable_scope('target'):
            self.conv_1_target = tf.layers.conv2d(inputs=self.input_float, data_format='channels_first', filters=32, kernel_size=8, strides=4, activation=tf.nn.relu)
            self.conv_2_target = tf.layers.conv2d(inputs=self.conv_1_target, filters=64, kernel_size=4, strides=2, activation=tf.nn.relu)
            self.conv_3_target = tf.layers.conv2d(inputs=self.conv_2_target, filters=64, kernel_size=3, strides=1, activation=tf.nn.relu)
            self.flatten_target = tf.layers.flatten(inputs=self.conv_3_target)
            self.dense_target = tf.layers.dense(inputs=self.flatten_target, units=512, activation=tf.nn.relu)
            self.output_target = tf.stop_gradient(tf.layers.dense(inputs=self.dense_target, units=self.actions, name='output_target'))
        # Optimizer
        self.action = tf.argmax(input=self.output, axis=1)
        self.q_pred = tf.gather_nd(params=self.output, indices=tf.stack([tf.range(tf.shape(self.a_true)[0]), self.a_true], axis=1))
        self.loss = tf.losses.huber_loss(labels=self.q_true, predictions=self.q_pred)
        self.train = tf.train.AdamOptimizer(learning_rate=0.00025).minimize(self.loss)
        # Summaries
        self.summaries = tf.summary.merge([
            tf.summary.scalar('reward', self.reward),
            tf.summary.scalar('loss', self.loss),
            tf.summary.scalar('max_q', tf.reduce_max(self.output))
        ])
        self.writer = tf.summary.FileWriter(logdir='./logs', graph=self.session.graph)
    def copy_model(self):
        """ Copy weights to target network """
        self.session.run([tf.assign(new, old) for (new, old) in zip(tf.trainable_variables('target'), tf.trainable_variables('online'))])

    def save_model(self):
        """ Saves current model to disk """
        print('--------->Saving model to disk')
        self.saver.save(sess=self.session, save_path=self.models_path+"model", global_step=self.step)
    def load_model(self):
        """ Loads model from disk """
        print('--------->Loading model from disk')
        save_path=tf.train.latest_checkpoint(self.models_path)
        if save_path is not None:
            self.saver.restore(sess=self.session, save_path=tf.train.latest_checkpoint(self.models_path))
        
    
    
    def predict(self, model, state):
        """ Prediction """
        if model == 'online':
            return self.session.run(fetches=self.output, feed_dict={self.input: np.array(state)})
        if model == 'target':
            return self.session.run(fetches=self.output_target, feed_dict={self.input: np.array(state)})

    def run(self, state):
        """ Perform action """
        
        # Policy action
        q = self.predict('online', np.expand_dims(state.start, 0))
        action = np.argmax(q)
        # Decrease eps
        self.eps *= self.eps_decay
        self.eps = max(self.eps_min, self.eps)
        # Increment step
        self.step += 1
        return action

    def learn(self,batch):
        self.step+=1
        """ Gradient descent """
        # Sync target network
        if self.step % self.copy == 0:
            self.copy_model()
        # Checkpoint model
        if self.step % self.save_each == 0:
            self.save_model()
        
        # Break if no training
        if self.learn_step < self.learn_each:
            self.learn_step += 1
            return

        # Sample batch
        
        [state,next_state,action,reward,done]= batch
        # Get next q values from target network
        next_q = self.predict('target', next_state)
        # Calculate discounted future reward
        if self.double_q:
            q = self.predict('online', next_state)
            a = np.argmax(q, axis=1)
            target_q = reward + (1. - done) * self.gamma * next_q[np.arange(0, self.batch_size), a]
        else:
            target_q = reward + (1. - done) * self.gamma * np.amax(next_q, axis=1)
        # Update model
        summary, _ = self.session.run(fetches=[self.summaries, self.train],
                                      feed_dict={self.input: state,
                                                 self.q_true: np.array(target_q),
                                                 self.a_true: np.array(action),
                                                 self.reward: np.mean(reward)})
        # Reset learn step
        self.learn_step = 0
        
        # Write
        self.writer.add_summary(summary, self.step)

  