# The neural network class
import numpy as np
class Neural_Network(object):
    def __init__(self):
        # Define Hyperparameters
        self.inputLayerSize = 2
        self.outputLayerSize = 1
        self.hiddenLayerSize = 3

        # Weights (parameters)
        # Layer 1 weights
        self.W1 = np.random.randn(self.inputLayerSize, self.hiddenLayerSize)

        # Layer 2 weights
        self.W2 = np.random.randn(self.hiddenLayerSize, self.outputLayerSize)
 
    def forward(self, X):
        # Normalize 
  #      X = X / np.amax(X, axis=0)
#        print 'X is: ' + str(X)

        # Propagate inputs through network
        # Layer 2 activities
        self.z2 = np.dot(X, self.W1)
        # Layer 2 activations
  #      print 'This is z2:'
   #     print self.z2
        self.a2 = self.sigmoid(self.z2)
#        print 'This is a2:'
 #       print self.a2
        # Layer 3 activations
        # This is where the outputs of the hidden layer are squashed together
        self.z3 = np.dot(self.a2, self.W2)
        # Predicted score
        # This runs the sigmoid activation function on z3 and saves it in yHat
        yHat = self.sigmoid(self.z3)
        return yHat

            
    def sigmoid(self, z):
        # Apply sigmoid activation function
        return 1 / (1 + np.exp(-z))


