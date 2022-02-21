#!/usr/bin/python
# -*- coding: UTF-8 -*-

def htmlPreview( str ):
    "helper to render the input str as HTML in iPython Notebook"
    from IPython.core.display import display, HTML
    display(HTML(str))


list_js_lib = {
    "tree": [
        "https://d3js.org/d3.v5.min.js",
        "https://unpkg.com/@hpcc-js/wasm@0.3.11/dist/index.min.js",
        "https://unpkg.com/d3-graphviz@3.0.5/build/d3-graphviz.js" ]
}

def section_html_header( func_key_list = [""]):
    "decide the js libraries to include based on key:[ libs ] in list_js_lib"
    if type(func_key_list) == str :
        func_key_list = [func_key_list]
    uri_list = []
    for key in func_key_list:
        if key in list_js_lib:
            uri_list += list_js_lib[key]
    return '''
<!DOCTYPE html>
<html>
<header>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3pro.css">
    <link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-indigo.css">
''' + '\n'.join([f'<script src="{uri}"></script>' for uri in uri_list]) + '''
</header>
'''
#print( section_html_header("tree") );


section_header = '''
<body>
    <header class="w3-bar w3-card w3-theme">
        <button class="w3-bar-item w3-button w3-xxxlarge w3-hover-theme" onclick="openSidebar()">&#9776;</button>
        <h1 class="w3-bar-item">定制家谱</h1>
    </header>
    <nav class="w3-sidebar w3-bar-block w3-card" id="mySidebar">
        <div class="w3-container w3-theme-d2">
        <span onclick="closeSidebar()" class="w3-button w3-display-topright w3-large">X</span>
        <br>
        <div class="w3-padding w3-center">
            <img class="w3-circle" src="img_avatar.jpg" alt="avatar" style="width:75%">
        </div>
        </div>
        <a class="w3-bar-item w3-button" href="#">我创建的</a>
        <a class="w3-bar-item w3-button" href="#">我参与的</a>
        <a class="w3-bar-item w3-button" href="#">关于我们</a>
    </nav>
    <script>
        function openSidebar() { document.getElementById("mySidebar").style.display = "block"; }
        function closeSidebar() { document.getElementById("mySidebar").style.display = "none"; }
        closeSidebar();
    </script>
    <a class="w3-button w3-xlarge w3-circle w3-theme-action" style="position:fixed;top:48px;right:24px;">+</a>
'''

section_footer = '''
    <footer class="w3-container w3-theme w3-margin-top">
        <h3>📙 &copy;2022 <a href="https://家谱.top">家谱.top</a></h3>
    </footer>
</body>
</html>'''
#htmlPreview( section_header + section_footer )

def page_mobi_list( itemDict ):
    'return the html page from {"id":("title","desc"), ...}'
    html_list = [f'''
    <hr />
    <div class="w3-cell-row">
        <div class="w3-cell" style="width:30%">
            <img src="{id}.jpg" style="width:100%">
        </div>
        <div class="w3-cell w3-container w3-text-theme">
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
    </div>''' for id,(title,desc) in itemDict.items()]

    return section_html_header() + section_header + '''
    <div class="w3-container">
    ''' + ''.join(html_list) +'</div>'+ section_footer
#test = page_mobi_list( {"id":("title","desc"),"id2":["Hello", "Hello, world!"]})
#print(test)
#htmlPreview( test )

def page_mobi_tree( tree_dict ):
    'return the html page for a family tree'
    return section_html_header("tree") + section_header + '''
    <div id="graph" class="w3-container"></div>

    <script>
    var dotIndex = 0;
    var graphviz = d3.select("#graph").graphviz()
        .transition(function () {
            return d3.transition("main")
                .ease(d3.easeLinear)
                .delay(500)
                .duration(1500);
        })
        .logEvents(true)
        .on("initEnd", render);

    function render() {
        var dotLines = dots[dotIndex];
        var dot = dotLines.join('');
        graphviz
            .renderDot(dot)
    }
    var dots = [
        [
            'digraph  {',
            '    node [style="filled"]',
            '    a [fillcolor="#d62728"]',
            '    b [fillcolor="#1f77b4"]',
            '    a -> b',
            '}'
        ]
    ];
    </script>
    ''' + section_footer
test = page_mobi_tree( {...})
print(test)
#htmlPreview( test )

page_photoEnh = '''
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>生活道与术，照片变魔术</title>
</head>
<body>
  <h1>生活道与术，照片变魔术</h1>
  <h2>用户上传原图：</h2>
    <img src='{uriAppImgEnh}/img/{userId}/{fileName}'></img>
  <h2>人工智能增强后的效果：</h2>
    <img id='myImg'  src='{uriAppImgEnh}/img/busy.gif'></img>
    <p style="color:darkgray">
    <a href='https://mp.weixin.qq.com/s/4ahSuA40t2ZrRh4jPjHfnA'>背景介绍</a><br/>
    图像处理比较费时。具体时长根据图片大小，服务器负载不同差异较大。一般都要几分钟，请耐心等待我们正在不停刷新中。<br/>
    如果需要也可以手动刷新本页面(并不能加速)。 如果真的真的一直刷不出来，有可能是程序出问题了(可怜的小服务器内存不够)可以在公众号对话框给我留言。</p>
    <script>
    img = new Image();
    loadImg = function() {{
        img.src='{uriAppImgEnh}/img/{userId}/{fileName}.jpg'+ '?v=' + Date.now()
    }}
    img.onload = function(){{
        document.getElementById("myImg").src = this.src;
    }};
    img.onerror = function(){{
        setTimeout('loadImg()',15000);
    }};
    loadImg();
    </script>
    <img align='center' src='{uriAppImgEnh}/img/wechatlogo.png'></img>
</body>
</html>'''
#htmlPreview(page_photoEnh)


