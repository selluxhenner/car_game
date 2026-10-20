#Game made by Kevin Schmid

#imports
import pygame
import random
import math

#init the pygame
pygame.init()

# Constants
DISPLAY_WIDTH = 1000
DISPLAY_HEIGHT = 600
FPS = 60
SHIFT_COOLDOWN = 50
MIN_TIME_INTERVAL = 10  # Minimum time interval in frames
MAX_TIME_INTERVAL = 100
MAX_SPEEDS = [90, 140, 280, 330]
ACCELERATION_FACTORS = [0.5, 0.48, 0.32, 0.28]

# Initialization of display and clock
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Car Game')
clock = pygame.time.Clock()

#variable
speed = 10

#define button
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.borderRadius = 10
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

#event quit game
def quit_game():
    pygame.quit()
    quit()

#event start game
def start_game():
    global current_screen
    current_screen = "GAME"

#define main menu
class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 50)
        self.background_color = (50, 50, 50)
        self.button_color = (100, 100, 250)
        self.button_hover_color = (150, 150, 250)
        self.input_box = pygame.Rect(100, 100, 140, 50)
        self.active = False
        self.buttons = [
            Button(400, 200, 200, 70, "Start Game", self.button_font, self.button_color, self.button_hover_color, start_game),
            Button(400, 300, 200, 70, "Quit", self.button_font, self.button_color, self.button_hover_color, quit_game)
        ]

    #handle events
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                button.click()
            if (self.input_box.collidepoint(event.pos)):
              self.active = not self.active
            else:
                self.active = False

    def draw(self):
        display.fill(self.background_color)

        image = pygame.image.load('elements/background.jpg')
        scaled_image = pygame.transform.scale(image, (1000, 600))
        display.blit(scaled_image, (0, 0))

        for button in self.buttons:
            button.draw(display)

        self.input_box.w = 200
        font = pygame.font.Font(None, 40)
        text = ''
        txt_surface = font.render(text, True, (255, 255, 255))
        display.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        #pygame.draw.rect(display, (255, 23, 23), self.input_box, 2)
        font = pygame.font.Font(None, 36)
        texts = [
            (f"Drive: W,A,S,D", (10, 10)),
            (f"Gear change: E,R", (10, 40)),
        ]
        for text, pos in texts:
            render_text = font.render(text, True, (255, 255, 255))
            display.blit(render_text, pos)

#define car
class Car:
    def __init__(self):
        self.x = 490
        self.y = 380
        self.width = 70
        self.height = 200
        self.angle = 0
        self.left_pressed = False
        self.right_pressed = False

    def draw(self, surface):
        car_body_color = (50, 50, 255)
        car_wheel_color = (255, 255, 255)
        car_cover_color = (50, 50, 200)

        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        body_rect = pygame.Rect(15, 30, 50, 100)
        pygame.draw.rect(car_surface, car_body_color, body_rect)

        # Draw wheels and covers
        wheels = [(10, 40), (60, 40), (10, 100), (60, 100)]
        for (wx, wy) in wheels:
            pygame.draw.rect(car_surface, car_wheel_color, (wx, wy, 10, 20))

        covers = [(13, 38), (57, 38), (13, 98), (57, 98)]
        for (cx, cy) in covers:
            pygame.draw.rect(car_surface, car_cover_color, (cx, cy, 10, 24))

        rotated_car = pygame.transform.rotate(car_surface, self.angle)
        surface.blit(rotated_car, (self.x, self.y))

    def handle_movement(self):
        if self.left_pressed:
            if self.x > 295:
                self.x -= 5
                self.angle = min(self.angle + 1, 10)
            else:
                self.angle = max(self.angle - 1, 0)

        elif self.right_pressed:
            if self.x < 620:
                self.x += 5
                self.angle = max(self.angle - 1, -10)
            else:
                self.angle = min(self.angle + 1, 0)
        else:
          if self.angle < 0:
            self.angle = min(self.angle + 1, 0)
          if self.angle > 0:
            self.angle = max(self.angle - 1, 0)
        
