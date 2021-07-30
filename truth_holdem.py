from RL_brain import DoubleDQN
import numpy as np
import tensorflow as tf
import env_puke_test

#德扑环境
env =env_puke_test.puke()
np.random.seed(1)
#超参数
MEMORY_SIZE = 3000
ACTION_SPACE = 6
OBSERVATION_SPACE=11  #TODO 改为10（包含对手动作）
epochs = 1

#TODO 这里的steps可以改玩几轮
steps = 10

TRAIN = False
TEST = True

#文件保存与加载路径
load_path ='model/natural_DQN.ckpt'


sess = tf.Session()
#两者形式的网络结构
#TODO：MC的更新可能比TD更新更好 需要修正
with tf.variable_scope('Natural_DQN'):
    natural_DQN = DoubleDQN(
        n_actions=ACTION_SPACE, n_features=OBSERVATION_SPACE, memory_size=MEMORY_SIZE,
        e_greedy_increment=0.001, double_q=False, sess=sess
    )

sess.run(tf.global_variables_initializer())


def train(RL):
    if TEST is True:

        RL.load(load_path)
        print('successfull loaded the model!')

    total_steps = 0

    for i_epoch  in range(epochs):
        sum_reward = 0
        for step in range(steps):
            observation = env.reset()
            while True:

                action = RL.choose_action(observation)
                f_action =action
                #更新观测
                observation_, reward, done = env.step(np.array([f_action]))

                print('action : '+str(f_action))

                # reward /= 10     #奖励函数

                sum_reward = sum_reward + reward

                RL.store_transition(observation, action, reward, observation_)

                total_steps = total_steps + 1

                observation = observation_

                if done == True:
                    break
            print('step: '+str(step)+' player1 reward: '+str(reward))

        mean_reward = sum_reward / steps

        print('epoch: ' + str(i_epoch) + ' player1 meanreward: ' + str(mean_reward))


train(natural_DQN)