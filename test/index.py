import pygame
import random

pygame.init()

# Constants
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 600
FPS = 20
SHIFT_COOLDOWN = 50
MIN_TIME_INTERVAL = 10  # Minimum time interval in frames
MAX_TIME_INTERVAL = 100 


# Initialization
display = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
pygame.display.set_caption('Car Game')
clock = pygame.time.Clock()

max_speeds = [140, 220, 310, 400]
acceleration_FACTORS = [0.5, 0.48, 0.32, 0.28]
car_x = 390

class Button:
  def __init__(self, x, y, width, height, text, font, color, hover_color, action=None):
    self.rect = pygame.Rect(x, y, width, height) 
    self.text = text
    self.font = font
    self.color = color
    self.hover_color = hover_color
    self.action = action
    self.is_hovered = False

  def draw(self, screen):
    mouse_pos = pygame.mouse.get_pos()
    self.is_hovered = self.rect.collidepoint(mouse_pos)
    color = self.hover_color if self.is_hovered else self.color
    pygame.draw.rect(screen, color, self.rect)
    text_surface = self.font.render(self.text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=self.rect.center)
    screen.blit(text_surface, text_rect)
  
  def click(self):
    if self.is_hovered and self.action:
       self.action()

def quit_game(self):
  pygame.quit()
  quit()

def start_game():
  print("Start Game")
  global current_screen
  current_screen = "GAME"

