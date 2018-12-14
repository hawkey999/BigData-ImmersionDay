# 动手实验3 EMR - 托管的 Hadoop
目的：操作创建一个EMR集群，并且使用Hive和Spark，建外表对S3中的数据进行分析

## EMR对S3数据源直接分析的优势
* 分钟级部署   
* 弹性动态扩/缩集群计算节点   
* 按使用付费，支持低价时段自动计算最大可节省90%成本  
  
把数据放在S3数据湖而不是HDFS:     
* 统一数据源 
* S3 高持久性的数据存储 
* 不用担心HDFS节点丢失 
* 不用担心去扩增 HDFS节点, S3 具有高扩展性 (IOPS, 容量)

![s3 data lake](./img/s3-datalake.png)  

## 前置知识
确认您已具备以下基本操作知识：
* VPC、子网、安全组的创建
* EC2的创建，以及使用Key pair进行SSH登录
* 对S3有了解

## 创建EMR集群
  
1. 在EMR控制台点创建
![1](./img/Picture1.png)  
选择高级选项  
![2](./img/Picture2.png)  
选择自动安装的模块  
![3](./img/Picture3.png)  
  
2. 配置硬件  
![4](./img/Picture4.png)  
强烈建议不要把EMR直接暴露在公网，应该配置在私有子网，使用跳板机去访问  
建议配置S3终端节点，从VPC内部直接访问S3，无需绕道公网  
  
三种节点说明：  
* 主节点 (Master Node): 主节点管理群集，通常运行分布式应用程序的Master组件。例如，YARN  ResourceManager, HDFS NameNode.  
* 核心节点(Core Node): 核心节点运行HDFS DataNode. 同时还运行任务跟踪守护程序，并对安装的应用程  序执行其并行计算任务。例如，运行 YARN NodeManager 守护程序、Hadoop MapReduce 任务和 Spark  执行器。  
* 任务节点(Task Node): 任务节点是可选的，可以使用任务节点来支持对数据执行并行计算任务，例如  Hadoop MapReduce 任务和 Spark 执行程序。任务节点不运行HDFS 的DataNode守护程序，也不在  HDFS 中存储数据。  
  
3. 一般选项
![5](./img/Picture5.png)   
  
4. 集群安全选项
![6](./img/Picture6.png)   
需要设置一个访问EC2的key
  
5. 完成  
等待集群启动，并观察摘要、监控、硬件、事件、步骤等选项

## 