import pygame
import sys
import numpy as np
from random import randint
import neuralNet as nn

class NeuralNetPlayer():
    def __init__(self, width, height, neuralNet=None):
        self.x = width - 100
        self.y = height / 2
        self.height = 80
        self.width = 20
        if neuralNet is None:
            self.neuralNet = nn.Neural_Network()
        else:
            self.neuralNet = neuralNet
        
        
        
        # The bat needs to go up, stay put or go down.
        # -1 is up, 0 is stay and 1 is down
        self.currentAction = 0
        # The amount of pixels to move by each update
        self.moveLength = 5
        
    def draw(self, display_surf):
        pygame.draw.rect(display_surf, (255, 255, 255), (self.x, self.y, self.width, self.height))
        
    def update(self, height, ballY, ballX):

        # Calculate action with network
        print ballY, ballX
        print self.y
        self.currentAction = self.neuralNet.forward(np.array(([ballY - self.y, ballX]), dtype=float)) 
        print 'Current action: ' + str(self.currentAction)
        
        
        if self.y <= 0:
            self.y = 0
 
        if self.y >= height - self.height:
            self.y = height - self.height - 5
        else:
            if self.currentAction < 0.4:
                self.currentAction = -1
            if self.currentAction > 0.6:
                self.currentAction = 1
            if self.currentAction >= 0.4 and self.currentAction <= 0.6:
                self.currentAction = 0    

            self.y += self.currentAction * self.moveLength


            
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
        if self.x - self.radius <= 10:
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
        if self.x - self.radius < opponent.x + opponent.width  and self.x - self.radius > opponent.x and self.y + self.radius >= opponent.y and self.y - self.radius < opponent.y + opponent.height:
            self.x = opponent.x + opponent.width + self.radius
            self.x_speed = -self.x_speed
            if self.x_speed > 0:
                self.x_speed += 0.2
            if self.x_speed < 0:
                self.x_speed -= 0.2
            
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

class Game():
    def __init__(self, withGUI=True):
        self.withGUI = withGUI
        self.running = True
        self.display_surf = None
        self.size = self.width, self.height = 640, 480
        
        self.player_points = 0
        self.opponent_points = 0
        
    def on_init(self):
        if (self.withGUI):
            pygame.init()
            self.display_surf = pygame.display.set_mode(self.size)
            pygame.display.set_caption('Pong with neural nets')
            self.font = pygame.font.SysFont('Arial', 40)
            self.weightsFont = pygame.font.SysFont('Arial', 10)
        self.running = True

    def update_score(self):
        if self.ball.opponent_scored == True:
            self.opponent_points += 1 
            self.ball.reset()
        if self.ball.player_scored == True:
            self.player_points += 1
            self.ball.reset()
           
    def draw_score(self):
        #setting up stuff to render
        score1 = self.font.render(str(self.opponent_points), True, (255, 255, 255))
        score2 = self.font.render(str(self.player_points), True, (255, 255, 255))
        #movetimer = self.font.render(str(self.opponent.move_timer), True, (255, 255, 255))
        print self.player.neuralNet.W1

        w1 = 'Weights for first node: '
        for weight in self.player.neuralNet.W1[0]:
            w1 += format('%.4f, ' % weight)
        w2 = 'Weights for second node: '
        for weight in self.player.neuralNet.W1[1]:
            w2 += format('%.4f, ' % weight)

        w3 = 'Weights for second layer: '
        for weight in self.player.neuralNet.W2:
            w3 += format('%.4f, ' % weight)
        

        weights1 = self.weightsFont.render(w1, True, (255, 240, 240))
        weights2 = self.weightsFont.render(w2, True, (255, 240, 240))
        weights3 = self.weightsFont.render(w3, True, (255, 240, 240))

        currentAction = self.weightsFont.render(format('Current Action: %.1f' % self.player.currentAction), True, (255,140,140))
        # Actual blitting to display surface
        self.display_surf.blit(score1, (10, 10))
        self.display_surf.blit(score2, (600, 10))
        # self.display_surf.blit(movetimer, (10, 50))
        self.display_surf.blit(weights1, (400, 50))
        self.display_surf.blit(weights2, (400, 65))
        self.display_surf.blit(weights3, (400, 80))
        self.display_surf.blit(currentAction, (400, 100))
        
    def update_world(self):
        self.ball.check_bounds(self.width, self.height)
        self.ball.checkBat(self.opponent, self.player)
        self.ball.move()
        self.player.update(self.height, self.ball.y, self.ball.x)
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
        
    def on_execute(self, neuralNet=None):
        if self.on_init() == False:
            self.running = False
#        self.player = Player(self.width, self.height)

        if neuralNet==None:
            neuralNet = nn.Neural_Network()
        self.player = NeuralNetPlayer(self.width, self.height, neuralNet)
        self.opponent = Opponent(self.width, self.height)
        self.ball = Ball()

        while (self.running):
            if (self.player_points == 5 or self.opponent_points == 5):
                if (self.withGUI):
                    pygame.quit()
#                with open('output.txt', "a") as text_file:
#                   text_file.write('player points: ' + str(self.player_points) + ',')
#                   text_file.write('opponent points: ' + str(self.opponent_points)+ ',')
                return (self.player_points, self.opponent_points)
                #return ('Player: ' + str(self.player_points) + '\nOpponent: ' + str( self.opponent_points))
            if (self.withGUI):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.neuralNet = nn.Neural_Network()
                            print 'new NN created for player'
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
            self.update_world()
            if (self.withGUI):
                self.render()
        return self.player_points



if __name__ == '__main__' :
    game = Game(False)
    game.on_execute()
