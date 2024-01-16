import numpy as np
import gymnasium as gym
from gymnasium import utils
from gymnasium.spaces import Box, MultiBinary
from typing import Optional
import numpy as np

class BracketGen(gym.Env):
    """
    ## Description

    This environment is the environment storing a logic behind the brackets for IYPT.
		
    ## Action Space
    The agent should yield a 2-element vector for actions.

    The action space is a discrete `(team 1, team 2)` each number in range `[1, N_teams]`, meaning the agent wants to
    swap team 1 and team 2 places.

    ## Observation Space

    The state space consists of positional values of different body parts of
    the pendulum system, followed by the velocities of those individual parts (their derivatives)
    with all the positions ordered before all the velocities.

    The observation is a `ndarray` with shape `(4,)` where the elements correspond to the following:

    | Num | Observation                                   | Min  | Max | Name (in corresponding XML file) | Joint | Unit                      |
    | --- | --------------------------------------------- | ---- | --- | -------------------------------- | ----- | ------------------------- |
    | 0   | position of the cart along the linear surface | -Inf | Inf | slider                           | slide | position (m)              |
    | 1   | vertical angle of the pole on the cart        | -Inf | Inf | hinge                            | hinge | angle (rad)               |
    | 2   | linear velocity of the cart                   | -Inf | Inf | slider                           | slide | velocity (m/s)            |
    | 3   | angular velocity of the pole on the cart      | -Inf | Inf | hinge                            | hinge | anglular velocity (rad/s) |


    ## Rewards

    The goal is to make the inverted pendulum stand upright (within a certain angle limit)
    as long as possible - as such a reward of +1 is awarded for each timestep that
    the pole is upright.

    ## Starting State
    All observations start in state
    (0.0, 0.0, 0.0, 0.0) with a uniform noise in the range
    of [-0.01, 0.01] added to the values for stochasticity.

    ## Episode End
    The episode ends when any of the following happens:

    1. Truncation: The episode duration reaches 1000 timesteps.
    2. Termination: Any of the state space values is no longer finite.
    3. Termination: The absolute value of the vertical angle between the pole and the cart is greater than 0.2 radian.

    ## Arguments

    No additional arguments are currently supported.

    ```python
    import gymnasium as gym
    env = gym.make('InvertedPendulum-v4')
    ```
    There is no v3 for InvertedPendulum, unlike the robot environments where a
    v3 and beyond take `gymnasium.make` kwargs such as `xml_file`, `ctrl_cost_weight`, `reset_noise_scale`, etc.
    ```python
    import gymnasium as gym
    env = gym.make('InvertedPendulum-v2')
    ```

    ## Version History

    * v4: All MuJoCo environments now use the MuJoCo bindings in mujoco >= 2.1.3
    * v3: Support for `gymnasium.make` kwargs such as `xml_file`, `ctrl_cost_weight`, `reset_noise_scale`, etc. rgb rendering comes from tracking camera (so agent does not run away from screen)
    * v2: All continuous control environments now use mujoco-py >= 1.50
    * v1: max_time_steps raised to 1000 for robot based tasks (including inverted pendulum)
    * v0: Initial versions release (1.0.0)
    """

    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
        ],
        "render_fps": 25,
    }

    def __init__(self, n_teams, n_fights, render_mode: Optional[str] = None):
        self.render_mode = render_mode
        self.action_space = MultiBinary(n_teams)
        observation_space = Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float64)

    def step(self, a):
        reward = 1.0
        self.do_simulation(a, self.frame_skip)
        ob = self._get_obs()
        terminated = bool(not np.isfinite(ob).all() or (np.abs(ob[1]) > 0.2))
        if self.render_mode == "human":
            self.render()
        return ob, reward, terminated, False, {}

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(
            size=self.model.nq, low=-0.01, high=0.01
        )
        qvel = self.init_qvel + self.np_random.uniform(
            size=self.model.nv, low=-0.01, high=0.01
        )
        self.set_state(qpos, qvel)
        return self._get_obs()

    def _get_obs(self):
        return np.concatenate([self.data.qpos, self.data.qvel]).ravel()
