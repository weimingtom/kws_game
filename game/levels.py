"""
levels
"""

import pygame

from interactable import Interactable


class Level(Interactable):
  """
  level class
  """

  def __init__(self, screen, screen_size, color_bag):

    # colors
    self.screen = screen
    self.screen_size = screen_size
    self.color_bag = color_bag

    # sprites
    self.all_sprites = pygame.sprite.Group()


  def setup_level(self):
    """
    setup level
    """
    pass


  def update(self):
    """
    update
    """

    # update sprites
    self.all_sprites.update()

    # fill screen
    self.screen.fill(self.color_bag.background)

    # draw sprites
    self.all_sprites.draw(screen)



class LevelGrid(Level):
  """
  level with grid
  """

  def __init__(self, screen, screen_size, color_bag, mic=None):

    from grid_world import GridWorld

    # parent class init
    super().__init__(screen, screen_size, color_bag)

    # new vars
    self.mic = mic

    # create gridworld
    self.grid_world = GridWorld(self.screen_size, self.color_bag, self.mic)

    # setup
    self.setup_level(self.grid_world)

    # sprites
    self.all_sprites.add(self.grid_world.wall_sprites, self.grid_world.move_wall_sprites)


  def setup_level(self, grid_world):
    """
    setup level
    """

    # set walls
    self.setup_wall_edge(self.grid_world)

    # create walls
    self.grid_world.create_walls()


  def setup_wall_edge(self, grid_world):
    """
    limit edges
    """

    # set walls
    self.grid_world.wall_grid[:, 0] = 1
    self.grid_world.wall_grid[:, -1] = 1
    self.grid_world.wall_grid[0, :] = 1
    self.grid_world.wall_grid[-1, :] = 1


  def reset(self):
    """
    reset level
    """

    self.grid_world.reset()


  def event_update(self, event):
    """
    event update
    """
    
    # grid world update
    self.grid_world.event_update(event)


  def update(self):
    """
    update
    """

    # grid world update
    self.grid_world.update()

    # update sprites
    self.all_sprites.update()

    # fill screen
    self.screen.fill(self.color_bag.background)

    # draw sprites
    self.all_sprites.draw(self.screen)



class LevelSquare(LevelGrid):
  """
  level square
  """

  def __init__(self, screen, screen_size, color_bag):

    # parent class init
    super().__init__(screen, screen_size, color_bag)


  def setup_level(self, grid_world):
    """
    setup level
    """

    # set walls
    self.setup_wall_edge(self.grid_world)

    # wall in the middle
    self.grid_world.wall_grid[7, 7] = 1

    # create walls
    self.grid_world.create_walls()



class LevelMoveWalls(LevelGrid):
  """
  level with moving walls
  """

  def __init__(self, screen, screen_size, color_bag, mic=None):

    # parent class init
    super().__init__(screen, screen_size, color_bag, mic)


  def setup_level(self, grid_world):
    """
    setup level
    """

    # set walls
    self.setup_wall_edge(self.grid_world)

    self.grid_world.wall_grid[5, 5] = 1

    # move walls
    self.grid_world.move_wall_grid[8, 8] = 1
    self.grid_world.move_wall_grid[10, 15] = 1
    self.grid_world.move_wall_grid[12, 20] = 1

    # create walls
    self.grid_world.create_walls()



