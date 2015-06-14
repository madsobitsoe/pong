import main


players = []

for x in range(5):
    game = main.Game(True)
    playerPoints = game.on_execute()
    player = game.player
    print playerPoints
    print player.neuralNet.W1
    print player.neuralNet.W2
    players.append((player, playerPoints))


i = 1
with open('players', "a") as text_file:
    for player in players:
        text_file.write('Player' + str(i) + ':\n ')
        text_file.write('Weights 1:\n')
        for weight in player[0].neuralNet.W1:
            text_file.write(str(weight) + '\n')
        text_file.write('Weights 2:\n')
        for weight in player[0].neuralNet.W2:
            text_file.write(str(weight) + '\n')
        text_file.write('Results from game: \n')
        text_file.write('Player score: ' + str(player[1][0]) + '\n')
        text_file.write('Opponent score: ' + str(player[1][1]) + '\n\n') 

        i += 1
                            
