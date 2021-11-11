# wechat_and_fund__for_handsome
handsome微信时光机，搭配每日基金涨跌查询、60s看新闻。python版

[教程](https://www.520315.xyz/archives/492)

# 使用说明
## 1.安装python3相关依赖
所需的第三方库在requirements.txt文件中
或执行命令'pip install -r requirements.txt'

## 2.新建数据库执行db文件夹下的sql文件
新建数据库导入sql文件建立数据表

## 3.修改conf文件夹下Config.json文件
修改为你自己的配置

## 4.启动
执行startWxFund.sh启动文件

''' shell

#启动脚本
./startWxFund.sh

#停止脚本
./stopWxFund.sh

'''

> 注意事项：bind.html文件中绑定网址自行更换，后台端口地址39080，需要可自行修改
