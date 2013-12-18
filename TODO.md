## TODO List  
[htmlenti]: http://www.w3schools.com/html/html_entities.asp "HTML Entity Code"
[entitydesign]: ./todo/simple_entity_design.png "Simple Entity Design"
  
#### auth  
1. 整合allauth基本配置，包括cookie时效和名字的配置，匿名用户登录的配置等(status: done)
2. 调整signin的参数和传出的数据,单元测试  
3. 调整signout的参数和传出的数据,单元测试  
4. 调整signup的参数和传出的数据,单元测试, 包括email的验证流程－－Meichen  
5. 配置allauth的第三方接入的数据，email和本地账户的对接  
6. 对每个需要登录的连接加上登录的限制
7. 把个个链接的参数整理成文档
8. user model根据需求重定义  
9. profile model根据需求定义，并接入allauth系统
10. 调整password(change, set, inactive, reset)的参数和传出的数据,单元测试  
  
  
#### 前后端数据交互统一  
1. 前端传入的数据需要进行[html entity code][htmlenti]的转化, 最好可以采用decorator的方式  
2. 统一python端httprespose的应用，可以写一个自己的response来达到统一传出参数格式的目地，具体格式如下(status:done, ray)  
3. 整理出个个操作的code值文档
    
##### 传出参数格式
    
    {"c":1, "d": {}}  
  
c是操作的code，表示操作的错误信息，把这些信息定义到一个python的module里，统一管理  
d是个个操作定义的参数，可以不存在
  
  
#### 业务层  
  
##### 实体设计  
首要建立个个实体之间的关系, 以下实体是我暂定，可以根据情况修改:  
![Simple Entity Design][entitydesign]   
这些实体我们可以理解成对应一个model，然后每个model会有自己的function。

##### 业务实现

1. PersonalInfoEdit  
2. PersonalInfo  
3. TeachingInfo  
4. TeachingInfoEdit  
5. LearningInfo  
6. Newsfeed  
7. EventList  
8. TutorProfilePage  
9. ViewRequest&ReplyPage  
10. CreateQuizPageBackbone  
11. CreateTopicoursePageBackbone  
12. CalenderNoSlide  
13. GroupPageBackbone

#### security  
1. csrf  
2. sql injection
