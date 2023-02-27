# AI x Bookathon
# MindsLab, Inc.

import tensorflow as tf

class NsgDecodingSampler(object):
    def __init__(self, config):
        self.method = config.sampling_method
        self.top_k = config.top_k
        self.top_p = config.top_p
        self.temperature = config.temperature

    def sample(self, logits):
        logits = logits / tf.to_float(self.temperature)

        if self.method == 'top_p':
            return top_p_logits(logits, self.top_p)
        elif self.method == 'top_k':
            return top_k_logits(logits, self.top_k)
        else:
            raise NotImplemented


def top_k_logits(logits, k):
    logits_top_k, _ = tf.nn.top_k(logits, k=k)
    min_logits = logits_top_k[:, -1, tf.newaxis]

    return tf.where(
        logits < min_logits,
        tf.ones_like(logits, dtype=logits.dtype) * -1e8,
        logits,
    )

def top_p_logits(logits, p):
    logits_sorted = tf.sort(logits, direction='DESCENDING')
    probs_sorted = tf.nn.softmax(logits_sorted)
    probs_cumsum = tf.cumsum(probs_sorted, axis=1, exclusive=True)
    logits_masked = tf.where(probs_cumsum < p, logits_sorted, tf.ones_like(logits_sorted)*1e6)
    min_logits = tf.reduce_min(logits_masked, axis=1, keepdims=True)

    return tf.where(
        logits < min_logits,
        tf.ones_like(logits, dtype=logits.dtype) * -1e8,
        logits,
    )
