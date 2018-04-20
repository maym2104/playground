from . import BaseAgent
from .. import constants


class VerySimpleAgent(BaseAgent):
    """The Random Agent that returns random actions given an action_space."""
    def act(self, obs, action_space):
        return constants.Action.Stop.value