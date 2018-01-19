1. 各种彩票数据爬取,练手
2. 爬取ed2k种子
3. 爬取表情包,兴起
    gif： https://segmentfault.com/q/1010000008651996
    
4. 爬取关系网(qq,weixin,weibo,知乎....)
5. 用户上网数据(qq,weixin,momo...)
6. 爬取用户小号(ip归属地来识别是否是同一人的)
7. 多开小号,伪装点赞,刷帖(水军)/ 某个活动,增大自己的概率
8. 经典的代码片段(code in game,这些网站里面)
9. 美食博,美食的做法
10. 股票,基金,比特币等
11. 返现类似的消息,做返现,推荐
12. 注册邮箱(ZOHO...),并激活邮箱保存到其他介质中
13. 网易邮箱签到活动,添加积分
    网易邮箱俱乐部的签到,需要Login,是一个独立的Login界面, 可以得到请求的link,但是其中的数据不知道是
    怎么处理出来的,在点击登录后. 对登录的信息做了一些混淆处理,加密等操作. 不太好找具体的加密等操作,成本
    也太高.  scrapy.http.FormRequest.from_response 貌似可以处理这样的问题.
    Link: http://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/request-response.html#scrapy.http.FormRequest.from_response
    
    签到地址: http://club.mail.163.com/mission/task/signin.do?from=signinframe&random=0.408874460884626
    (需要保留cookie)
    click btn id :signinstate
    
14. https://segmentfault.com/ 可以尝试注册多个账号
    1. 收取邮件,读取邮件内容,eg: 激活链接
    2. proxy验证,先验证请求已经使用了proxy,不是本机ip了再发出请求
    (proxy的稳定性是一个难题,如何确保稳定的ip代理池)
    3. 如何绕过需要手机号验证的注册过程
    4. +