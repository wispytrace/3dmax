# commonMessage
1. 介绍：一些通用的格式信息，比如服务类型、状态类型、命令信息
2. 服务端(slam执行处)发送的信息：服务类型，执行状态，数据（字符串格式)
3. 客户端(被控机器人移动处)发送的信息，服务类型、命令、数据(字符串格式)

# slamData
1. 处理slam客户都服务发送数据所需要封装成的数据格式， 目前只有一个img，负责将img从字符解码出来

# slamRes
1. 处理slam服务端发送数据所需封装的数据格式