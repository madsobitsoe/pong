#Pong with neural nets

I want to study and further understand neural nets and evolutionary algorithms. For this reason i decided to rewrite my old PoC pong clone into using neural net "brains" as players and pit them against a bad hardcoded AI.




##What have i done  
- *Written small clone of pong
This is a bad implementation, should probably be rewritten*

- *Written Neural Net*  
This is based on 'neural nets demystified'
https://www.youtube.com/watch?v=bxe2T-V8XRs

*Merged neural net with pong to control player*  
The neuralnet player is initialized with random weights
Takes ball coordinates as input and outputs a value that is interpreted as an action. 
The action is either move up, move down or stay. 

###What do i want to do
*I want to create bat evolution and evolve better bats*

####For this i need to
- Model weights (or neuralnets?) as bytes  
- write evolution code  
-- Mutation  
-- combining two 'brains'  
-- decide on fitness functions  
-- rewrite pong to play a game, not play forever  
-- Needs to output results, preferably to a textfile  
-- Create 'tournament' code for selecting brains to bring on to next generation  

###I also want to track this stuff, preferably using matplotlib
####For this i need to
- Learn matplotlib
- Figure out what data to save

### I want to make the GUI pluggable  
- There is no reason to watch the games, if i want to run for instance 10.000 iterations/generations.  


# How do i do what i am currently doing  
I have a neural network class.   
The class has various properties:  

| Property        | What is it                                                               |
| :---            | :---:                                                                    |
| inputLayerSize  | The size of the input layer of the neural net                            |
| outputLayerSize | The size of the outputlayer of the neural net                            |
| hiddenLayerSize | The size of the hidden layer of the neural net                           |
| W1              | The weights between the inputlayer and the hiddenlayer as a numpy array  |
| W2              | The weights between the hiddenlayer and the outputlayer as a numpy array |
|                 |                                                                          |



#What happens?   
When the forward function is called, a matrix of input is supplied.   
In the pong game, this matrix is a 2x1 matrix, containing distance from paddleY to ballY and the ball's xCoordinate.   

The dot-product of X and W1 is then calculated and stored in z2.   
This is run through the activation function (sigmoid), and stored in a2.   
The dot-product of a2 and and W2 is then saved in z3.   
z3 is run through the activation function and saved in yHat.  
yHat is returned.  


The sigmoid function is:  
```python
def sigmoid(self, z):
    # Apply sigmoid activation function
    return 1 / (1 + np.exp(-z))
```

This results in a value between 0 and 1.   
If the value is between 0.4 and 0.6, the paddle stays where it is.  
If it is less than 0.4, it moves up.  
If it is more than 0.6 it moves down.  




*Dependencies*  
- Pygame  
- Numpy  

