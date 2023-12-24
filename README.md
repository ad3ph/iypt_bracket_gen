# iypt_bracket_gen
Bracket generator for IYPT. Intellectual Genetic Optimization Algorithm

❗ The how-to-use instructions is not yet written. Pray to god or ask @ad3ph

# Definitions
A bracket is a table of teams participating in each room and in each physics fight.
Here's an example of a bracket for 10 teams and two physics fights (imaginary teams are called Alpha, Beta, ...).

| PF | Room A               | Room B          | Room C              |
|----|----------------------|-----------------|---------------------|
| 1  | Alpha, Beta, Gamma   | Epsilon, Nu, Mu | Delta, Xi, Chi, Phi |
| 2  | Gamma, Nu, Xi, Alpha | Chi, Beta, Mu   | Delta, Epsilon, Phi |

The brackets are regularized by the Rules of the Tournament, stating that:
- 3 or 4 teams may participate in a fight
- The first role in a fight depends on the position in this fight's bracket: Reporter, Opponent, Reviewer in 3 teams fight; if the fourth team is present, they start their fight with Observer role.
- In one PF (in one row), team have to appear once and only once (obviously)

We are trying to generate the most optimal brackets, fulfilling the following criteria as much as possible, in the order of decreasing importance:
1. A: Any two teams should never see each other twice in the whole tournament
2. B: Teams should never participate in four-team fights (because this is tiring)
3. C: Teams should always have their first roles different in all fights (a team's strategy depends heavily on their first role)
4. D: Teams should play in each physical room only once (due to different air & temp conditions, projector quality, convenience etc.)
4. E: Teams should never play two consequent four team fights (c'mon, guys are tired!)
5. F: There are sets of teams never playing with each other (the organizers then are able to regularize Drawing Lots procedure, making conflicted teams (one school or one country) never meet)

In program, a team is represented as an integer.
The representation of a bracket in code is a Bracket class wrapper around a nested list. Here's an example, representing a bracket for 10 teams and two physics fights.
```python
[
        [[1, 2, 5], [7, 3, 9], [8, 6, 4, 10]],
        [[5, 3, 6, 1], [4, 2, 9], [8, 7, 10]]
]
```

# Main metric - Fu coefficient
The Fu coefficient (pronounced as 'foo', from Russian _фу_ - _yuk_, an expression of disgust) is introduced as a metric for a bracket showing how bad the bracket is in fulfilling the optimization criteria.
## Calculation method
:triangular_flag_on_post: **Status**: criteria A, B, C, D, E are supported currently.

<...>

## Code implementation
<...>

# Investigated algorithms of generating an optimal bracket
## Genetic optimizer with randomized start
:triangular_flag_on_post: **Status**: in use

Upon the request "make X attempts of optimization with a maximum depth of Y" the program repeats the single optimization run X times. The resulting brackets from each run, along with corresponding matrices and Fu, are outputted as a response.
In a single optimization run, the program generates A as a random bracket, then cycles the following:
1. Makes a random permutation in A;
2. Compares the Fu of the new bracket with the Fu of the unmodified A. If the Fu has decreased, then the new bracket becomes A, otherwise A remains the unmodified one.

The cycle repeats until Y permutations are attempted without changing Fu. 

_Parameters and recommended values: <...>_

### Sleep-like rearrangement
:triangular_flag_on_post: **Status**: in use

Every Z repetitions of previous algorithm's cycle, T random permutations are additionally performed. This increases the probability of finding the global minimum of Fu, but increases the execution time.

_Parameters and recommended values: <...>_

## Teacher-trained neural network
:triangular_flag_on_post: **Status**: not supported

Training a neural network, convolutional or dense, on "before-after" dumps made in genetic optimizer work.
<...>

_Parameters and recommended values: <...>_

## Dense NN reinforcement learning using REINFORCE algorithm (without training data)
:triangular_flag_on_post: **Status**: in development

The [OpenAI/Farama Gymnasium API](https://github.com/Farama-Foundation/Gymnasium.git) is used.
### Observations space
<...>
### Actions space
<...>
### NN architecture
<...>

_Parameters and recommended values: <...>_
