import pygame
import random

pygame.init()

# Constants
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 600


# Initialization
display = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
FPS = 60

speed = 10
max_speeds = [140, 220, 310, 400]
acceleration = 0.1
acceleration_FACTORS = [0.5, 0.48, 0.32, 0.28]
current_gear = 1
accelerate_pressed = False
acceleration_delay = 0
acceleration_delay_minus = 0
deacelerate_pressed = False
left_pressed = False
right_pressed = False
SHIFT_COOLDOWN = 50
SHIFT_COOLDOWN_COUNTER = 0
car_angle = 0

x_car = 490

MIN_TIME_INTERVAL = 10  # Minimum time interval in frames
MAX_TIME_INTERVAL = 100 

elements = []
amount_rect = 0
timees = 0
timees_value = 0
x = DISPLAY_WIDTH // 2 - 10 // 2
y = 0

gap = 0
length = 0

ELEMENT_WIDTH = 70 
ELEMENT_HEIGHT = 200 #4000 / max_speeds[current_gear - 1]
ELEMENT_GAP = 6000 / max_speeds[current_gear - 1]  

def accelerations():
    global speed, acceleration, current_gear, accelerate_pressed, deacelerate_pressed, acceleration_delay, acceleration_delay_minus, max_speed

    acceleration_factor = acceleration_FACTORS[current_gear - 1]
    max_speed = max_speeds[current_gear - 1]

    # Handle acceleration
    if accelerate_pressed:
        if speed < max_speed:
            acceleration += acceleration_factor * acceleration * (1 - (speed / max_speed)) ** 20
            speed += acceleration
        
        if acceleration_delay < 1.5:
            acceleration_delay += 0.05
            car.y += acceleration_delay
            acceleration_delay_minus = 0.0  # Reset reverse delay

    # Handle deceleration
    elif deacelerate_pressed:
        if speed > 10:
            acceleration -= round(3 * acceleration * (1 - (speed / max_speed)) ** 20, 3)
            speed -= acceleration
        
        if acceleration_delay > -1.5:
            acceleration_delay -= 0.05
            car.y += acceleration_delay
            acceleration_delay_minus = 0.0  # Reset reverse delay

    # Gradually reset position when neither accelerating nor decelerating
    else:
      if (acceleration < 0.1):
         acceleration = 0.1

      if acceleration > 0.1 and speed > 10:
        acceleration -= acceleration * (1 - (speed / max_speed)) ** 20
        speed -= 0.3 * acceleration_factor * acceleration
        
      if acceleration_delay > -0.05 and acceleration_delay < 0.05:
          acceleration_delay = 0

      elif acceleration_delay > 0:
          acceleration_delay -= 0.05
          car.y -= acceleration_delay  # Move back down

      elif acceleration_delay < 0:
          acceleration_delay += 0.05
          car.y -= acceleration_delay  # Move back up

      # Gradual return of reverse delay if it was used
      if acceleration_delay_minus > 0:
          acceleration_delay_minus -= 0.05
          car.y -= acceleration_delay_minus

    # Clamp car.y to stay within the range of 360 to 400
    if car.y < 350:
        car.y = 350
    elif car.y > 410:
        car.y = 410

obstacles = []
def obstacle(a, b, width, height):
  obstacles.append(pygame.Rect(a, b, width, height))

def set_gear(gear):
  global current_gear, acceleration, SHIFT_COOLDOWN_COUNTER

  if 1 <= gear <= 4:
    if current_gear != gear:
      current_gear = gear
      acceleration = 0.1
      SHIFT_COOLDOWN_COUNTER = SHIFT_COOLDOWN

def cooldown_tick():
  global SHIFT_COOLDOWN_COUNTER

  if SHIFT_COOLDOWN_COUNTER > 0:
    SHIFT_COOLDOWN_COUNTER -= 1

def is_cooldown_active():
  return SHIFT_COOLDOWN_COUNTER > 0

def drive():
  global x_car, car_angle, left_pressed, right_pressed

  if left_pressed == True:
    if x_car > 290:
      x_car -= 5
      
      if car_angle < 10:
        car_angle += 1
      car.update_position()

  else:
    if car_angle > 0:
      car_angle -= 1
  
  if right_pressed == True:
    if x_car < 700 - ELEMENT_WIDTH:
      x_car += 5
      
      if car_angle > -10:
        car_angle -= 1
      car.update_position()
  else:
    if car_angle < 0:
      car_angle += 1



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

    if self.is_hovered:
      pygame.draw.rect(screen, self.hover_color, self.rect)
    else:
      pygame.draw.rect(screen, self.color, self.rect)

    text_surface = self.font.render(self.text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=self.rect.center)
    screen.blit(text_surface, text_rect)
  
  def click(self):
    if self.is_hovered and self.action:
       self.action()

def draw_car(surface, width, height):
  car_body_color = (50, 50, 255)  # Blue body
  car_body_top = (100, 0, 0)
  car_wheel_color = (255, 255, 255)
  car_cover_color = (50, 50, 200)

  body_rect = pygame.Rect(15, 30, 50, 100)  
  pygame.draw.rect(surface, car_body_color, body_rect)
  wheel_1 = pygame.Rect(10, 40, 10, 20)  
  wheel_2 = pygame.Rect(60, 40, 10, 20)  
  wheel_3 = pygame.Rect(10, 100, 10, 20)  
  wheel_4 = pygame.Rect(60, 100, 10, 20)  
  pygame.draw.rect(surface, car_wheel_color, wheel_1)
  pygame.draw.rect(surface, car_wheel_color, wheel_2)
  pygame.draw.rect(surface, car_wheel_color, wheel_3)
  pygame.draw.rect(surface, car_wheel_color, wheel_4)
  
  cover_1 = pygame.Rect(13, 38, 10, 24)  
  cover_2 = pygame.Rect(57, 38, 10, 24)  
  cover_3 = pygame.Rect(13, 98, 10, 24)  
  cover_4 = pygame.Rect(57, 98, 10, 24)  
  pygame.draw.rect(surface, car_cover_color, cover_1)
  pygame.draw.rect(surface, car_cover_color, cover_2)
  pygame.draw.rect(surface, car_cover_color, cover_3)
  pygame.draw.rect(surface, car_cover_color, cover_4)

