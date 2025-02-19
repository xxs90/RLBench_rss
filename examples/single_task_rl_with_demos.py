import numpy as np

from rlbench.action_modes.action_mode import MoveArmThenGripper
from rlbench.action_modes.arm_action_modes import JointVelocity
from rlbench.action_modes.gripper_action_modes import Discrete
from rlbench.environment import Environment
from rlbench.observation_config import ObservationConfig
from rlbench.tasks import LampOn as tks


class Agent(object):

    def __init__(self, action_shape):
        self.action_shape = action_shape

    def ingest(self, demos):
        pass

    def act(self, obs):
        arm = np.random.normal(0.0, 0.1, size=(self.action_shape[0] - 1,))
        gripper = [1.0]  # Always open
        return np.concatenate([arm, gripper], axis=-1)


# To use 'saved' demos, set the path below, and set live_demos=False
live_demos = True
DATASET = '' if live_demos else 'PATH/TO/YOUR/DATASET'

obs_config = ObservationConfig()
obs_config.set_all(True)

action_mode = MoveArmThenGripper(
    arm_action_mode=JointVelocity(), gripper_action_mode=Discrete())
env = Environment(
    action_mode, DATASET, obs_config, False)
env.launch()

task = env.get_task(tks)
demos = task.get_demos(2, live_demos=live_demos)

agent = Agent(env.action_shape)
agent.ingest(demos)

training_steps = 1000
episode_length = 50
obs = None
for i in range(training_steps):
    if i % episode_length == 0:
        print('Reset Episode')
        descriptions, obs = task.reset()
        print(descriptions)
    action = agent.act(obs)
    print(action)
    obs, reward, terminate = task.step(action)
    print(reward, terminate)

print('Done')
env.shutdown()
