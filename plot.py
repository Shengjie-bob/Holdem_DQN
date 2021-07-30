import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('science')


path ='train_dqn.txt'

record=open(path)

lines = record.readlines()

epochs = []
rewards = []
for line in lines:
    _, epoch,_,reward = line.split()
    epochs.append(epoch)
    rewards.append(reward)

epochs = np.array(epochs).astype(np.float32)
rewards = np.array(rewards).astype(np.float32)


plt.figure(figsize=(6,4),dpi=300)

plt.plot(epochs,rewards)
plt.xlabel('episode')
plt.ylabel('reward')
savepath = path.split('.')[0]+'.png'
plt.savefig(savepath,format='png',dpi=300)
plt.show()


