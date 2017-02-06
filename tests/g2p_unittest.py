
import unittest
from g2p_seq2seq import g2p
from g2p_seq2seq import data_utils

class TestG2P(unittest.TestCase):

  def test_train(self):
    with g2p.tf.Graph().as_default():
      g2p_model = g2p.G2PModel(None)
      train_path = "tests/data/toydict.train"
      valid_path = "tests/data/toydict.test"
      test_path = "tests/data/toydict.test"
      g2p_params = g2p.TrainingParams()
      g2p_params.steps_per_checkpoint = 1
      g2p_params.max_steps = 1
      g2p_params.num_layers = 1
      g2p_params.size = 2
      g2p_model.prepare_data(train_path, valid_path, test_path)
      g2p_model.create_train_model(g2p_params)
      g2p_model.train()


  def test_evaluate(self):
    model_dir = "tests/models/decode"
    with g2p.tf.Graph().as_default():
      g2p_model = g2p.G2PModel(model_dir)
      g2p_model.load_decode_model()
      test_lines = open("tests/data/toydict.test").readlines()
      g2p_model.evaluate(test_lines)
      test_dic = data_utils.collect_pronunciations(test_lines)
      errors = g2p_model.calc_error(test_dic)
      self.assertAlmostEqual(float(errors)/len(test_dic), 0.667, places=3)


  def test_decode(self):
    model_dir = "tests/models/decode"
    with g2p.tf.Graph().as_default():
      g2p_model = g2p.G2PModel(model_dir)
      g2p_model.load_decode_model()
      decode_lines = open("tests/data/toydict.graphemes").readlines()
      phoneme_lines = g2p_model.decode(decode_lines)
      self.assertEqual(phoneme_lines[0].strip(), u'C')
      self.assertEqual(phoneme_lines[1].strip(), u'B C B')
      self.assertEqual(phoneme_lines[2].strip(), u'B')
