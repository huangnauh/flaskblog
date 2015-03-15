##介绍

### flaskblog.py
使用sqlite3来保存博客


###flaskblog1.py
使用Stormpath账户登入，保存博客

[将用户管理和认证外包给Stormpath](http://www.infoq.com/cn/news/2013/07/Stormpath)

pip install flask-stormpath

1. 创建Stormpath账户:https://api.stormpath.com/register
2. 创建API 密钥:https://api.stormpath.com/ui/dashboard
3. 下载文件apiKey.properties
4. 创建Stormpath应用，https://api.stormpath.com/v#!applications?。创建一个名为flaskblog的新应用。
5. 访问https://api.stormpath.com/ui/accounts/create? ，在flaskblog Directory创建新用户账户。所有在这儿创建的账户都可以用来登入你将搭建的微博客。
