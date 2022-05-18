此项目为本科毕业设计“象棋揭棋玩法中的非对称信息博弈”的代码


环境：
- python3.8 
- CUDA 11.3.1
- cudnn 8.2.1
- tensorflow-gpu 2.7
- keras 2.7
- torch 1.10.2


# 思路
#### 游戏模块：接收决策信息，更新棋盘，发送棋盘

- [ ] 可视化界面

#### AI模块：接收棋盘信息，根据棋盘进行决策，发送决策

- [x] 决策

二者通过socket进行连接

#### 参考文献：
    
- [x] A VIEW ON DEEP REINFORCEMENT LEARNING IN IMPERFECT INFORMATION GAMES 
- [x] Combining Deep Reinforcement Learning and Search for Imperfect-Information Games
- [x] Deep Reinforcement Learning from Self-Play in Imperfect-Information Games
- [x] Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm
- [x] Mastering the game of Go without human knowledge
