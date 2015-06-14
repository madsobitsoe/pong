import main
import neuralNet as nn

players = []
results = []

# Create 5 players
for x in range(5):
    players.append(nn.Neural_Network())
# Play 5 games with each player
for x in range(5):
    for player in players:
        game = main.Game(False)
        playerPoints = game.on_execute(player)
        results.append("player " + str(players.index(player)) + '\nResult of game: ' + str(playerPoints))
        with open('players', 'a') as text_file:
            text_file.write('Game number: '+ str(x + 1) + '\n\n')
            text_file.write('Player' + str(players.index(player) + 1) + ':\n ')
            text_file.write('Weights 1:\n')
            for weight in player.W1:
                text_file.write(str(weight) + '\n')
            text_file.write('Weights 2:\n')
            for weight in player.W2:
                text_file.write(str(weight) + '\n')
            text_file.write('Results from game: \n')
            try:
                print 'PlayerPoints is of type: ' + str(type(playerPoints))

                text_file.write('Player score: ' + (str(playerPoints[0])) + '\n')
                text_file.write('Opponent score: ' + str(playerPoints[1]) + '\n\n')
            except TypeError:
                print 'PlayerPoints is of type: ' + str(type(playerPoints))

                text_file.write('Player score: No points, game was interrupted\n')
                text_file.write('Opponent score: No points, game was interrupted\n\n')             
for result in results:
    print result            
