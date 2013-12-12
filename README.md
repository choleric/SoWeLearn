SoWeLearn
=========
  
### 目录说明  

#### bin,  
一些部署脚本，暂时未用

#### static  
静态文件存放的目录，包括html, javascript, css, image等不需要python动态解析的东西  

#### mylearn
后端主工程目录。启动后端服务可以用脚本**MYLEARN_MODE=dev python mylearn/manage.py runserver 8080**。  
windows下或IDE下需设置环境变量**MYLEARN_MODE=dev**, 这个变量指明我们的部署的模式是*开发模式(dev)*，相对的*产品模式(production)*。
  
#### mylearn/mylearn/apps  
存放我们的apps，只要用常规的apps创方法创建即可，不需要修改INSTALLED_APPS变量。

#### mylearn/mylearn/dev, mylearn/mylearn/production
分别存放开发模式和产品模式的配置文件：  
1. url配置  
2. log配置  
.......

#### mylearn/mylearn/locale
国际化的文件
