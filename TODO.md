## TODO List  
[htmlenti]: http://www.w3schools.com/html/html_entities.asp "HTML Entity Code"
[entitydesign]: ./todo/simple_entity_design.png "Simple Entity Design"
[gravatar]: https://en.gravatar.com/ "Global avatar solution"
[youtubeIssue]: https://github.com/choleric/SoWeLearn/issues/3 "youtube API issues"
  
#### feed  
1. feed信息的来源确定，哪些evet会出现在feed上, 哪些操作会让feed消失
2. feed信息搜索  
3. feed CRUD

#### tutormap
1. model的review(存储int替代string，id关联)
2. view 修改和书写，现在是假数据
3. appointment 设计
4. tutor 翻页实现
  
#### stat
1. student statistics 统计的内容确定  
2. student statistics 后台定时任务  
1. teacher statistics 统计的内容确定  
2. teacher statistics 后台定时任务  

#### topicourse
1. Dicision making：整理需求，确定那些使用第三方app
2. 根据需要修改定义model和前后端接口
3. 创建topicourse的参数和传出的数据,单元测试(status: ongoing, Meichen)
4. 创建topiquiz的参数和传出的数据,单元测试(topiquiz 的抽象处理，允许后台和前端增加不同类型的quiz, 这些quiz有没有可能关联)
5. 用户评论的参数和传出的数据,单元测试
6. 用户观看topicourse的内容存储：model，interface and unittest.
7. 使用Youtube上传视频的参数和传出的数据,单元测试(status: done, Meichen)
8. Youtube API,Youtube政策分析，[youtube API terms][youtubeIssue]
9. 用户观看topiquiz的内容存储：model，interface and unittest.
10. 视频的观看模式方案确定，全屏，黑灯效果，自动拉伸，评论在视频内还是和视频分开
11. 时间表示，根据用户浏览器的时区转换对应的时间

#### user_profile
1. 用户头像(是否存储图片，存储图片的容量和尺寸;不存图片url限制;第三方[gravatar][gravatar])
  
#### auth  
1. 整合allauth基本配置，包括cookie时效和名字的配置，匿名用户登录的配置等(status: done, Meichen)
2. 调整signin的参数和传出的数据,单元测试 (status: done, Xiong)
3. 调整signout的参数和传出的数据,单元测试(status: done, Ray)  
4. 调整signup的参数和传出的数据,单元测试, 包括email的验证流程(status: to be checked, Meichen)
5. 配置allauth的第三方接入的数据，email和本地账户的对接(status: done, Meichen & Xiong)
6. 对每个需要登录的连接加上登录的限制
7. 把个个链接的参数整理成文档(status: ongoing, all)
8. user model根据需求重定义  
9. profile model根据需求定义，并接入allauth系统(status: assigned, Ray)
10. 调整password(change, set, inactive, reset)的参数和传出的数据,单元测试(status: to be verified, Meichen)
  
  
#### 前后端数据交互统一  
1. 前端传入的数据需要进行[html entity code][htmlenti]的转化, 最好可以采用decorator的方式(status:done, Ray)  
2. 统一python端httprespose的应用，可以写一个自己的response来达到统一传出参数格式的目地，具体格式如下(status:done, Ray)  
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
  
#### deploy  
1. nginx 配置文件根据后缀转发，前端需要整理所有资源的后缀或者后端只转发特定url到wsgi  
