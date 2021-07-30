# Holdem_DQN
# 蒙特卡洛基础算法程序
* holdem_calc.py 是采用蒙特卡洛算法的主函数程序
* holdem_functions.py holdem_argparser.py 主要含有一些计算胜率和参数传递和读取的函数 function文件计算胜率 argparser文件是参数传递和读取功能（非重点）


# 强化学习算法程序（用于算法的迭代更新）
* RL_brain.py 是强化学习算法DQN的集成类程序
* env_puke.py 是基于gym类的德扑环境程序 配套DQN算法
* run_holdem.py 是强化学习算法DQN的主函数运行程序

# 强化学习算法测试程序（主要作为使用）
* RL_brain.py 是强化学习算法DQN的集成类程序
* env_puke_test.py 是基于gym类的德扑环境程序 配套DQN算法
* test_holdem.py 是强化学习算法DQN的测试主函数运行程序 并非直接运行 仅用于检查结果
* truth_holdem.py 直接运行测试程序



# 运行程序
* python truth_holdem.py 可以直接在终端进行 也可以在python的解释器里运行
* 其中运行后会出现类似如下结果：

```
successfull loaded the model!
['5h', '2s', '3d', '6h'] None
player2 action :
```

* 之后输入我们的动作【action：1：弃牌 2：跟 3：小注 4：中注 5：大注 6：梭哈】后两张牌是我们的牌 前两者为机器人的牌
* 策略网络会给出他的结果 如下所示：

```
successfull loaded the model!
['5h', '2s', '3d', '6h'] None
player2 action : 2
1
action : 4
['5h', '2s', '3d', '6h'] ['4h', '6d', '7h']
player2 action :
```
* 其中action：4代表机器人的动作 ，其动作【action： 0：弃牌 1：跟 2：小注 3：中注 4：大注 5：梭哈】
* 它有时会用比较大的注 因为我为了更好训练 怕他产生一直丢牌的问题 所以没有区分大小注 所以其实主要看他是弃牌还是跟

* 一般来说它的牌比较差 如果你连续跟 他会弃牌 除非他有大A 那样他就会一直跟
* 类似下面的情况

```
['3h', 'Ac', '7s', '8s'] None
player2 action : 2
1
action : 4
['3h', 'Ac', '7s', '8s'] ['9h', 'Ad', '5s']
player2 action : 2
2
action : 5
['3h', 'Ac', '7s', '8s'] ['9h', 'Ad', '5s', '7h']
player2 action : 2
3
action : 4
['3h', 'Ac', '7s', '8s'] ['9h', 'Ad', '5s', '7h', 'As']
player2 action : 2
['3h', 'Ac', '7s', '8s'] ['9h', 'Ad', '5s', '7h', 'As']
Winning Percentages:
(3h, Ac) :  1.0
(7s, 8s) :  0.0
0
action : 2
step: 6 player1 reward: 1
```

# 修改玩几轮
truth_holdem.py文件中15 16行代码为：
# TODO 这里的steps可以改玩几轮
steps = 10

通过修改可以改回合的次数