class LevelCharacter(LevelGrid):
  """
  level with character
  """

  def __init__(self, screen, screen_size, color_bag, mic=None):

    # parent class init
    super().__init__(screen, screen_size, color_bag, mic)

    from character import Character

    # create the character
    self.henry = Character(position=(self.screen_size[0]//2, self.screen_size[1]//2), scale=(2, 2), is_gravity=True)
    self.henry.obstacle_sprites.add(self.grid_world.wall_sprites, self.grid_world.move_wall_sprites)

    # add to sprites
    self.all_sprites.add(self.henry)


  def setup_level(self, grid_world):
    """
    setup level
    """

    # set walls
    self.setup_wall_edge(self.grid_world)

    # wall in the middle
    self.grid_world.wall_grid[20:25, 20:24] = 1
    self.grid_world.wall_grid[10:15, 20] = 1

    # create walls
    self.grid_world.create_walls()


  def reset(self):
    """
    reset level
    """

    self.grid_world.reset()
    self.henry.reset()


  def event_update(self, event):
    """
    event update
    """
    
    # grid world update
    self.henry.event_update(event)
    self.grid_world.event_update(event)



class LevelThings(LevelCharacter):
  """
  level with character
  """

  def __init__(self, screen, screen_size, color_bag, mic=None):

    # parent class init
    super().__init__(screen, screen_size, color_bag, mic)

    from things import Thing

    # create thing
    self.thing = Thing(position=self.grid_world.grid_to_pos([22, 18]), scale=(2, 2))

    # add to sprites
    self.all_sprites.add(self.thing)
    self.henry.thing_sprites.add(self.thing)

    # determine position
    self.henry.set_position(self.grid_world.grid_to_pos([10, 10]), is_init_pos=True)


  def reset(self):
    """
    reset level
    """

    self.grid_world.reset()
    self.henry.reset()

    # add to sprites
    self.all_sprites.add(self.thing)
    self.henry.thing_sprites.add(self.thing)



class Level_01(LevelThings):
  """
  first actual level
  """

  def __init__(self, screen, screen_size, color_bag, mic=None):

    # parent class init
    super().__init__(screen, screen_size, color_bag, mic)

    # determine start position
    self.henry.set_position(self.grid_world.grid_to_pos([5, 20]), is_init_pos=True)
    self.thing.set_position(self.grid_world.grid_to_pos([22, 18]), is_init_pos=True)


  def setup_level(self, grid_world):
    """
    setup level
    """

    # set walls
    self.setup_wall_edge(self.grid_world)

    # wall in the middle
    self.grid_world.wall_grid[20:25, 20:23] = 1
    self.grid_world.wall_grid[20:25, 16] = 1
    self.grid_world.wall_grid[25, 16:23] = 1

    self.grid_world.wall_grid[10:15, 20:23] = 1

    # move walls
    self.grid_world.move_wall_grid[20, 17] = 1
    self.grid_world.move_wall_grid[20, 18] = 1
    self.grid_world.move_wall_grid[20, 19] = 1

    # create walls
    self.grid_world.create_walls()


class Level_02(LevelThings):
  """
  first actual level
  """

  def __init__(self, screen, screen_size, color_bag, mic=None):

    # parent class init
    super().__init__(screen, screen_size, color_bag, mic)

    # determine start position
    self.henry.set_position(self.grid_world.grid_to_pos([22, 20]), is_init_pos=True)
    self.thing.set_position(self.grid_world.grid_to_pos([2, 5]), is_init_pos=True)


  def setup_level(self, grid_world):
    """
    setup level
    """

    # set walls
    self.setup_wall_edge(self.grid_world)

    # wall in the middle
    self.grid_world.wall_grid[27:, 19] = 1
    self.grid_world.wall_grid[19:22, 15] = 1
    self.grid_world.wall_grid[11:14, 11] = 1

    self.grid_world.wall_grid[:5, 7] = 1

    # move walls
    self.grid_world.move_wall_grid[29, 22] = 1
    self.grid_world.move_wall_grid[27, 18] = 1
    self.grid_world.move_wall_grid[19, 16] = 1
    self.grid_world.move_wall_grid[4, 8] = 1

    # create walls
    self.grid_world.create_walls()


if __name__ == '__main__':
  """
  levels
  """

  from color_bag import ColorBag
  from game_logic import GameLogic, ThingsGameLogic
  from text import Text

  # size of display
  screen_size = width, height = 640, 480

  # init pygame
  pygame.init()

  # init display
  screen = pygame.display.set_mode(screen_size)

  # collection of game colors
  color_bag = ColorBag()
  text = Text(screen, color_bag)

  # level creation
  #level = LevelSquare(screen, screen_size, color_bag)
  #level = LevelMoveWalls(screen, screen_size, color_bag)

  # level creation
  #levels = [Level_01(screen, screen_size, color_bag), Level_02(screen, screen_size, color_bag)]
  levels = [Level_02(screen, screen_size, color_bag)]

  # choose level
  level = levels[0]

  # game logic with dependencies
  game_logic = ThingsGameLogic(level, levels, text)

  # add clock
  clock = pygame.time.Clock()


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

    # update display
    pygame.display.flip()

    # reduce framerate
    clock.tick(60)

  # end pygame
  pygame.quit()




  

