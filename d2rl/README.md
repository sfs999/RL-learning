# Hands-on RL 强化学习教程

本目录包含《Hands-on RL》强化学习教程的完整资源。

## 📚 资源内容

### 1. GitHub 仓库代码 (Hands-on-RL/)

完整的强化学习算法实现代码，包含 21 个章节的 Jupyter Notebook：

**基础部分：**
- 第 2 章 - 多臂老虎机问题
- 第 3 章 - 马尔可夫决策过程
- 第 4 章 - 动态规划算法
- 第 5 章 - 时序差分算法
- 第 6 章 - Dyna-Q 算法

**深度强化学习：**
- 第 7 章 - DQN 算法
- 第 8 章 - DQN 改进算法
- 第 9 章 - 策略梯度算法
- 第 10 章 - Actor-Critic 算法
- 第 11 章 - TRPO 算法
- 第 12 章 - PPO 算法

**高级算法：**
- 第 13 章 - DDPG 算法
- 第 14 章 - SAC 算法
- 第 15 章 - 模仿学习
- 第 16 章 - 模型预测控制
- 第 17 章 - 基于模型的策略优化
- 第 18 章 - 离线强化学习
- 第 19 章 - 目标导向的强化学习
- 第 20 章 - 多智能体强化学习入门
- 第 21 章 - 多智能体强化学习进阶

**工具文件：**
- `rl_utils.py` - 强化学习通用工具函数

### 2. 网页版书籍内容 (book-content/)

从 https://hrl.boyuai.com 下载的网页版教材 HTML 文件，包含：

- 第 1 章 - 强化学习简介
- 第 2 章 - 多臂赌博机
- 第 3 章 - 马尔可夫决策过程
- 第 4 章 - 动态规划
- 第 5 章 - 蒙特卡洛方法
- 第 6 章 - 时序差分方法
- 第 7 章 - 价值函数近似
- 第 8 章 - 策略梯度方法
- 第 9 章 - 高级主题

## 🔧 使用说明

### 运行环境配置

```bash
# 安装必要的 Python 库
pip install numpy matplotlib torch gymnasium
```

### 运行 Notebook

使用 Jupyter Notebook 或 JupyterLab 打开任意章节：

```bash
jupyter notebook 第 2 章 - 多臂老虎机问题.ipynb
```

### 查看网页版教材

直接用浏览器打开 `book-content/` 目录中的 HTML 文件即可查看对应的理论讲解。

## 📖 学习建议

1. **理论与实践结合**：先阅读网页版教材的理论部分（book-content/），再运行对应的代码实现（Hands-on-RL/）
2. **循序渐进**：按照章节顺序学习，从基础概念到高级算法
3. **动手实验**：修改和运行 Notebook 中的代码，观察不同参数的效果
4. **完成练习**：每章结束后尝试自己实现变体算法

## 🌐 原始资源

- **GitHub 仓库**: https://github.com/boyu-ai/Hands-on-RL
- **在线书籍**: https://hrl.boyuai.com/chapter/intro

## 📝 许可证

本资源遵循原项目的开源许可证（MIT License）

---

**下载日期**: 2026 年 3 月 9 日  
**下载工具**: download_book.py