#define game menu
class GameMenu:
    def __init__(self):
        self.current_gear = 1
        self.speed = 10
        self.acceleration = 0.1
        self.acceleration_pressed = False
        self.deceleration_pressed = False
        self.acceleration_delay = 0
        self.acceleration_delay_minus = 0
        self.timees = 0
        self.timees_value = 50
        self.elements = []
        self.obstacles = []
        self.obstacles_amount = 0
        self.car = Car()
        self.get_back_button = Button(780, 40, 180, 50, "Get Back", pygame.font.Font(None, 50), (100, 100, 250), (150, 150, 250), self.get_back)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.car.left_pressed = True
            elif event.key == pygame.K_d:
                self.car.right_pressed = True
            elif event.key == pygame.K_w:
                self.acceleration_pressed = True
            elif event.key == pygame.K_s:
                self.deceleration_pressed = True
            elif event.key == pygame.K_r:
              if self.current_gear < 4:
                self.current_gear += 1
                self.acceleration = 2
            elif event.key == pygame.K_f:
              if self.current_gear > 1:
                self.current_gear -= 1
                if self.acceleration > 3:
                  self.acceleration = self.acceleration / 2

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.car.left_pressed = False
            elif event.key == pygame.K_d:
                self.car.right_pressed = False
            elif event.key == pygame.K_w:
                self.acceleration_pressed = False
            elif event.key == pygame.K_s:
                self.deceleration_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
             self.get_back_button.click()

    def update(self):
        self.timees += 1
        self.car.handle_movement()

        # Update elements and obstacles
        self.update_elements()

        length = 60 
        gap_length = max(4, 30 - int(self.speed / 15))
        print(self.timees, gap_length)
        if self.speed > 400: 
            length = 40
        elif self.speed > 300: 
            length = 45
        elif self.speed > 200: 
            length = 50
        elif self.speed > 150: 
            length = 52
        elif self.speed > 100: 
            length = 55
        elif self.speed > 50: 
            length = 57

        if self.timees % gap_length == 1:
          y = -50  
          if self.elements:
            current_gap = self.elements[-1].y
            if current_gap > 30:
              self.elements.append(pygame.Rect(495, y, 10, length))
          else:
              self.elements.append(pygame.Rect(495, y, 10, length))

        if self.timees % 60 == 0 and self.obstacles_amount < 7: 
            width = 50
            height = 80
            integers = [325, 425, 525, 625]
            ran_int = random.randint(0, 3)
            self.obstacles.append(pygame.Rect(integers[ran_int], -height, width, height))
            self.obstacles_amount += 1

        self.update_obstacles()
        self.display_speedboard()

        # Draw elements and car
        self.draw()

        #acceleration
        acceleration_factor = ACCELERATION_FACTORS[self.current_gear - 1]
        max_speed = MAX_SPEEDS[self.current_gear - 1]
        if self.acceleration_pressed:
            if self.speed < max_speed:
                self.speed += acceleration_factor * self.acceleration * (1 - (self.speed / max_speed))
            if self.acceleration < 7:
                self.acceleration += 0.05
            if self.acceleration_delay < 1.5:
              self.acceleration_delay += 0.05
              self.car.y += self.acceleration_delay
              self.acceleration_delay_minus = 0.0

        #deceleration
        elif self.deceleration_pressed:
            if self.speed > 10:
                self.speed -= 3 * acceleration_factor * (1 - (self.speed / max_speed))
            if self.acceleration < 0.05:
              self.acceleration = 0
            elif self.acceleration > 0:
              self.acceleration -= 0.05
          
            if self.acceleration_delay > -1.5:
              self.acceleration_delay -= 0.05
              self.car.y += self.acceleration_delay
              self.acceleration_delay_minus = 0.0
        else:
            if self.speed > 10:
                self.speed -= 0.38 * acceleration_factor
            if self.acceleration < 0.05:
              self.acceleration = 0
            elif self.acceleration > 0:
              self.acceleration -= 0.005
          
            if self.acceleration_delay > -0.05 and self.acceleration_delay < 0.05:
                self.acceleration_delay = 0

            elif self.acceleration_delay > 0:
                self.acceleration_delay -= 0.05
                self.car.y -= self.acceleration_delay  # Move back down

            elif self.acceleration_delay < 0:
                self.acceleration_delay += 0.05
                self.car.y -= self.acceleration_delay  # Move back up

            # Gradual return of reverse delay if it was used
            if self.acceleration_delay_minus > 0:
                self.acceleration_delay_minus -= 0.05
                self.car.y -= self.acceleration_delay_minus

        # Clamp car.y to stay within the range of 360 to 400
        if self.car.y < 350:
            self.car.y = 350
        elif self.car.y > 410:
            self.car.y = 410

    def update_elements(self):
        for element in self.elements[:]:
            element.y += self.speed / 10
            if element.top > DISPLAY_HEIGHT:
                self.elements.remove(element)

    def update_obstacles(self):
        for obstacle in self.obstacles[:]:
            obstacle.y += self.speed / 10
            if obstacle.top > DISPLAY_HEIGHT:
                self.obstacles.remove(obstacle)
                self.obstacles_amount -= 1

    def draw(self):
        display.fill((25, 25, 25))

        for element in self.elements:
            pygame.draw.rect(display, (255, 255, 255), element)

        for obstacle in self.obstacles:
            pygame.draw.rect(display, (200, 55, 20), obstacle)

        # Draw the car
        self.car.draw(display)

        pygame.draw.rect(display, (0, 255, 0), (0, 0, 300, 600))
        pygame.draw.rect(display, (0, 255, 0), (700, 0, 300, 600))
        pygame.draw.line(display, (255, 255, 255), (300, 0), (300, 600), 4)
        pygame.draw.line(display, (255, 255, 255), (700, 0), (700, 600), 4)

        # Draw UI elements
        self.get_back_button.draw(display)

        # Display text
        self.display_text()
        self.display_speedboard()

    def display_text(self):
        font = pygame.font.Font(None, 36)
        texts = [
            (f"Gear: {self.current_gear}", (10, 10)),
            (f"Speed: {self.speed:.2f}", (10, 40)),
            (f"Acceleration: {self.acceleration}", (10, 70)),
            (f"Timees: {self.timees}", (10, 100)),
            (f"Timees Value: {self.timees_value}", (10, 130)),
        ]
        for text, pos in texts:
            render_text = font.render(text, True, (255, 255, 255))
            display.blit(render_text, pos)

    def display_speedboard(self):
        pos = [[780, 500], [920, 500]]
        radius = 60
        
        for index, position in enumerate(pos):
          start_angle = 0
          end_angle = math.pi
          speed_angle = self.speed / 350 * 180 if index == 0 else self.acceleration / 9 * 180
        
          arc = pygame.Rect(position[0] - radius, position[1] - radius, 2 * radius, 2 * radius)
          pygame.draw.arc(display, (255,255,255), arc, start_angle, end_angle)

          points = [(position[0], position[1]),  # Center point
            (position[0] - radius, position[1]),  # Leftmost point
            (position[0] + radius, position[1])]
          
          for angle in range(0, 181):
            x = position[0] + int(radius * math.cos(math.radians(angle)))
            y = position[1] - int(radius * math.sin(math.radians(angle)))  # Invert y-axis for Pygame
            points.append((x, y))
          
          pygame.draw.polygon(display, (0, 0, 0), points)

          line_surface = pygame.Surface((2 * radius, 2), pygame.SRCALPHA)
          line_surface.fill((0, 105, 205))
          # Rotate the line surface
          rotated_line = pygame.transform.rotate(line_surface, -speed_angle)  # Use negative angle to rotate counterclockwise

          # Calculate position to place the rotated line
          line_rect = rotated_line.get_rect(center=position)

          # Draw the rotated line
          display.blit(rotated_line, line_rect.topleft)

    def get_back(self):
        global current_screen
        current_screen = 'MAIN_MENU'

#define Game Loop
def game_loop():
    global current_screen
    current_screen = "MAIN_MENU"
    main_menu = MainMenu()
    game_menu = GameMenu()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_screen == "MAIN_MENU":
                main_menu.handle_events(event)
            elif current_screen == "GAME":
                game_menu.handle_events(event)

        # Update the game logic and draw
        if current_screen == "MAIN_MENU":
            main_menu.draw()
        elif current_screen == "GAME":
            game_menu.update()

        pygame.display.update()

        #frame rate at FPS
        clock.tick(FPS)

    pygame.quit()

#start game loop
game_loop()