class MainMenu:
  def __init__(self):
    self.font = pygame.font.Font(None, 74)
    self.button_font = pygame.font.Font(None, 50)
    self.background_color = (50, 50, 50)
    self.button_color = (100, 100, 250)
    self.button_hover_color = (150, 150, 250)
    self.buttons = [
      Button(400, 200, 200, 70, "Start Game", self.button_font, self.button_color, self.button_hover_color, start_game),
      Button(400, 300, 200, 70, "Quit", self.button_font, self.button_color, self.button_hover_color, quit_game)
    ]


  def handle_events(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for button in self.buttons:
            button.click()

  def draw(self):
    display.fill(self.background_color)
    for button in self.buttons:
      button.draw(display)

class Settings_Menu:
  def __init__(self):
    self.font = pygame.font.Font(None, 74)

"""def times():
  global timees, amount_rect, y
  timees_value = max(MIN_TIME_INTERVAL, min(MAX_TIME_INTERVAL, round(1000 / speed)))

  #timees_value = 20

  # Check if it's time to add a new rectangle
  if timees % timees_value == 1:
    length = 60 
    if speed > 100: 
        length = 50
    elif speed > 200: 
        length = 40
    elif speed > 300: 
        length = 30
    elif speed > 400: 
        length = 20
    
    y = -50  # Reset y position if needed
    elements.append(pygame.Rect(x, y, 10, length))
    amount_rect += 1

  timees += 1"""

class Car:
  def __init__(self):
    self.x = car_x
    self.y = 380
    self.width = 70
    self.height = 200
    self.left_pressed = False
    self.right_pressed = True

  def draw_car(self, surface):
    car_body_color = (50, 50, 255)  # Blue body
    car_wheel_color = (255, 255, 255)
    car_cover_color = (50, 50, 200)

    car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
    body_rect = pygame.Rect(15, 30, 50, 100)
    wheels = [(10, 40), (60, 40), (10, 100), (60, 100)]
    for (wx, wy) in wheels:
        pygame.draw.rect(car_surface, car_wheel_color, (wx, wy, 10, 20))

    covers = [(13, 38), (57, 38), (13, 98), (57, 98)]
    for (cx, cy) in covers:
        pygame.draw.rect(car_surface, car_cover_color, (cx, cy, 10, 24))

    rotated_car = pygame.transform.rotate(car_surface, self.angle)
    surface.blit(rotated_car, (self.x, self.y))
  
  def handle_movement(self):
     
    print(f"Car X: {self.cx}, Car Angle: {self.car_angle}")
    if self.left_pressed == True:
      if self.x > 290:
        self.x -= 5
        
        if self.car_angle < 10:
          self.car_angle += 1

    else:
      if self.car_angle > 0:
        self.car_angle -= 1
    
    if self.right_pressed == True:
      if self.x < 700 - 20:
        self.x += 5
        
        if self.car_angle > -10:
          self.car_angle -= 1
    else:
      if self.car_angle < 0:
        self.car_angle += 1

  """def draw(self):
    car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
    self.draw_car(car_surface)
    rotated_car = pygame.transform.rotate(car_surface, GameMenu.car_angle)
    display.blit(rotated_car, (self.x, self.y))

  def update(self):

  def render(self):
      self.display.fill((25, 25, 25))
      self.car_draw(display)
      # Render other elements

  def run(self):
      while self.running:
          self.handle_events()
          self.update(self)
          self.render()"""
#car = Car()


class GameMenu:
  def __init__(self):
    self.accelerate_pressed = False
    self.deacelerate_pressed = False
    self.right_pressed = False
    self.left_pressed = False
    self.current_gear = 1
    self.acceleration = 0.1
    self.acceleration_delay = 0
    self.acceleration_delay_minus = 0
    self.timees = 0
    self.timees_value = 50
    self.amount_rect = 0
    self.elements = []
    self.obstacles = []
    self.speed = 10
    self.cooldown = False
    self.cooldowns = [0] * 4  # Example cooldowns list
    self.transform = [-150, -70, 40, 120]
    self.car = None
    self.car_y = 380
    self.car_x = 0
    button_font = pygame.font.Font(None, 50)
    button_color = (100, 100, 250)
    button_hover_color = (150, 150, 250)
    self.get_back_button = Button(780, 40, 180, 50, "Get Back", button_font, button_color, button_hover_color, self.get_back)
    
  
  car_angle = 0

  def handle_events(self, event):
    if event.type == pygame.QUIT:
        self.running = False

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            self.car.left_pressed = True
        elif event.key == pygame.K_d:
            self.car.right_pressed = True
        elif event.key == pygame.K_w:
            self.accelerate()
        elif event.key == pygame.K_s:
            self.decelerate()

        elif event.key == pygame.K_r:
          if self.current_gear < 4:
            self.set_gear(self.current_gear + 1)

        elif event.key == pygame.K_a:
          self.left_pressed = True

        elif event.key == pygame.K_d:
          self.right_pressed = True

        elif event.key == pygame.K_f:
          if self.current_gear > 1:
            self.set_gear(self.current_gear - 1)
        """if event.key == pygame.K_w:
          self.accelerate_pressed = True

        elif event.key == pygame.K_s: 
          self.deacelerate_pressed = True"""

    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            self.car.left_pressed = False
        elif event.key == pygame.K_d:
            self.car.right_pressed = False

        elif event.key == pygame.K_a:
          self.left_pressed = False

        elif event.key == pygame.K_d:
          self.right_pressed = False
        """if event.key == pygame.K_w:
          self.accelerate_pressed = False

        elif event.key == pygame.K_s:
          self.deacelerate_pressed = False"""
      
    """elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          self.get_back_button.click()"""
    
  def update(self):
    self.timees += 1
    self.car.handle_movement()
    acceleration_factor = acceleration_FACTORS[self.current_gear - 1]
    max_speed = max_speeds[self.current_gear - 1]
        

    # Create new obstacles
    if self.timees % 60 == 0:  # Example interval
        width = 50
        height = 80
        self.obstacles.append(pygame.Rect(random.randint(300, 700), -height, width, height))

    # Move elements and obstacles
    for element in self.elements[:]:
        element.y += speed / 10
        if element.top > DISPLAY_HEIGHT:
            self.elements.remove(element)
            self.amount_rect -= 1

    for obstacle in self.obstacles[:]:
        obstacle.y += speed / 10
        if obstacle.top > DISPLAY_HEIGHT:
            self.obstacles.remove(obstacle)

    """self.cooldown_tick()

    if not self.is_cooldown_active():
      self.accelerations()
    else:
      self.acceleration = 0.1"""
    self.accelerations()
    """
    random_int = random.randint(40, 80)
    transform_number = random.randint(0, 3)
    transform = [-150, -70, 40, 120]
    cooldowns = [0] * len(transform)
    for i in range(len(cooldowns)):
      if cooldowns[i] > 0:
          cooldowns[i] -= 1

    available_indices = [i for i in range(len(transform)) if cooldowns[i] == 0]
    
    if available_indices:
        transform_number = random.choice(available_indices)
        
        if timees % random_int == 1:
            obstacle(DISPLAY_WIDTH // 2 - 20 // 2 + transform[transform_number], -60, 50, 80)
            
            cooldowns[transform_number] = 90"""
  """
  def render(self):
    self.display.fill((25, 25, 25))

    self.render_elements()"""

  def accelerations(self):
      print('accel')
      acceleration_factor = acceleration_FACTORS[current_gear - 1]
      max_speed = max_speeds[current_gear - 1]

      # Handle acceleration
      if self.accelerate_pressed:
          if self.speed < max_speed:
              self.acceleration += acceleration_factor * self.acceleration * (1 - (self.speed / max_speed)) ** 20
              self.speed += self.acceleration
          
          if self.acceleration_delay < 1.5:
              self.acceleration_delay += 0.05
              car.y += self.acceleration_delay
              self.acceleration_delay_minus = 0.0  # Reset reverse delay

      # Handle deceleration
      elif self.deacelerate_pressed:
          if self.speed > 10:
              self.acceleration -= round(3 * self.acceleration * (1 - (self.speed / max_speed)) ** 20, 3)
              self.speed -= self.acceleration
          
          if self.acceleration_delay > -1.5:
              self.acceleration_delay -= 0.05
              car.y += self.acceleration_delay
              self.acceleration_delay_minus = 0.0  # Reset reverse delay

      # Gradually reset position when neither accelerating nor decelerating
      else:
        if (self.acceleration < 0.1):
          self.acceleration = 0.1

        if self.acceleration > 0.1 and self.speed > 10:
          self.acceleration -= self.acceleration * (1 - (speed / max_speed)) ** 20
          self.speed -= 0.3 * acceleration_factor * self.acceleration
          
        if self.acceleration_delay > -0.05 and self.acceleration_delay < 0.05:
            self.acceleration_delay = 0

        elif self.acceleration_delay > 0:
            self.acceleration_delay -= 0.05
            car.y -= self.acceleration_delay  # Move back down

        elif self.acceleration_delay < 0:
            self.acceleration_delay += 0.05
            car.y -= self.acceleration_delay  # Move back up

        # Gradual return of reverse delay if it was used
        if self.acceleration_delay_minus > 0:
            self.acceleration_delay_minus -= 0.05
            car.y -= self.acceleration_delay_minus

      # Clamp car.y to stay within the range of 360 to 400
      if car.y < 350:
          car.y = 350
      elif car.y > 410:
          car.y = 410

  """obstacles = []
  def obstacle(a, b, width, height):
    obstacles.append(pygame.Rect(a, b, width, height))"""

  def set_gear(self, gear):
    if 1 <= gear <= 4:
      if self.current_gear != gear:
        self.current_gear = gear
        self.acceleration = 0.1
        self.shift_cooldown_counter = SHIFT_COOLDOWN

  def cooldown_tick(self):
    if self.shift_cooldown_counter > 0:
      self.shift_cooldown_counter -= 1

  def is_cooldown_active(self):
    return self.shift_cooldown_counter > 0

  

  """for element in elements[:]:
    element.y += speed / 10
    pygame.draw.rect(display, (255, 255, 255), element)

    if element.top > DISPLAY_HEIGHT:
      elements.remove(element)
      amount_rect -= 1

  for element in obstacles[:]:
    element.y += speed / 10
    pygame.draw.rect(display, (200, 55, 20), element)

    if element.top > DISPLAY_HEIGHT:
      obstacles.remove(element)"""
  
  def draw(self):
    display.fill((25, 25, 25))

    for element in self.elements:
        pygame.draw.rect(display, (255, 255, 255), element)

    # Draw obstacles
    for obstacle in self.obstacles:
        pygame.draw.rect(display, (200, 55, 20), obstacle)
        
    pygame.draw.rect(display, (0, 255, 0), (0, 0, 300, 600))
    pygame.draw.rect(display, (0, 255, 0), (700, 0, 300, 600))
    pygame.draw.line(display, (255, 255, 255), (300, 0), (300, 600), 4)
    pygame.draw.line(display, (255, 255, 255), (700, 0), (700, 600), 4)

    car.draw()

    self.get_back_button.draw(display)


    font = pygame.font.Font(None, 36)
    texts = [
          (f"Gear: {self.current_gear}", (10, 10)),
          (f"Speed: {self.speed:.2f}", (10, 40)),
          (f"Acceleration: {self.acceleration}", (10, 70)),
          (f"Timees: {self.timees}", (10, 100)),
          (f"Timees Value: {self.timees_value}", (10, 130)),
          (f"Amount Rect: {self.amount_rect}", (10, 160)),
          (f"Acceleration Delay: {self.acceleration_delay}", (10, 190)),
    ]

    for text, pos in texts:      
        rendere_text = font.render(text, True, (255, 255, 255))
        display.blit(rendere_text, pos)
    
  def get_back(self):
    global current_screen
    current_screen = 'MAIN_MENU'

main_menu = MainMenu()
settings_menu = Settings_Menu()
game_menu = GameMenu()

current_screen = "MAIN_MENU"


def game_loop():
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if current_screen == "MAIN_MENU":
        main_menu.handle_events(event)
      elif current_screen == "SETTINGS":
        settings_menu.handle_events(event)
      elif current_screen == "GAME":
        game_menu.handle_events(event)

      if current_screen == "MAIN_MENU":
          main_menu.draw()
      elif current_screen == "SETTINGS":
          settings_menu.draw()
      elif current_screen == "GAME":
          game_menu.update()
          game_menu.draw()

      pygame.display.update()
      clock.tick(FPS)
      game_menu.timees += 1

game_loop()
pygame.quit()