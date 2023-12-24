# iypt_bracket_gen
Bracket generator for IYPT. Intellectual Genetic Optimization Algorithm

❗The how-to-use instructions is not yet written. Pray to god or ask @ad3ph

# Investigated algorithms
## Main metric - Fu coefficient
_Parameters and recommended values: Z, T_

## Genetic optimizer with randomized start
:triangular_flag_on_post: **Status**: in use

Upon the request "make X attempts of optimization with a maximum depth of Y" the program repeats the single optimization run X times. The resulting brackets from each run, along with corresponding matrices and Fu, are outputted as a response.
In a single optimization run, the program generates A as a random bracket, then cycles the following:
1. Makes a random permutation in A;
2. Compares the Fu of the new bracket with the Fu of the unmodified A. If the Fu has decreased, then the new bracket becomes A, otherwise A remains the unmodified one.
The cycle repeats until Y permutations are attempted without changing Fu. 
_Parameters and recommended values: X, Y_

### Sleep-like rearrangement
:triangular_flag_on_post: **Status**: in use

Every Z repetitions of previous algorithm's cycle, T random permutations are additionally performed. This increases the probability of finding the global minimum of Fu, but increases the execution time.
_Parameters and recommended values: Z, T_

## Teacher-trained neural network
:triangular_flag_on_post: **Status**: not supported

Training a neural network, convolutional or dense, on "before-after" dumps made in genetic optimizer work
_Parameters and recommended values:_

## Dense NN reinforcement learning using REINFORCE algorithm (without training data)
:triangular_flag_on_post: **Status**: in development

The [OpenAI/Farama Gymnasium API](https://github.com/Farama-Foundation/Gymnasium.git) is used.
_Parameters and recommended values:_
