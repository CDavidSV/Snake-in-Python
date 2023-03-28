import pygame
import random

# Initialize pygame
window_width = 630
window_height = 696
top_margin = 66
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
background = pygame.image.load('assets/background_image.png').convert()
font = pygame.font.Font('assets/Fixedsys.ttf', 28)
background = pygame.transform.scale(background, (window_width, window_height - top_margin))
key_map = {119: "UP", 115: "DOWN", 97: "LEFT", 100: "RIGHT"}
images = [pygame.image.load('assets/first-car-right.png').convert_alpha(), #0
          pygame.image.load('assets/mid-car-right.png').convert_alpha(), #1
          pygame.image.load('assets/turn-car-right-up.png').convert_alpha(), #2
          pygame.image.load('assets/turn-car-down-right.png').convert_alpha(), #3
          pygame.image.load('assets/first-car-left.png').convert_alpha(), #4
          pygame.image.load('assets/mid-car-left.png').convert_alpha(), #5
          pygame.image.load('assets/first-car-top-up.png').convert_alpha(), #6
          pygame.image.load('assets/mid-car-top-up.png').convert_alpha(), #7
          pygame.image.load('assets/mid-car-top-down.png').convert_alpha(), #8
          pygame.image.load('assets/first-car-top-down.png').convert_alpha(), #9
          pygame.image.load('assets/mid-car-top-down.png').convert_alpha(), #10
          pygame.image.load('assets/turn-car-up-right.png').convert_alpha(), #11
          pygame.image.load('assets/turn-car-up-left.png').convert_alpha(),] #12

# set the window title
pygame.display.set_caption("Snake Game")

def update_high_score(high_score, score):
    if score < high_score:
        return high_score

    with open('high_score.txt', "w") as f:
        f.write(str(score))

    return score

def check_high_score():
    try:
        with open('high_score.txt', "r") as f:
            high_score = f.read().strip()
            if high_score.isdigit():
                return int(high_score)

        with open('high_score.txt', "w") as f:
            f.write('0')
        return 0
    except IOError:
        with open('high_score.txt', "w") as f:
            f.write('0')
        return 0

class Snake:
    def __init__(self, size):
        self.size = size
        self.snake_arr = [pygame.Vector2(300 - 60, 300 + top_margin), pygame.Vector2(300 - 30, 300 + top_margin), pygame.Vector2(300, 300 + top_margin)]
        self.snake_images = [{"pos": pygame.Vector2(size, 0), "img": images[4]}, {"pos": pygame.Vector2(size, 0), "img": images[1]}, {"pos": pygame.Vector2(size, 0), "img": images[0]}]
        self.length = len(self.snake_arr)
        self.direction = pygame.Vector2(size, 0)
        self.direction_update = pygame.Vector2(0, 0)
        self.direction_queue = []
        self.directions = {"UP": pygame.Vector2(0, -size), "DOWN": pygame.Vector2(0, size), "LEFT": pygame.Vector2(-size, 0), "RIGHT": pygame.Vector2(size, 0)}
        self.collided = False
        self.images_dictionary = {
            "RIGHT": images[1],
            "RIGHT_FIRST": images[0],
            "RIGHT_LAST": images[4],
            "LEFT": images[5],
            "LEFT_FIRST": images[4],
            "LEFT_LAST": images[0],
            "UP": images[7],
            "UP_FIRST": images[6],
            "UP_LAST": images[8],
            "DOWN": images[10],
            "DOWN_FIRST": images[9],
            "DOWN_LAST": images[6],
            "RIGHT_UP": images[2],
            "DOWN_RIGHT": images[3],
            "LEFT_UP": images[3],
            "DOWN_LEFT": images[2],
            "UP_RIGHT": images[11],
            "UP_LEFT": images[12],
            "LEFT_DOWN": images[11],
            "RIGHT_DOWN": images[12],
        }

    def check_direction(self, direction):
        if direction == pygame.Vector2(self.size, 0):
            return "RIGHT"
        elif direction == pygame.Vector2(-self.size, 0):
            return "LEFT"
        elif direction == pygame.Vector2(0, self.size):
            return "DOWN"
        else:
            return "UP"

    def change_direction(self, direction):
        direction = direction.upper()

        # Check if the directions is opposite to the current snake direction.
        direction_vector = self.directions[direction]
        if direction_vector == -self.direction_update:
            return

        if direction not in self.direction_queue:
            self.direction_queue.append(direction)
            self.direction_update = direction_vector

    def increase_length(self, points):
        self.length += points

    def move(self):
        if len(self.direction_queue) >= 1:
            self.direction = self.directions[self.direction_queue[0]]
            del self.direction_queue[0]

        if self.direction.x == 0 and self.direction.y == 0:
            return

        # Generate the new snake head in its corresponding position based on the direction.
        new_head = self.snake_arr[-1] + self.direction
        if new_head in self.snake_arr:
            self.collided = True # Check if the snake collided with itself.

        self.snake_arr.append(new_head)
        self.snake_images.append({"pos": self.direction, "img": self.images_dictionary[f"{self.check_direction(self.direction)}_FIRST"]}) # FIRST represents the first car of the train (head of the snake).

        prev_pos = self.snake_images[-2]["pos"]
        curr_pos = self.snake_images[-1]["pos"]
        # We check if the snake changed direction.
        if prev_pos != curr_pos:
            self.snake_images[-2] = {"pos": self.direction, "img": self.images_dictionary[f"{self.check_direction(prev_pos)}_{self.check_direction(curr_pos)}"]}
        else:
            self.snake_images[-2] = {"pos": self.direction, "img": self.images_dictionary[f"{self.check_direction(prev_pos)}"]}

        if len(self.snake_arr) > self.length:
            diff = abs(self.length - len(self.snake_arr))
            for i in range (0, diff):
                curr_pos = self.snake_images[1]["pos"]
                self.snake_images[1]["img"] = self.images_dictionary[f"{self.check_direction(curr_pos)}_LAST"] # The last car is added at the beginning of the array.
                del self.snake_images[0]
                del self.snake_arr[0]

    def draw(self):
        for index, body in enumerate(self.snake_arr):
            image = self.snake_images[index]["img"]
            window.blit(image, (body.x, body.y))

