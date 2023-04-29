from collections import deque
from random import choice
import pygame

# Initialize pygame
WINDOW_WIDTH = 630
WINDOW_HEIGHT = 696
TOP_MARGIN = 66
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Other variables
HIGH_SCORE_FILE = 'high_score.txt'
overlay = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT], pygame.SRCALPHA, 32)
overlay = overlay.convert_alpha()
overlay.fill((0, 0, 0, 200))
replay_btn = pygame.image.load('assets/buttons/replay_btn.png').convert_alpha()
background = pygame.image.load('assets/background_image_1.png').convert()
passenger = pygame.image.load('assets/passenger.png').convert_alpha()
font = pygame.font.Font('assets/fonts/Fixedsys.ttf', 28)
final_font = pygame.font.Font('assets/fonts/Fixedsys.ttf', 128)
controls_map = {pygame.K_w: "UP", pygame.K_s: "DOWN", pygame.K_a: "LEFT", pygame.K_d: "RIGHT", pygame.K_UP: "UP", pygame.K_DOWN: "DOWN", pygame.K_LEFT: "LEFT", pygame.K_RIGHT: "RIGHT"}
game_state = "stopped"
images = [pygame.image.load('assets/train_car_imgs/first-car-right.png').convert_alpha(), #0
          pygame.image.load('assets/train_car_imgs/mid-car-right.png').convert_alpha(), #1
          pygame.image.load('assets/train_car_imgs/turn-car-right-up.png').convert_alpha(), #2
          pygame.image.load('assets/train_car_imgs/turn-car-down-right.png').convert_alpha(), #3
          pygame.image.load('assets/train_car_imgs/first-car-left.png').convert_alpha(), #4
          pygame.image.load('assets/train_car_imgs/mid-car-left.png').convert_alpha(), #5
          pygame.image.load('assets/train_car_imgs/first-car-top-up.png').convert_alpha(), #6
          pygame.image.load('assets/train_car_imgs/mid-car-top-up.png').convert_alpha(), #7
          pygame.image.load('assets/train_car_imgs/mid-car-top-down.png').convert_alpha(), #8
          pygame.image.load('assets/train_car_imgs/first-car-top-down.png').convert_alpha(), #9
          pygame.image.load('assets/train_car_imgs/mid-car-top-down.png').convert_alpha(), #10
          pygame.image.load('assets/train_car_imgs/turn-car-up-right.png').convert_alpha(), #11
          pygame.image.load('assets/train_car_imgs/turn-car-up-left.png').convert_alpha(),] #12

# set the window title
pygame.display.set_caption("Snake Game")

