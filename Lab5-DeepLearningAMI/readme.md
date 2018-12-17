# 动手实验 5 - 启动深度学习 EC2 环境  

AWS Deep Learning AMI 可以为机器学习从业人员和研究人员提供基础设施和各种工具，从而加快在云中进行任意规模的深度学习的速度。您可以快速启动预先安装了常见深度学习框架 (如 Apache MXNet 和 Gluon、TensorFlow、Microsoft Cognitive Toolkit、Caffe、Caffe2、Theano、Torch、Pytorch、Chainer 和 Keras) 的 Amazon EC2 实例来训练复杂的自定义 AI 模型、实验新算法或学习新的技能和技巧。  
![2](./img/img2.png)
无论您需要 Amazon EC2 GPU 还是 CPU 实例，都无需为 Deep Learning AMI 支付额外费用，您只需为存储和运行应用程序所需的 AWS 资源付费即可。  
  

本实验会指导启动深度学习 EC2，并启动Jupyter Notebook 以供交换分析

## 步骤

1. 启动 EC2  
  
![1](./img/img1.png)
  
2. 选择深度学习镜像  

如果不知道如何选择，可以参考文档[《选择 Deep Learning AMI 》](https://docs.aws.amazon.com/zh_cn/dlami/latest/devguide/options.html)  

![3](./img/img3.png)  


3. 选择实例类型  

如果需要 GPU 可以选择 GPU 实例，如果不需要 GPU，则可以考虑其他的 C 系列或 R 系列实例
![4](./img/img4.png)  

4. 登录  
```
ssh -L localhost:8888:localhost:8888 -i <.pem file name> ec2-user@< instance DNS>
```
pem 文件是 EC2 实例的 Key ，instance DNS 是 EC2 的地址。  
这里使用 8888 端口转发，是为了后面的步骤访问 jupyter notebook  
  
登录后界面  
![5](./img/img5c.png)  

查看 GPU 信息，以及刷新 GPU 占用情况(5秒刷新)
```
nvidia-smi -L
nvidia-smi -l 5
```

5. 启动 Jupyter notebook  
```
nohup jupyter notebook --no-browser &
tail nohup.out
```
  
![6](./img/img6c.png)  

从回显中拷贝 jupyter notebook 的地址，在本地浏览器打开即可访问

6. 访问 Jupyter notebook

![7](./img/img7.png)  

点击 NEW 生成对应的环境，然后你就可以开始做分析了。

7. Explore more ...  
启动 Deep Learning AMI (Amazon Linux) ，并使用 GPU 实例

```
source activate mxnet_p36
cd src
ls
```
查看 GPU 
```
nvidia-smi -L
```
Start Jupyter notebook
```
nohup jupyter notebook --no-browser &
tail nohup.out
```
[Jupyter notebook 文档](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)

尝试 [MNIST 手写识别数据集](http://yann.lecun.com/exdb/mnist/)

## 创建多层神经网络  
在 Jupyter notebook ln 栏运行加载依赖包  
```
# Import dependencies
from __future__ import print_function
import mxnet as mx
import numpy as np
from mxnet import nd, autograd
print("Dependencies imported")
```
使用 GPU 
```
# Use a GPU with MXNet
ctx = mx.gpu()
```
加载 MNIST 数据
```
# Get the MNIST image dataset
mnist = mx.test_utils.get_mnist()
```
定义神经网络参数
```
# Parameters for the neural network
# Number of inputs: A 1-dimensional input consisting of a single image (28 pixels by 28 pixels)
num_inputs = 784
# Number of Outputs: Number of outputs to be predicted by the network (Digits 0-9) 
num_outputs = 10
# Batch size is the number of images processed in a single batch 
batch_size = 64
```
拆分数据为训练集和测试集
```
def transform(data, label):
    return data.astype(np.float32)/255, label.astype(np.float32)
train_data = mx.gluon.data.DataLoader(mx.gluon.data.vision.MNIST(train=True, transform=transform),batch_size, shuffle=True)
test_data = mx.gluon.data.DataLoader(mx.gluon.data.vision.MNIST(train=False, transform=transform),batch_size, shuffle=False)
```
... ...