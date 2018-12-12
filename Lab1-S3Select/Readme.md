# 动手实验1 - S3 Select

## 前置准备
1. 本机安装 Python3

2. 本机安装 boto3，参考命令

    pip3 install boto3 --user

3. 本地进行 AWS Credentials 配置

    aws configure

配置可以访问 AWS 的 access key，如果之前使用过命令行则重用CLI的配置即可。

4. 下载以下2个样例数据文件，并上传到你账户的 S3 某个 Bucket 中

    [pagecounts-20100212-050000.gz](./sample-data/pagecounts-20100212-050000.gz)
    [users-data.json](./sample-data/users-data.json)

## 在控制台进行 S3 Select

1. 打开 S3 控制台，选择刚才上传的 pagecounts-20100212-050000.gz ，点选“选择范围”页面
![在控制台进行S3 Select](./img/img1.png)

2. Console 分析 CSV 数据
对 pagecount 数据样例进行 S3 Select 尝试：
![下一步](./img/img2.png)
![SQL](./img/img3.png)

    select count(*) from s3object s

    select * from  s3object s limit 10

    select s._1,s._4 from s3object s where s._4='377' limit 10

参考示例，做更多 S3 命令尝试
![示例](./img/img4.png)

尝试其他更多的命令，参考：S3 SELECT command SQL
https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference-select.html

3. Console 分析 JSON 数据
对 users-data.json 进行 S3 Select:

    select s.userid, s.username, s.phone from s3object as s where s.userid = 7

## 使用 Python 程序调用 S3 Select

下载样例 [S3SelectDemo-csv.py](./S3SelectDemo-csv.py) 

替换代码中的<bucket>和<s3 bucket prefix> 为上传的 pagecount 文件所在位置 

在本地运行

    python3 S3SelectDemo-csv.py

分析并尝试 获取S3 Select 还有哪些选项，S3 SELECT boto3 refer to:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.select_object_content

观察 Python 代码如何获取 Select 结果的，
Response of PayLoad is botocore.eventstream.EventStream Object, refer to:
https://botocore.amazonaws.com/v1/documentation/api/latest/reference/eventstream.html#botocore-eventstream