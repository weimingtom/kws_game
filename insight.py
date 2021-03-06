"""
Insight file for investigating the nn models
"""

import numpy as np
import matplotlib.pyplot as plt
import librosa

# my stuff
from common import create_folder
from plots import *
from conv_nets import *

from feature_extraction import pre_processing, calc_mfcc39, frames_to_sample
from classifier import Classifier

from skimage.util.shape import view_as_windows


def eval_model(model):
  """
  evaluate model
  """

  print("\nmodel:\n", model)

  print("weights: ", model.fc1.weight.detach().shape)

  #print("conv weights: ", model.conv.weight.detach())
  print("conv weights: ", model.conv.weight.detach().shape)

  plt.figure(), plt.imshow(np.squeeze(model.conv.weight.detach().numpy()[0]), aspect='auto'), plt.colorbar()
  plt.figure(), plt.imshow(np.squeeze(model.conv.weight.detach().numpy()[1]), aspect='auto'), plt.colorbar()
  plt.figure(), plt.imshow(np.squeeze(model.conv.weight.detach().numpy()[2]), aspect='auto'), plt.colorbar()
  plt.figure(), plt.imshow(np.squeeze(model.conv.weight.detach().numpy()[3]), aspect='auto'), plt.colorbar()

  #plt.figure(), plt.imshow(model.fc1.weight.detach().numpy(), aspect='auto'), plt.colorbar()
  #plt.figure(), plt.imshow(model.fc2.weight.detach().numpy(), aspect='auto'), plt.colorbar()
  #plt.figure(), plt.imshow(model.fc4.weight.detach().numpy(), aspect='auto'), plt.colorbar()


if __name__ == '__main__':
  """
  Insight file - gives insight in neural nets
  """
  
  import yaml
  from path_collector import PathCollector
  
  # yaml config file
  cfg = yaml.safe_load(open("./config.yaml"))

  # init path collector
  path_coll = PathCollector(cfg)

  # plot path and model path
  plot_path = './ignore/plots/insight/'

  # create folder
  create_folder([plot_path])

  # classifier
  classifier = Classifier(path_coll=path_coll, verbose=True)

  # get model
  model = classifier.cnn_handler.model 


  # wav file to evaluate
  #wav = './ignore/my_recordings/clean_records/down.wav'
  wav = './ignore/my_recordings/clean_records/up.wav'

  # sampling rate
  fs = 16000

  # window and hop size
  N, hop = int(cfg['feature_params']['N_s'] * cfg['feature_params']['fs']), int(cfg['feature_params']['hop_s'] * cfg['feature_params']['fs'])


  # -- 
  # model insights

  # model visualization
  #eval_model(model)


  # --
  # classification insights

  # read audio from file
  x_raw, fs = librosa.load(wav, sr=fs)

  # preprocessing
  x_pre = pre_processing(x_raw)

  # mfcc
  x_mfcc = calc_mfcc39(x_pre, fs, N=N, hop=hop, n_filter_bands=32, n_ceps_coeff=12)

  # dimensions
  m, f, window_step = 39, 32, 2

  # windowed [r x m x f]
  x_win = np.squeeze(view_as_windows(x_mfcc, (m, f), step=window_step))
  y_hat_list = []

  for i, x in enumerate(x_win):

    # classify
    print("frame: ", i)
    y_hat, label = classifier.classify_sample(x)
    y_hat_list.append(y_hat)

    # plot
    time_s = frames_to_sample(i*window_step, fs, hop)
    time_e = frames_to_sample(i*window_step+32, fs, hop)

    plot_waveform(x_pre[time_s:time_e], fs, title='frame{}_y-{}'.format(i, y_hat), xlim=None, ylim=(-1, 1), plot_path=plot_path, name='frame{}'.format(i))

  print("y_hats: ", y_hat_list)
  plot_waveform(x_pre, fs, ylim=(-1, 1))

  plt.show()



