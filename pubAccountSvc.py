#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import textwrap
from io import BytesIO, BufferedReader
from PIL import Image, ImageDraw, ImageFont

import sys
sys.path.append("/xxxxx/pyLunarCalendar")
import lunar
import qrcode
import werobot
from werobot.replies import ImageReply

robot = werobot.WeRoBot(token='xxxxx')
robot.config["APP_ID"]="xxxxx"
robot.config["APP_SECRET"]="xxxxx"
#robot.logger.setLevel('DEBUG')
client=robot.client

# 当日节气或者下一个节气
def jieqi( l ):
    if l.todaySolarTerms and l.todaySolarTerms != '无':
        return "今日" + l.todaySolarTerms
    nextDate = datetime.datetime(l.nextSolarTermYear, l.nextSolarTermDate[0], l.nextSolarTermDate[1])
    delta = nextDate - l.date
    if delta.days == 1:
        return "明日" + l.nextSolarTerm
    if delta.days == 2:
        return "后天" + l.nextSolarTerm
    nextLunar = lunar.Lunar( nextDate )
    return  nextLunar.lunarDayCn + l.nextSolarTerm


# 按字数折行，为塞进两边的框。最多取10行，太多写不下
def wrap2sideBox( txt ):
    txtLines = textwrap.wrap(txt, width=11)
    return '\n'.join(txtLines[0:10])

# 按字数折行，针对下部中间的那堆小字
def pushLine( mylist, txt ):
    txtLines = textwrap.wrap(txt, width=25)
    mylist += txtLines

# 渐变填充背景
def gradientFill(img,c1,c2):
    (w,h) = img.size
    d = ImageDraw.Draw(img)
    stepR = (c2[0]-c1[0])/h
    stepG = (c2[1]-c1[1])/h
    stepB = (c2[2]-c1[2])/h
    for y in range(0,h):
        bgR = round(c1[0]+ stepR*y)
        bgG = round(c1[1]+ stepG*y)
        bgB = round(c1[2]+ stepB*y)
        for x in range(0,w):
            d.point((x,y),fill=(bgR,bgG,bgB))

# 添加二维码
def addQR(img, positionXY, color_front, color_back ):
    qr = qrcode.QRCode(box_size=2,border=0)
    qr.add_data('http://weixin.qq.com/r/IxDr8_-EirL1rauQ90Ux')
    qr.make()
    qr_img = qr.make_image(fill_color=color_front, back_color=color_back)
    img.paste(qr_img,positionXY)

