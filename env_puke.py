import numpy as np
import holdem_calc
np.random.seed(1)

class puke():
    def __init__(self):
        #TODO：未来给动作加个字典 这样更为明确的知道最后的结果
        self.action_space = [0, 1, 2, 3, 4, 5] # action 0：弃牌 1：跟 2：小注 3：中注 4：大注 5：梭哈
        #玩家2的动作空间
        self.p2_action_space = [1, 2, 3, 4, 5, 6]  # action 1：弃牌 2：跟 3：小注 4：中注 5：大注 6：梭哈

        self.n_actions = len(self.action_space)
        # self.observation = np.zeros([7])
        #TODO:加入对手动作的观测量
        self.observation=np.zeros([11])

        self.non_observation =np.zeros([2])
        self.all_puke = np.arange(52)+1           #需要改成1到53张牌
        np.random.shuffle(self.all_puke)
        self.sp=0
        self.done =False
    #回合结束重置
    def reset(self):
        self.done=False
        self.all_puke = np.arange(52)+1           #需要改成1到53张牌 已解决
        np.random.shuffle(self.all_puke)

        # self.observation[:5] = self.chouka(5)[::np.newaxis]   #中间需要做个筛选器 去掉相同的 已解决
        # self.update(2)

        #TODO：改动
        self.observation[:2] = self.chouka(2)[::np.newaxis]
        self.update(2)
        #

        self.non_observation[:2]= self.chouka(2)
        self.update(2)
        return self.observation
    #每步观测
    def step(self,action):
        self.sp += 1
        p2_action = self.p2_step()
        #TODO:改动第一步 先考虑自己先手
        if self.sp ==1:
            if action == 0:
                self.reward =-0.1  #仅损失本金 -1的奖励有点大  TODO：未来加入更为合理的奖励
                self.new_game()
            elif p2_action >1:
                self.observation[2:5]=self.chouka(3)
                self.update(3)
                self.reward =0
            else:
                self.reward = 0.1
                self.new_game()

        elif self.sp <=3 :
            if action == 0:
                self.reward = -0.1  #仅损失本金 -1的奖励有点大  TODO：未来加入更为合理的奖励
                self.new_game()
            elif p2_action >1:
                #注意此处的观测量
                self.observation[3+self.sp]=self.chouka(1)
                self.update(1)
                self.reward =0
            else:
                self.reward =0.1
                self.new_game()
        else:
            if action ==0:
                self.reward = -0.1
                self.new_game()
            elif p2_action >1:
                a =self.win_check()
                if a >0:
                    self.reward = 1
                else:
                    self.reward = -1
                self.new_game()
            else:
                self.reward = 1
                self.new_game()
        print(self.sp)
        return self.observation , self.reward, self.done

    #发牌
    def chouka(self,number):
        # np.random.shuffle(self.all_puke)
        return self.all_puke[:number]
    #更新剩余扑克
    def update(self,number):
        num =np.arange(number)
        # print(self.all_puke)
        self.all_puke =np.delete(self.all_puke,num)
        # print(self.all_puke)
    #新的一轮发牌
    def new_game(self):
        # self.observation = np.zeros([7])

        #TODO:改动
        self.observation = np.zeros([11])

        self.non_observation =np.zeros([2])
        # self.all_puke = np.arange(52)+1
        # np.random.shuffle(self.all_puke)
        self.sp =0
        self.done =True

    #验证动作后卡牌是否获得胜利 
    def win_check(self):
        array1 = self.observation[:2]
        array2 = self.non_observation
        array3 = self.observation[2:7]  #由于变化所以此处的观测量为10个 TODO：
        array1_2 =np.hstack([array1,array2])
        cards =[]
        boards =[]
        suited_card_dic ={0:'s',1:'c',2:'h',3 :'d'}
        card_dic ={1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'T',11:'J',12:'Q',0:'K'}   #10如果单独出现会出现位数增加的问题 但结合“T”完美解决位数问题
        for i in array1_2:
            card_num =card_dic[(i-1)%13]
            card_type =suited_card_dic[np.floor((i-1)/13)]
            card =card_num+card_type
            cards.append(card)
        for l in array3:
            board_num =card_dic[(l-1)%13]
            board_type =suited_card_dic[np.floor((l-1)/13)]
            board =board_num+board_type
            boards.append(board)
        print(cards,boards)
        percentage = holdem_calc.main(cards,boards)

        if percentage[1]>percentage[2]:
            a=1
        else:
            a=0
        return a

    def p2_step(self):
        array1 = self.observation[:2]
        array2 = self.non_observation
        array3 = self.observation[2:7]
        array1_2 =np.hstack([array1,array2])
        cards =[]
        boards =[]
        suited_card_dic ={0:'s',1:'c',2:'h',3 :'d'}
        card_dic ={1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'T',11:'J',12:'Q',0:'K'}   #10如果单独出现会出现位数增加的问题 但结合“T”完美解决位数问题
        for i in array1_2:
            card_num =card_dic[(i-1)%13]
            card_type =suited_card_dic[np.floor((i-1)/13)]
            card =card_num+card_type
            cards.append(card)
        #判断是否存在桌面牌
        for l in array3:
            if l==0:
                continue
            else:
                board_num =card_dic[(l-1)%13]
                board_type =suited_card_dic[np.floor((l-1)/13)]
                board =board_num+board_type
                boards.append(board)

        if len(boards):
            pass
        else:
            boards =None
        print(cards, boards)
        percentage = holdem_calc.main(cards,boards)

        # 玩家2是否比玩家1手牌好
        if percentage[2]-percentage[1] < 0:
            p2_action = self.p2_action_space[0]
        elif (percentage[2]-percentage[1]) / (percentage[2]+1e-4)<0.2:
            p2_action =self.p2_action_space[1]
        elif (percentage[2] - percentage[1]) / (percentage[2]+1e-4) < 0.4:
            p2_action = self.p2_action_space[2]
        elif (percentage[2] - percentage[1]) / (percentage[2]+1e-4) < 0.5:
            p2_action = self.p2_action_space[3]
        elif (percentage[2] - percentage[1]) / (percentage[2]+1e-4) < 0.8:
            p2_action = self.p2_action_space[4]
        else:
            p2_action = self.p2_action_space[5]

        self.observation[6+self.sp] =p2_action

        return p2_action
