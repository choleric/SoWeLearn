SoWeLearn
=========
[logd]: https://docs.djangoproject.com/en/dev/topics/logging/ "Django Logging"
[logp]: http://docs.python.org/2/howto/logging.html "Python Logging"
[codestyle]: http://www.python.org/dev/peps/pep-0008/ "Python Code Style"

  
### TIPS  
  
#### git  
git是分布式的版本管理工具，所以有远程repo和本地repo的概念。*git push*和*git pull*是远程相关的操作, 建议只在本地开发测试完成后进行使用。而其他的操作只影响你本地的代码，所以可以为所欲为。  
##### branch
我们可以使用如下命令在本地新建一个local_master的分支， 并让它和远程分支同步（也就是说pull和push会自动同步两个分支）:  

    git branch -t local_master origin/newproj

##### checkout and status  
记得要经常看下自己所在的branch是不是自己认为的哦
##### commit  
推荐用如下的流程commit代码：  

    git status  
    git add xxx  
    git commit -m "commit log"  

这样是防止*git commit -am "commit log"*将所有不必要的问题，提交到repo里去  
##### push  
每次push之间记得要pull以下代码哦
  
#### code with log  
后端想要*print xxx*的时候千万别print, 而是用如下的代码：  

    import logging
    log = logging.getLogger(__name__)  
    log.error("This is a print with name %s", "print No.1")

这是利用了python的日志模块，方便我们统一管理日志。具体可以参考连接：[python log][logp]和[django log][logd]
  
#### python code style
规范编码风格，让代码merge的时候难度降低，也让可读性更好。我们可以采用python推荐的[code style][codestyle]。  
尽量遵守，有些不适应的地方可以忽略。
  
### URL  
我们现在的工程采用了前后端分离的模式，也就是说我们会有一个web server（nginx）根据url不同转发请求。所以我们会把url分成如下几类：  
1. http://www.domain.com/html/xxx, html的请求  
2. http://www.domain.com/js/xxx, js的请求  
3. http://www.domain.com/css/xxx, css的请求  
4. http://www.domain.com/images/xxx, image的请求  
5. 而其他的请求会转发给cgi，最终给django处理    

  
### 目录说明  

#### bin,  
一些部署脚本，暂时未用

#### static  
静态文件存放的目录，包括html, javascript, css, image等不需要python动态解析的东西  

#### mylearn
后端主工程目录。启动后端服务可以用命令:

    MYLEARN_MODE=dev python mylearn/manage.py runserver 8080  

windows下或IDE下需设置环境变量  

    MYLEARN_MODE=dev  

这个变量指明我们的部署的模式是*开发模式(dev)*，相对的*产品模式(production)*。
  
#### mylearn/mylearn/apps  
存放我们的apps，只要用常规的apps创方法创建即可，不需要修改INSTALLED_APPS变量。

#### mylearn/mylearn/dev, mylearn/mylearn/production
分别存放开发模式和产品模式的配置文件：  
1. url配置  
2. log配置  
.......

#### mylearn/mylearn/locale
国际化的文件
