# edge
1. 构造函数无要求
2. 主要函数为check，传入参数： 图片， 返回边缘信息

# objectDetect

1. 构造函数需传入 需要检测目标的图片信息，数据格式为numpy array
2. 主要功能为detect, 其中输入参数为边缘信息，以及输入图像本身,数据格式为numpy array，返回矩形框四个顶点

# orbSlam

1. 构造函数无要求
2. 首先要使用setInitNode定义初始位置
3. receieveImg 接受图片，并且为图中添加相应的约束
4. addRobotNode 为添加一个机器人的状态结点，接受的参数为{'x': 1, 'y':2},字典形式,可以通过getConstrain函数输入x和y快捷获得
5. reconstrcutGraph 全局重解获取位置信息
6. solveIncGraph 局部增量重解获取位置信息
7. 注意一定要先添加机器人状态再接受图片设置约束，不然会出问题。