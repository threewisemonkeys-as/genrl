from gym import Wrapper
from abc import ABC, abstractmethod


class BaseWrapper(Wrapper):
    def __init__(self, env, n_envs=None):
        pass

    @property
    def batch_size(self):
        """
        The number of batches trained per update
        """
        return None

    @abstractmethod
    def observation_space(self):
        raise NotImplementedError

    @abstractmethod
    def action_space(self):
        raise NotImplementedError

    #TODO(zeus3101) Add get_state and set_state methods

    @abstractmethod
    def seed(self):
        raise NotImplementedError

    @abstractmethod
    def render(self):
        raise NotImplementedError
    
    @abstractmethod
    def step(self, action):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    def __enter__(self):
        """
        Allows environment to be called using with statement
        """
        return self

    def __exit__(self, exec_type, exec_value, exec_traceback):
        """
        Allows environment to be called using with statement
        """
        self.close()
