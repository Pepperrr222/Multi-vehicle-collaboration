# 自动驾驶多车协作工程 (Raceworld Project)

这是一个基于 ROS Noetic 和 Gazebo 的自动驾驶课程设计项目。项目旨在模拟一个由三辆车组成的团队，在有障碍（坑洞）的道路上协作通行。其中 `car1` 为主车，`car2` 和 `car3` 为辅助车，负责帮 `car1` 过洞。

---

##  功能实现状态 (Feature Status)

- [x] **基本环境搭建**:
  - [x] 创建包含道路、坑洞的Gazebo世界 (`raceworld.world`)
  - [x] 在Launch文件中生成三辆小车和两个坑洞
- [ ] **单车自主巡线 (`car1`)**:
  - [x] 图像处理与车道线检测 (`lane.py`)
  - [ ] 发布稳定的控制指令实现平滑巡线
- [x] **障碍物感知 (`car1`)**:
  - [x] 使用AprilTag作为坑洞的标识
  - [x] 成功检测并识别AprilTag的ID (`tag_detect.py`)
- [ ] **多车协作逻辑**:
  - [ ] **主控制器 (`car1`)**:
    - [ ] 状态机设计（巡线、等待、过坑）
    - [x] 检测到坑后能够停车
    - [x] 发布救援请求
  - [ ] **辅助车控制器 (`car2`, `car3`)**:
    - [ ] 接收救援请求
    - [ ] 路径规划与自主移动到坑洞位置
    - [ ] 到位后发布“准备就绪”信号
- [ ] **完整流程贯通**:
  - [ ] 实现 `car1` -> `car2` -> `car1` -> `car3` -> `car1` 的完整协作流程

---

##  更新日志 (Changelog)

**最新更新: 202X年X月X日**

#### 1. 主要功能实现：
- **实现了基础的坑洞检测功能**：`car1` 现在可以通过摄像头识别到坑洞前方的AprilTag，并在检测到后停车。

#### 2. 文件修改详情：
- **`src/raceworld/src/tag_detect.py`**:
  - **修改**: 重构了代码，将检测器初始化移出回调函数，提升了性能。
  - **新增**: 添加了ROS Publisher，用于发布 `pit_detected` 信号。
- **`src/raceworld/src/lane.py`**:
  - **修改**: 调整了PID参数，使巡线更加平稳。
- **`launch/raceworld_3cars.launch`**:
  - **新增**: 添加了 `tag_detect.py` 节点的启动项。
  - **修改**: 调整了 `car2` 和 `car3` 的初始位置和角度。
- **`README.md`**:
  - **新增**: 添加了“功能实现状态”和“更新日志”部分，方便团队协作。

---

##  环境依赖 (Dependencies)

- **操作系统**: Ubuntu 20.04
- **ROS 版本**: ROS Noetic
- **系统依赖包**:
  ```bash
  sudo apt-get update
  sudo apt-get install ros-noetic-gazebo-ros-control ros-noetic-ackermann-msgs ros-noetic-apriltag-ros
  ```
- **Python 依赖库**:
  ```bash
  pip3 install pyapriltags numpy opencv-python
  ```

---

##  构建与运行

1.  **克隆仓库**:
    ```bash
    git clone https://github.com/Pepperrr222/Multi-vehicle-collaboration.git
    cd Multi-vehicle-collaboration/
    ```

2.  **运行三车协作场景**:
    ```bash
    ./tag_detect.sh
    ```

3.  **（可选）独立启动功能节点进行调试**:
    打开一个新终端 (并 `source devel/setup.bash`)，可运行：
    ```bash
    # 启动键盘控制
    rosrun raceworld key_op.py
    # 启动标签检测
    rosrun raceworld tag_detect.py
    ```
---

##  项目结构

- `src/raceworld/`: 核心 ROS 包。
  - `launch/`: 存放启动不同场景的 `.launch` 文件。
  - `urdf/` & `models/`: 存放机器人和环境的 3D 模型。
  - `src/`: 存放核心功能的 Python 脚本（如 `lane.py`, `tag_detect.py`, `主控制器节点` 等）。
  - `config/`: 存放配置文件。
