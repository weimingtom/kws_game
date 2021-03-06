"""
screen capture for video presentation
"""

import pygame
import os
import soundfile

from common import create_folder, delete_png_in_path


class ScreenCapturer():
  """
  screen capture class for recording pygame screens
  """

  def __init__(self, screen, screen_size, fps, capture_path='./ignore/capture/', frame_path='frames/', frame_name='frame', enabled=True):

    # params
    self.screen = screen
    self.screen_size = screen_size
    self.fps = fps

    # paths
    self.capture_path = capture_path
    self.frame_path = frame_path
    self.frame_name = frame_name

    # enabled
    self.enabled = enabled

    # delete old data
    delete_png_in_path(self.capture_path + self.frame_path)

    # create folder for captured frames
    create_folder([self.capture_path + self.frame_path])

    # vars
    self.actual_frame_num = 0
    self.frame_container = []

    # downsample of fps
    self.downsample = 2
    self.downsample_count = 0


  def update(self):
    """
    update once per frame
    """

    # return if deactivated
    if not self.enabled:
      return

    # add image to container
    if self.downsample_count >= self.downsample:
      self.frame_container.append(pygame.image.tostring(self.screen, 'RGB'))
      self.downsample_count = 0

    # update frame number
    self.actual_frame_num += 1
    self.downsample_count += 1


  def save_video(self, mic=None):
    """
    save as video format
    """

    # return if deactivated
    if not self.enabled:
      return

    # restore all images and save them
    for i, frame in enumerate(self.frame_container):

      # save image
      pygame.image.save(pygame.image.fromstring(frame, (self.screen_size[0], self.screen_size[1]), 'RGB'), '{}{}{}.png'.format(self.capture_path + self.frame_path, self.frame_name, i))

    # audio
    if mic is not None:

      # save audio
      soundfile.write('{}out_audio.wav'.format(self.capture_path), mic.collector.x_all, mic.feature_params['fs'], subtype=None, endian=None, format=None, closefd=True)

    # convert to video format
    try:
      os.system("ffmpeg -framerate {} -start_number 0 -i {}%d.png -i {}out_audio.wav -vcodec mpeg4 {}.avi".format(self.fps // self.downsample, self.capture_path + self.frame_path + self.frame_name, self.capture_path, self.capture_path + 'out'))
    except:
      print("***Problem with conversions of frames to video")


if __name__ == '__main__':
  """
  capture
  """

  import yaml
  
  # append paths
  import sys
  sys.path.append("./game")

  # game stuff
  from game_logic import ThingsGameLogic
  from levels import Level_01, Level_02
  from classifier import Classifier
  from mic import Mic
  from text import Text
  from path_collector import PathCollector


  # yaml config file
  cfg = yaml.safe_load(open("./config.yaml"))

  # init path collector
  path_coll = PathCollector(cfg)


  # --
  # mic (for sound capture)

  # window and hop size
  N, hop = int(cfg['feature_params']['N_s'] * cfg['feature_params']['fs']), int(cfg['feature_params']['hop_s'] * cfg['feature_params']['fs'])

  # create classifier
  classifier = Classifier(path_coll=path_coll, verbose=True)

  # create mic instance
  mic = Mic(classifier=classifier, feature_params=cfg['feature_params'], mic_params=cfg['mic_params'], is_audio_record=True)
  
  
  # --
  # game setup

  # init pygame
  pygame.init()

  # init display
  screen = pygame.display.set_mode(cfg['game']['screen_size'])


  # init screen capturer
  screen_capturer = ScreenCapturer(screen, cfg['game']['screen_size'], cfg['game']['fps'], capture_path=cfg['game']['capture_path'])


  # text
  text = Text(screen)

  # level creation
  levels = [Level_01(screen, cfg['game']['screen_size'], mic)]

  # choose level
  level = levels[0]

  # game logic with dependencies
  game_logic = ThingsGameLogic(level, levels, text)

  # add clock
  clock = pygame.time.Clock()


  # mic stream and update
  with mic.stream:

    # game loop
    while game_logic.run_loop:
      for event in pygame.event.get():

        # input handling
        game_logic.event_update(event)
        level.event_update(event)

      # frame update
      level = game_logic.update()
      level.update()
      text.update()
      screen_capturer.update()


      # update display
      pygame.display.flip()

      # reduce framerate
      clock.tick(cfg['game']['fps'])


  # save video
  screen_capturer.save_video(mic)

  # end pygame
  pygame.quit()