def main_menu():
  menu_running = True

  font = pygame.font.Font(None, 74)
  button_font = pygame.font.Font(None, 50)
  background_color = (50, 50, 50)
  button_color = (100, 100, 250)
  button_hover_color = (150, 150, 250)
  
  start_button = Button(400, 200, 200, 70, "Start Game", button_font, button_color, button_hover_color, start_game)
  quit_button = Button(400, 300, 200, 70, "Quit", button_font, button_color, button_hover_color, quit_game)

  while menu_running:
    display.fill(background_color)

    for event in pygame.event.get():
      if event.type == pygame.QUIT: 
        menu_running = False
        pygame.quit()
        quit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          start_button.click()
          quit_button.click()

    start_button.draw(display)
    quit_button.draw(display)

    pygame.display.update()
    clock.tick(FPS)

def times():
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

  timees += 1

class Car:
  def __init__(self):
    self.x = x_car
    self.y = 380
    self.width =  ELEMENT_WIDTH
    self.height = ELEMENT_HEIGHT

  def update_position(self):
    self.x = x_car

  def draw(self):
    car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
    draw_car(car_surface, self.width, self.height)
    rotated_car = pygame.transform.rotate(car_surface, car_angle)
    display.blit(rotated_car, (self.x, self.y))
car = Car()

def start_game():
  global main_menu_running
  main_menu_running = False
  game()

def quit_game():
  pygame.quit()
  quit()

def get_back():
  print('click')
  global main_menu_running
  main_menu_running = True
  main_menu()
  pygame.quit()
   

def game():
  global accelerate_pressed, deacelerate_pressed, current_gear, acceleration, right_pressed, left_pressed, gap, length, timees, amount_rect

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          accelerate_pressed = True

        elif event.key == pygame.K_s: 
          deacelerate_pressed = True

        elif event.key == pygame.K_r:
          if current_gear < 4:
            x_gear = current_gear
            set_gear(x_gear + 1)

        elif event.key == pygame.K_a:
          left_pressed = True

        elif event.key == pygame.K_d:
          right_pressed = True

        elif event.key == pygame.K_f:
          if current_gear > 0:
            x_gear = current_gear
            set_gear(x_gear - 1)

      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          accelerate_pressed = False

        elif event.key == pygame.K_s:
          deacelerate_pressed = False

        elif event.key == pygame.K_a:
          left_pressed = False

        elif event.key == pygame.K_d:
          right_pressed = False
      
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          get_back_button.click()
    
    cooldown_tick()

    if not is_cooldown_active():
      accelerations()

    else:
      acceleration = 0.1

    drive()
    times()

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
            
            cooldowns[transform_number] = 90

    display.fill((25, 25, 25))

    for element in elements[:]:
      element.y += speed / 10
      pygame.draw.rect(display, (255, 255, 255), element)

      if element.top > DISPLAY_HEIGHT:
        elements.remove(element)
        amount_rect -= 1

    for element in obstacles[:]:
      element.y += speed / 10
      pygame.draw.rect(display, (200, 55, 20), element)

      if element.top > DISPLAY_HEIGHT:
        obstacles.remove(element)
    
    pygame.draw.rect(display, (0, 255, 0), (0, 0, 300, 600))
    pygame.draw.rect(display, (0, 255, 0), (700, 0, 300, 600))
    pygame.draw.line(display, (255, 255, 255), (300, 0), (300, 600), 4)
    pygame.draw.line(display, (255, 255, 255), (700, 0), (700, 600), 4)

    font = pygame.font.Font(None, 36)
    text2 = font.render(f"speed: {speed: .2f}", True, (255, 255, 255))
    text1 = font.render(f"Gear: {current_gear}", True, (255, 255, 255))
    text4 = font.render(f"timees: {timees}", True, (255, 255, 255))
    text3 = font.render(f"Aceleration: {acceleration}", True, (255, 255, 255))
    text5 = font.render(f"timees_value: {timees_value}", True, (255, 255, 255))
    text6 = font.render(f"amount_rect: {amount_rect}", True, (255, 255, 255))
    text7 = font.render(f"acceleration_delay: {acceleration_delay}", True, (255, 255, 255))
    display.blit(text1, (10, 10))
    display.blit(text2, (10, 40))
    display.blit(text3, (10, 70))
    display.blit(text4, (10, 100))
    display.blit(text5, (10, 130))
    display.blit(text6, (10, 160))
    display.blit(text7, (10, 190))

    button_font = pygame.font.Font(None, 50)
    button_color = (100, 100, 250)
    button_hover_color = (150, 150, 250)
    get_back_button = Button(780, 40, 180, 50, "Get Back", button_font, button_color, button_hover_color, get_back)
    get_back_button.draw(display)



    car.draw()

    #print(f"Gear: {current_gear}: speed: {speed:.2f}")

    pygame.display.update()
    clock.tick(FPS)

main_menu()