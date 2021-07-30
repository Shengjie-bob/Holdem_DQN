import gym
from RL_brain import DoubleDQN
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import env_puke

#德扑环境
env =env_puke.puke()
np.random.seed(1)
#超参数
MEMORY_SIZE = 3000
ACTION_SPACE = 6
OBSERVATION_SPACE=11  #TODO 改为10（包含对手动作）
epochs = 100
steps = 200
TRAIN = True
TEST = False

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

with tf.variable_scope('Double_DQN'):
    double_DQN = DoubleDQN(
        n_actions=ACTION_SPACE, n_features=OBSERVATION_SPACE, memory_size=MEMORY_SIZE,
        e_greedy_increment=0.001, double_q=True, sess=sess, output_graph=True)


sess.run(tf.global_variables_initializer())



f = open('train_dqn.txt','w+')


def train(RL):
    if TEST is True:
        RL.load(load_path)

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

                # reward /= 10     #奖励函数

                sum_reward = sum_reward + reward

                RL.store_transition(observation, action, reward, observation_)

                total_steps = total_steps + 1

                if total_steps > MEMORY_SIZE:   # 学习
                    RL.learn()

                observation = observation_

                if done == True:
                    break
            print('step: '+str(step)+' reward: '+str(reward))

        mean_reward = sum_reward / steps

        print('epoch: ' + str(i_epoch) + ' meanreward: ' + str(mean_reward))

        f.write('Ep: ' +str(i_epoch)+
          " Ep_r: " +str(mean_reward)+'\n')

        # 保存模型
        if i_epoch == epochs-1:
            RL.save(load_path)
            f.close()

    return RL.q


q_natural = train(natural_DQN)
#q_double = train(double_DQN)

plt.plot(np.array(q_natural), c='r', label='natural')
#plt.plot(np.array(q_double), c='b', label='double')
plt.legend(loc='best')
plt.ylabel('Q eval')
plt.xlabel('training steps')
plt.grid()
plt.savefig('training.png',dpi=300)
