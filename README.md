# 微信公众号后台服务
向公众号发送任意信息后返回当日老黄历图片  
![2021 12 30](https://user-images.githubusercontent.com/3489487/147736683-98aeea14-bde5-4201-906f-701eea1ade8e.png)

# 运行环境配置
python3  
图形库 `pip3 install pillow`  
微信接口库 `pip3 install werobot`  ( https://github.com/offu/WeRoBot )  
农历库 `git clone https://github.com/OPN48/pyLunarCalendar.git`  
二维码库 `pip3 install qrcode`  
centOS 8 装中文字体 `yum group install Fonts` 查看 `fc-list :lang=zh`  
运行 `nohup python3 pubAccountSvc.py &`  
