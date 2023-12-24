# Core Library
import logging

# Third party
from gymnasium.envs.registration import register

logger = logging.getLogger(__name__)

register(id="BracketGen-v1", entry_point="gym_bracket_gen.envs:MountainCarEnv")