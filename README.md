# 微信公众号后台服务
向公众号发送日期信息后返回该日老黄历。支持datetime.dateutil.parser能解析的所有写法，外加“前天”到“后天”的中文。  
![2022.1.1](https://user-images.githubusercontent.com/3489487/148159388-ebc3e9ad-6937-4327-aa75-34fdc08545c9.png)

# 运行环境配置
python3  
图形库 `pip3 install pillow`  
微信接口库 `pip3 install werobot`  ( https://github.com/offu/WeRoBot )  
农历库 `git clone https://github.com/OPN48/pyLunarCalendar.git`  
二维码库 `pip3 install qrcode`  
centOS 8 装中文字体 `yum group install Fonts` 查看已装字体 `fc-list :lang=zh`  
运行 `nohup python3 pubAccountSvc.py &`  
主机设置虚拟内存： https://mp.weixin.qq.com/s/go-xcOJcC0HcPtHDIxoLPA
