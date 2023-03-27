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
length_increment = 1
key_map = {119: "UP", 115: "DOWN", 97: "LEFT", 100: "RIGHT"}

class Snake:
    def __init__(self, size):
        self.width = size
        self.height = size
        self.snakeArr = [pygame.Vector2(300 - 60, 300 + top_margin), pygame.Vector2(300 - 30, 300 + top_margin), pygame.Vector2(300, 300 + top_margin)]
        self.length = len(self.snakeArr)
        self.direction = pygame.Vector2(0, 0)
        self.curr_direction_string = "RIGHT"
        self.direction_queue = []
        self.directions = {"UP": pygame.Vector2(0, -size), "DOWN": pygame.Vector2(0, size), "LEFT": pygame.Vector2(-size, 0), "RIGHT": pygame.Vector2(size, 0)}
        self.opposite_directions = {"UP": "DOWN", "LEFT": "RIGHT", "DOWN": "UP", "RIGHT": "LEFT"}
        self.collided = False
    
    def change_direction(self, direction):
        direction = direction.upper()

        # Check if the directions is opposite to the current snake direction.
        if direction == self.opposite_directions[self.curr_direction_string]:
            return

        if direction not in self.direction_queue:
            self.direction_queue.append(direction)
            self.curr_direction_string = direction

    def increase_length(self, points):
        self.length += points

    def move(self):
        if len(self.direction_queue) >= 1:
            self.direction = self.directions[self.direction_queue[0]]
            del self.direction_queue[0]

        if self.direction.x == 0 and self.direction.y == 0:
            return # If there is no direction then return

        # Generate the new snake head in its corresponding position based on the direction.
        newHead = self.snakeArr[-1] + self.direction
        if newHead in self.snakeArr:
            self.collided = True # Check if the snake collided with itself.

        self.snakeArr.append(newHead)

        if len(self.snakeArr) > self.length:
            diff = abs(self.length - len(self.snakeArr))
            for i in range (0, diff):
                del self.snakeArr[0]

    def draw(self):
        for body in self.snakeArr:
            pygame.draw.rect(window, 'black', pygame.Rect(body.x, body.y, self.width, self.height))

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
    text = font.render(f'Score: {score}', True, 'blue')

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
        if snake.snakeArr[-1] == food.food_pos:
            food.changePos(random.randint(1, 21) * 30, random.randint(1, 21) * 30 + top_margin)
            snake.increase_length(length_increment)
            score += 1
            text = font.render(f'Score: {score}', True, 'blue')

        # Check if the snake is out of bounds.
        if snake.snakeArr[-1].x > window_width - snake.width:
            snake.snakeArr[-1].x = 0
        elif snake.snakeArr[-1].x < 0:
            snake.snakeArr[-1].x = window_width - snake.width
        
        if snake.snakeArr[-1].y > window_height - snake.height:
            snake.snakeArr[-1].y = 0 + top_margin
        elif snake.snakeArr[-1].y < top_margin:
            snake.snakeArr[-1].y = window_height - snake.height

        # Check if the snake collided with itself.
        if snake.collided:
            running = False
        
        # Display updates
        window.fill('white')
        window.blit(background, (0, top_margin))
        window.blit(text, (20, 20))
        snake.draw()
        food.draw()

        pygame.display.flip()
        clock.tick(60) # Limit the framerate to 60.

    pygame.quit()