# 生成整个图片
def imgGen( d ):
    (imgW,imgH)=(600,600)
    (boxW,boxH) = (130,200)
    boxSpacing = 20
    fontname1 = 'NotoSansCJK-Medium.ttc'
    row1 = 30
    row2 = 130
    row3 = 240
    row4 = row3+35
    row5 = 310
    row6 = 390
    colorBGtop = (200,245,246)
    colorBG = (255,250,240)
    color1 = (0,64,0)
    colorGood = (102,0,0)
    colorBad = (64,64,64)
    font1 = ImageFont.truetype( fontname1, size=45)
    font2 = ImageFont.truetype( fontname1, size=35)
    font3 = ImageFont.truetype( fontname1, size=200)
    font4 = ImageFont.truetype( fontname1, size=50)
    font5 = ImageFont.truetype( fontname1, size=22)
    font6 = ImageFont.truetype( fontname1, size=8)
    font7 = ImageFont.truetype( fontname1, size=25)
    #font7.set_variation_by_name('Bold')
    font8 = ImageFont.truetype( fontname1, size=12)

    a = lunar.Lunar(d)
    img =  Image.new( mode = "RGB", size = (imgW, imgH), color = colorBG )
    gradientFill(img, colorBGtop, colorBG)
    addQR(img, (507,57),color1, colorBGtop )
    draw = ImageDraw.Draw(img)
    draw.text((imgW-60, row2), "微信扫码畅查", fill=colorBad, anchor="mm", font=font8)

    draw.text((imgW/2, row1), "老黄历", fill=color1, anchor="mm", font=font1)
    draw.text((imgW/5, row1), str(d.year) + "年"  , fill=color1, anchor="mm", font=font2)
    draw.text((imgW*4/5, row1), str(d.month) +"月 "+d.strftime("%b").upper() , fill=color1, anchor="mm", font=font2)
    draw.text((imgW/2, row2), str(d.day)  , fill=color1, anchor="mm", font=font3)

    draw.text((imgW/4, row3), a.lunarDayCn + "日" , fill=color1, anchor="mm", font=font4)
    draw.text((imgW*3/4, row3), a.weekDayCn  , fill=color1, anchor="mm", font=font4)
    draw.text((imgW/4, row4), '%s(%s)年%s' % ( a.year8Char, a.chineseYearZodiac, a.lunarMonthCn) +('(闰)' if a.isLunarLeapMonth else '')  , fill=color1, anchor="mm", font=font5)
    draw.text((imgW*3/4, row4), d.strftime("%A").upper()  , fill=color1, anchor="mm", font=font5)
    draw.text((imgW/2, row3+10), jieqi(a), fill=color1, anchor="mm", font=font5)

    draw.text((imgW/2-160, row5+3), '时辰', fill=color1, anchor="mm", font=font7)
    draw.text((imgW/2-160, row5+30), '吉凶', fill=color1, anchor="mm", font=font7)
    draw.text((imgW/2 + 30, row5), ' '.join(lunar.the12EarthlyBranches), fill=color1, anchor="mm", font=font5)
    draw.text((imgW/2 + 30, row5+16), '23-01  01-03  03-05  05-07  07-09  09-11  11-13  13-15  15-17  17-19  19-21  21-23', fill=color1, anchor="mm", font=font6)
    draw.text((imgW/2 + 30, row5+30), ' '.join(a.get_twohourLuckyList()[:12]), fill=color1, anchor="mm", font=font5)

    draw.rectangle([boxSpacing,row6-20,boxW+boxSpacing,row6+20],colorGood,colorGood)
    draw.rectangle([boxSpacing,row6+20,boxW+boxSpacing,row6+boxH],colorBG,colorGood)
    draw.text((boxSpacing + boxW/2, row6), '宜', fill=colorBG, anchor="mm", font=font2)
    draw.text((boxSpacing + boxW/2, row6+boxH/2+10), wrap2sideBox( ' '.join(a.goodThing)), fill=colorGood, anchor="mm", font=font8)

    draw.rectangle([imgW-boxSpacing-boxW,row6-20,imgW-boxSpacing,row6+20],colorBad,colorBad)
    draw.rectangle([imgW-boxSpacing-boxW,row6+20,imgW-boxSpacing,row6+boxH],colorBG,colorBad)
    draw.text((imgW-boxSpacing-boxW/2, row6), '忌', fill=colorBG, anchor="mm", font=font2)
    draw.text((imgW-boxSpacing-boxW/2, row6+boxH/2+10), wrap2sideBox(' '.join(a.badThing)), fill=colorBad, anchor="mm", font=font8)

    misc = []
    holiday = list(filter(str.strip, [a.get_legalHolidays(),a.get_otherHolidays(), a.get_otherLunarHolidays()]))
    if len(holiday) > 0 :
        pushLine(misc, '【今日节日】' + ' '.join(holiday))
    pushLine(misc, '【生肖冲煞】' + a.chineseZodiacClash)
    pushLine(misc, '【星座】' + a.starZodiac + ' 【星次】' + a.todayEastZodiac)
    pushLine(misc, '【十二神】' + ' '.join(a.get_today12DayOfficer()))
    pushLine(misc, '【廿八宿】' + a.get_the28Stars() + ' 【纳音】' + a.get_nayin())
    pushLine(misc, '【三合】' + ' '.join(a.zodiacMark3List) + ' 【六合】' + ' '.join(a.zodiacMark6) )
    pushLine(misc, '【彭祖百忌】' + a.get_pengTaboo(long=4, delimit=','))
    pushLine(misc, '【今日胎神】' + a.get_fetalGod())
    pushLine(misc, '【今日吉神】' + ' '.join(a.goodGodName))
    pushLine(misc, '【今日凶煞】' + ' '.join(a.badGodName))
    pushLine(misc, '【九宫飞星】' + a.get_the9FlyStar())
    pushLine(misc, '【吉神方位】' + ' '.join(a.get_luckyGodsDirection()))
    draw.text((imgW/2, row6+boxH/2-10), '\n'.join(misc[0:13]), fill=color1, anchor="mm", font=font8)
    
    now = datetime.datetime.now()
    draw.text((imgW, imgH), now.strftime("%Y年%m月%d日 %H:%M:%S 敬制 "), fill=colorBad, anchor="rs", font=font6)
    return img

# 上传图片到微信后台
def uploadImg(img):
    buf = BytesIO()
    #img.save("rand.png")
    img.save(buf, format='PNG')
    buf.seek(0)
    buf.name = 'rand.png'
    json = client.upload_media("image", BufferedReader( buf ) )
    mid = json["media_id"]
    return mid

@robot.handler
def onMsg(message):
    wantedDate = parseDate( message.content )
    if wantedDate :
        img =  imgGen( wantedDate )
        m_id = uploadImg( img )
        return ImageReply(message=message, media_id=m_id)
    else :
        return helpText

@robot.subscribe
def onSub( message ):
    return helpText

from dateutil import parser
from datetime import timedelta
def parseDate( txt ):
    try:
        return parser.parse( txt )
    except:
        pass
    if "今天" in txt :
        delta = 0
    elif "明天" in txt :
        delta = 1
    elif "后天" in txt :
        delta = 2
    elif "昨天" in txt :
        delta = -1
    elif "前天" in txt :
        delta = -2
    else :
        return False
    return datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=delta)

helpText = "我现在除了做日历啥也不会，可以把需要的日期发我。\n\n比如:\n2021.12.30、12/30、明天..."

# 让服务器监听在 0.0.0.0:80
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
