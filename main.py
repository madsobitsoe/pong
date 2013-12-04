import pygame

from random import randint

def load_png(name):
    # Load image and return image object
    fullname = os.path.join('res', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()

class Player():
    def __init__(self, width, height):
        self.x = width - 100
        self.y = height / 2
        self.height = 80
        self.width = 20

    def draw(self, display_surf):
        pygame.draw.rect(display_surf, (255, 255, 255), (self.x, self.y, self.width, self.height))
        
    def update(self, height):
        coords = pygame.mouse.get_pos()
        if coords[1] <= 0:
            self.y = 0
        if coords[1] >= height - self.height:
            self.y = height - self.height
        else:
            self.y = coords[1]

class Opponent():
    def __init__(self, width, height):
        self.x = 100
        self.y = height / 2
        self.height = 80
        self.width = 20
        self.speed = 0
        self.move_timer = 10
        
    def draw(self, display_surf):
        pygame.draw.rect(display_surf, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def move(self):
        if self.move_timer == 0:
            self.y += self.speed
        else:
            self.move_timer -= 1

    def update(self, ball_y, height):
        if ball_y < self.y + (self.height/2):
            self.speed -= 1
        if ball_y > self.y + (self.height/2):
            self.speed += 1
        
        if self.speed < -4:
            self.speed = -4
        if self.speed > 4:
            self.speed = 4

        if self.y < 0:
            self.y = 0
        if self.y + self.height > height:
            self.y = height - self.height
class Ball():
    def __init__(self):
        self.x = 320
        self.y = 240
        
        self.x_speed = 4
        self.y_speed = 4
        self.radius = 10
        self.player_scored = False
        self.opponent_scored = False
    def reset(self):
            
        self.x = 320
        self.y = 240
        if (randint(1, 10) % 2) == 0:
            self.x_speed = 4
        else:
            self.x_speed = -4
        self.y_speed = randint(-4, 4)
        self.player_scored = False
        self.opponent_scored = False
        

    def draw(self, display_surf):
        pygame.draw.circle(display_surf,( 0, 255, 0), (int(self.x), int(self.y)), self.radius, 0)
    

    def check_bounds(self, width, height):
        # Check left boundary
        if self.x - self.radius <= 0:
            self.player_scored = True
        # Check right boundary
        if self.x + self.radius >= width:
            self.opponent_scored = True
        # Check upper boundary
        if self.y - self.radius <= 0:
            self.y_speed = -self.y_speed
        # check lower boundary
        if self.y + self.radius >= height:
            self.y_speed = -self.y_speed

    def checkBat(self, opponent, player):
    # Check collision with player bat
        if self.x + self.radius > player.x and self.x - self.radius < player.x + player.width and self.y + self.radius >= player.y and self.y - self.radius < player.y + player.height:
            self.x = player.x - self.radius
            self.x_speed = -self.x_speed
            if self.x_speed > 0:
                self.x_speed += 0.2
            if self.x_speed < 0:
                self.x_speed -= 0.2
            if self.y_speed < 0:
                if self.y > player.y and self.y < player.y + 20:
                    self.y_speed -= 0.4
                if self.y > player.y + 20 and self.y < player.y + 60:
                    self.y_speed -= 0.2
                if self.y > player.y + 60 and self.y < player.y + 80:
                    self.y_speed -= 0.4
            if self.y_speed > 0:
                if self.y > player.y and self.y < player.y + 20:
                    self.y_speed += 0.4
                if self.y > player.y + 20 and self.y < player.y + 60:
                    self.y_speed += 0.2
                if self.y > player.y + 60 and self.y < player.y +80:
                    self.y_speed += 0.4
            opponent.move_timer = randint(1, 50)
    # Check collision with opponent bat
        if self.x - self.radius < opponent.x + opponent.width  and self.y + self.radius >= opponent.y and self.y - self.radius < opponent.y + opponent.height:
            self.x = opponent.x + opponent.width + self.radius
            self.x_speed = -self.x_speed
            if self.x_speed > 0:
                self.x_speed += 0.2
            if self.x_speed < 0:
                self.x_speed -= 0.2
            
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

class Main():
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.size = self.width, self.height = 640, 480
        
        self.player_points = 0
        self.opponent_points = 0
        
    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Pong clone')
        self.running = True
        self.font = pygame.font.SysFont('Arial', 40)
    def update_score(self):
        if self.ball.opponent_scored == True:
            self.opponent_points += 1 
            self.ball.reset()
        if self.ball.player_scored == True:
            self.player_points += 1
            self.ball.reset()
           
    def draw_score(self):
        score1 = self.font.render(str(self.opponent_points), True, (255, 255, 255))
        score2 = self.font.render(str(self.player_points), True, (255, 255, 255))
#        movetimer = self.font.render(str(self.opponent.move_timer), True, (255, 255, 255))
        self.display_surf.blit(score1, (10, 10))
        self.display_surf.blit(score2, (600, 10))
#        self.display_surf.blit(movetimer, (10, 50))

    def update_world(self):
        self.ball.check_bounds(self.width, self.height)
        self.ball.checkBat(self.opponent, self.player)
        self.ball.move()
        self.player.update(self.height)
        self.opponent.update(self.ball.y, self.height)
        self.opponent.move()
        self.update_score()
    
    def render(self):

        self.display_surf.fill((0, 0, 0,))
        self.ball.draw(self.display_surf)
        self.player.draw(self.display_surf)
        self.opponent.draw(self.display_surf)
        self.draw_score()
        pygame.display.flip()
        
    def on_execute(self):
        if self.on_init() == False:
            self.running = False
        self.player = Player(self.width, self.height)
        self.opponent = Opponent(self.width, self.height)
        self.ball = Ball()

        while (self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
            self.update_world()
            self.render()
            



if __name__ == '__main__' :
    game = Main()
    game.on_execute()