class Food:
    def __init__(self, size, x , y):
        self.size = size
        self.posX = x
        self.posY = y
        self.food_pos = pygame.Vector2(self.posX - self.size, self.posY - self.size)

    def changePos(self, x, y):
        self.food_pos = pygame.Vector2(x - self.size, y - self.size)
    
    def draw(self):
        pygame.draw.rect(window, 'red', pygame.Rect(self.food_pos.x, self.food_pos.y, self.size, self.size))

if __name__ == "__main__":
    snake = Snake(30)
    food = Food(30, random.randint(1, 21) * 30, random.randint(1, 21) * 30 + top_margin)
    move_interval = 100
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

            if event.type != pygame.KEYDOWN or event.key not in key_map:
                continue   
            
            # Check for keyboard input.
            snake.change_direction(key_map[event.key])

        # Check if it's time to move the player
        current_time = pygame.time.get_ticks()
        time_since_last_move = current_time - last_move_time
        if time_since_last_move >= move_interval:
            snake.move()
            last_move_time = current_time

        # Check if snake ate food.
        if snake.snake_arr[-1] == food.food_pos:
            food.changePos(random.randint(1, 21) * 30, random.randint(1, 21) * 30 + top_margin)
            snake.increase_length(1)
            score += 1
            score_text = font.render(f'Score: {score}', True, 'blue')

        # Check if the snake is out of bounds.
        if snake.snake_arr[-1].x > window_width - snake.size:
            snake.snake_arr[-1].x = 0
        elif snake.snake_arr[-1].x < 0:
            snake.snake_arr[-1].x = window_width - snake.size
        if snake.snake_arr[-1].y > window_height - snake.size:
            snake.snake_arr[-1].y = 0 + top_margin
        elif snake.snake_arr[-1].y < top_margin:
            snake.snake_arr[-1].y = window_height - snake.size

        # Check if the snake collided with itself.
        if snake.collided:
            running = False
            high_score = update_high_score(high_score, score)
            high_score_text = font.render(f'High Score: {high_score}', True, 'orange')
            break
        
        # Display updates
        window.fill('white')
        window.blit(background, (0, top_margin))
        window.blit(high_score_text, (200, 20))
        window.blit(score_text, (20, 20))
        snake.draw()
        food.draw()

        pygame.display.flip()
        clock.tick(300) # Limit the framerate to 300.

    pygame.quit()