class Snake:
    collided = False
    direction_queue = deque([])
    length = 3
    def __init__(self, size, init_pos_x, init_pos_y):
        self.size = size
        self.init_pos_x = init_pos_x
        self.init_pos_y = init_pos_y
        self.snake_arr = deque([pygame.Vector2(init_pos_x, init_pos_y + TOP_MARGIN), pygame.Vector2(init_pos_x - size, init_pos_y + TOP_MARGIN), pygame.Vector2(init_pos_x - size * 2, init_pos_y + TOP_MARGIN)])
        self.snake_images = deque([{"dir": pygame.Vector2(size, 0), "img": images[0]}, {"dir": pygame.Vector2(size, 0), "img": images[1]}, {"dir": pygame.Vector2(size, 0), "img": images[4]}])
        self.direction = pygame.Vector2(size, 0)
        self.direction_update = pygame.Vector2(size, 0)
        self.images_dictionary = {
            "RIGHT": images[1], # Car going right.
            "RIGHT_FIRST": images[0], # First car going right.
            "RIGHT_LAST": images[4], # Last car going right.
            "LEFT": images[5], # Car going left.
            "LEFT_FIRST": images[4], # First car going left.
            "LEFT_LAST": images[0], # Last car going left.
            "UP": images[7], # Car going up.
            "UP_FIRST": images[6], # First car going up.
            "UP_LAST": images[9], # Last car going up.
            "DOWN": images[10], # Car going down
            "DOWN_FIRST": images[9], # First car going down.
            "DOWN_LAST": images[6], # Last car going down.
            "RIGHT_UP": images[2], # Turning car going up from the right.
            "DOWN_RIGHT": images[3], # Turning car going down from the right.
            "LEFT_UP": images[3], # Turning car going up from the left.
            "DOWN_LEFT": images[2], # Turning car going up from the left.
            "UP_RIGHT": images[11], # Turning car going right from upward direction.
            "UP_LEFT": images[12], # Turning car going left from upward direction.
            "LEFT_DOWN": images[11], # Turning car going left from downward direction.
            "RIGHT_DOWN": images[12], # Turning car going right from downward direction.
        }

    def check_direction(self, direction):
        directions = {(0, -self.size): "UP",
                      (0, self.size): "DOWN", 
                      (-self.size, 0): "LEFT", 
                      (self.size, 0): "RIGHT",
                      }
        return directions[tuple(direction)]

    def change_direction(self, direction):
        directions = {"UP": pygame.Vector2(0, -self.size), 
                      "DOWN": pygame.Vector2(0, self.size), 
                      "LEFT": pygame.Vector2(-self.size, 0), 
                      "RIGHT": pygame.Vector2(self.size, 0)
                      }
        
        # Check if the directions is opposite to the current snake direction.
        direction = direction.upper()
        if directions[direction] != -self.direction_update and direction not in self.direction_queue:
            self.direction_queue.append(directions[direction])
            self.direction_update = directions[direction]

    def reset(self):
        self.direction = pygame.Vector2(self.size, 0)
        self.direction_update = pygame.Vector2(self.size, 0)
        self.direction_queue = deque([])
        self.length = 3
        self.collided = False
        self.snake_arr = deque([pygame.Vector2(self.init_pos_x, self.init_pos_y + TOP_MARGIN), pygame.Vector2(self.init_pos_x - self.size, self.init_pos_y + TOP_MARGIN), pygame.Vector2(self.init_pos_x - self.size * 2, self.init_pos_y + TOP_MARGIN) ])
        self.snake_images = deque([{"dir": pygame.Vector2(self.size, 0), "img": images[0]}, {"dir": pygame.Vector2(self.size, 0), "img": images[1]}, {"dir": pygame.Vector2(self.size, 0), "img": images[4]}])

    def increase_length(self):
        self.length += 1

    def move(self):
        if len(self.direction_queue) >= 1:
            self.direction = self.direction_queue[0]
            self.direction_queue.popleft()

        # Check if the snake is out of bounds.
        new_head = self.snake_arr[0].copy()

        # Generate the new snake head in its corresponding position based on the direction.
        new_head += self.direction
        
        if self.snake_arr[0].x >= WINDOW_WIDTH - self.size and self.direction.x > 0:
            new_head.x = 0
        elif self.snake_arr[0].x <= 0 and self.direction.x < 0:
            new_head.x = WINDOW_WIDTH - self.size
        if self.snake_arr[0].y >= WINDOW_HEIGHT - self.size and self.direction.y > 0:
            new_head.y = 0 + TOP_MARGIN
        elif self.snake_arr[0].y < TOP_MARGIN + self.size and self.direction.y < 0:
            new_head.y = WINDOW_HEIGHT - self.size

        if new_head in self.snake_arr:
            self.collided = True # Check if the snake collided with itself.
            return

        self.snake_arr.appendleft(new_head)
        self.snake_images.appendleft({"dir": self.direction, "img": self.images_dictionary[f"{self.check_direction(self.direction)}_FIRST"]}) # FIRST represents the first car of the train (head of the snake).

        # We check if the snake changed direction.
        prev_dir = self.snake_images[1]["dir"]
        curr_dir = self.snake_images[0]["dir"]
        if prev_dir != curr_dir:
            self.snake_images[1] = {"dir": self.direction, "img": self.images_dictionary[f"{self.check_direction(prev_dir)}_{self.check_direction(curr_dir)}"]}
        else:
            self.snake_images[1] = {"dir": self.direction, "img": self.images_dictionary[f"{self.check_direction(prev_dir)}"]}

        if len(self.snake_arr) > self.length:
            self.snake_images[-2]["img"] = self.images_dictionary[f"{self.check_direction(self.snake_images[-2]['dir'])}_LAST"] # The last car is added at the beginning of the array.
            self.snake_images.pop()
            self.snake_arr.pop()

    def draw(self):
        for body, image in zip(self.snake_arr, self.snake_images):
            window.blit(image["img"], (body.x, body.y))

