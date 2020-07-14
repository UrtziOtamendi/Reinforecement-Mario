import tensorflow.compat.v1 as tf

class Logger:

    def __init__(self,path):
        self.path=path
        self.score = tf.placeholder(dtype=tf.float32, shape=[], name='score')
        self.step=0
        self.summaries = tf.summary.merge([ tf.summary.scalar('score', self.score)])
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        self.writer = tf.summary.FileWriter(logdir= self.path, graph=self.session.graph)

    def record(self,score):
        self.step+=1
        self.writer.add_summary({'score':score},self.step)
