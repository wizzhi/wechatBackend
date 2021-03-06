# 微信公众号后台服务
向公众号发送日期信息后返回该日老黄历。支持datetime.dateutil.parser能解析的所有写法，外加“前天”到“后天”的中文。  
发送图片的话，会触发AI图像增强功能。谁试谁知道 :)

更多介绍移步微信公众号文章：[万物皆可数字化，老黄历在微信查](https://mp.weixin.qq.com/s?__biz=Mzk0NjEzMzQ5Mw==&mid=2247484190&idx=1&sn=e1611f92031a60676647ef2019012a8a&chksm=c30b8384f47c0a92004440d60b98add39c9f3ab2a2f960c200bb9b4406085f9a57e3126c4be9#rd)

![2022.1.1](https://user-images.githubusercontent.com/3489487/148159388-ebc3e9ad-6937-4327-aa75-34fdc08545c9.png)

# 运行环境配置
### 基本环境
python3  
图形库 `pip3 install pillow`  
微信接口库 `pip3 install werobot`  ( https://github.com/offu/WeRoBot )  
农历库 `git clone https://github.com/OPN48/pyLunarCalendar.git`  
二维码库 `pip3 install qrcode`  
centOS 8 装中文字体 `yum group install Fonts` 查看已装字体 `fc-list :lang=zh`  
运行 `nohup python3 pubAccountSvc.py &`  

### 生产环境用gunicorn 做WSGI服务器
安装 `pip3 install gunicorn`  
运习 `nohup gunicorn pubAccountSvc:app --bind='0.0.0.0:80' &`  
或者 `nohup python3 pubAccountSvc.py &` 都行  

### 如果需要AI图形修复功能还要安装更多库
具体参考：https://github.com/TencentARC/GFPGAN  
pip install basicsr  
pip install facexlib  
pin install torch  
pip install realesrgan  
pip install gfpgan  
...  

外加模型下载：  
./model/downloadModels.sh  

AI很吃内存，主机设置虚拟内存：https://mp.weixin.qq.com/s/go-xcOJcC0HcPtHDIxoLPA  