class Food:
    def __init__(self, size, x , y):
        self.size = size
        self.posX = x
        self.posY = y
        self.food_pos = pygame.Vector2(self.posX, self.posY)

    def changePos(self, x, y):
        self.food_pos = pygame.Vector2(x, y)
    
    def draw(self):
        #pygame.draw.rect(window, 'red', pygame.Rect(self.food_pos.x, self.food_pos.y, self.size, self.size))
        window.blit(passenger, pygame.Rect(self.food_pos.x, self.food_pos.y, self.size, self.size))

def random_pos(start, end, skip=1, exclude=[]):
    unoccupied_positions = []

    for x in range(start, end):
        for y in range(start, end):
            position = pygame.Vector2(x * skip, y * skip + TOP_MARGIN)
            if position not in exclude:
                unoccupied_positions.append(position)
    return choice(unoccupied_positions)

def update_high_score(high_score, score):
    if score < high_score:
        return high_score

    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

    return score

def check_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            high_score = f.read().strip()
            if high_score.isdigit():
                return int(high_score)
            
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write('0')
        return 0
    except IOError:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write('0')
        return 0

if __name__ == "__main__":
    snake = Snake(30, 300, 300)
    random_food_pos = random_pos(1, 20, 30, snake.snake_arr)
    food = Food(30, random_food_pos.x, random_food_pos.y)
    move_interval = 100 # Speed
    score = 0
    high_score = check_high_score()
    score_text = font.render(f'Score: {score}', True, 'blue')
    high_score_text = font.render(f'High Score: {high_score}', True, 'orange')

    last_move_time = pygame.time.get_ticks()
    running = True

    while running:
        # Lister for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in controls_map and game_state != "lost":
                game_state = "started"
                snake.change_direction(controls_map[event.key])
                started = True  
            elif event.type == pygame.MOUSEBUTTONUP and game_state == "lost":
                game_state = "stopped"
                score = 0
                score_text = font.render(f'Score: {score}', True, 'blue')
                snake.reset()

        # Check if it's time to move the player
        current_time = pygame.time.get_ticks()
        time_since_last_move = current_time - last_move_time
        if time_since_last_move >= move_interval and game_state == "started":
            snake.move()
            last_move_time = current_time

        # Check if snake ate food.
        if snake.snake_arr[0] == food.food_pos:
            random_food_pos = random_pos(1, 21, 30, snake.snake_arr)
            food.changePos(random_food_pos.x, random_food_pos.y)
            snake.increase_length()
            score += 1
            if score >= high_score:
                high_score = score
            score_text = font.render(f'Score: {score}', True, 'blue')
            high_score_text = font.render(f'High Score: {high_score}', True, 'orange')

        # Check if the snake collided with itself.
        if snake.collided:
            game_state = "lost"
            high_score = update_high_score(high_score, score)
        
        # Display updates
        window.fill('white')
        window.blit(background, (0, TOP_MARGIN))
        window.blit(high_score_text, (200, 20))
        window.blit(score_text, (20, 20))
        snake.draw()
        food.draw()

        if game_state == "lost":
            final_score = final_font.render(f'{score}', True, 'blue')
            window.blit(overlay, (0, 0))
            window.blit(replay_btn, (WINDOW_WIDTH / 2 - replay_btn.get_width() / 2, WINDOW_HEIGHT / 2))
            window.blit(final_score, final_score.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 125)))

        pygame.display.flip()
    pygame.quit()