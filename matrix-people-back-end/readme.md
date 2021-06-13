## 前言

关键词：图数据库、NoSQL、neo4j、非关系型数据库、

经过半个月的业余开发，基于NoSQL（非关系型数据库）的可视化人脉图谱项目终于上线与大家见面了~虽然目前完善的功能较为简单，不过这套框架的可扩展性较强，且使用较为大众的web框架Springboot+Vue.js开发，只要开发者能想得到适合的领域，这套框架就能最大程度的兼容与适配，比如为历史中的人物添加关系方便记忆，比如管理平台中用户的关注关系以整合资源，比如理清书籍、游戏、影视作品中的人物关系，比如结构深度学习中多维的神经网络……希望该项目能够成为推动HelpDesk、数据可视化、数据看板等IT基础能力持续降低上手门槛的起点。

## 简单介绍

在开始详细介绍之前，先以视频的形式给大家快速展示下我们框架的功能：

视频链接：[NoSQL可视化人脉图谱实战教程](https://www.bilibili.com/video/BV1MA411L7DY)
 
目前我们仅基于自己的业务做了最基本的功能展示，实际上该组件的可扩展性还是很广的，例如改变节点属性、改变连接属性，且无论是节点还是边甚至可以设为多种……Nosql作为更符合人脑记忆的数据展现形式，在未来理论会成为应用界的主流。可惜在国内暂时还看不到相关高可用的开源项目，所以我们成为了第一个吃螃蟹的人。

## 如何上手

源文档：https://bytedance.feishu.cn/docs/doccnFWmivHblarejnUNdeWwyVg#Q5JSLz

1.  打开仓库：https://github.com/hokaso/hocassian-people-neo4j，将项目克隆到本地。
1.  分别用相关IDE打开前后端，其中根目录为后端，「neo4j-nosql-front」目录为前端。
1.  参考[Neo4j 学习手册](https://f69397rwlh.feishu.cn/docs/doccnBVmeV7Ses6AO0rI0hpCQgg) 在服务器中配置好neo4j的生产环境。
1.  导入示例数据库：

首先在项目中找到graph.db.dump文件，将该文件移动至服务器的/home/ubuntu/目录中；

将数据库文件导入本地（停止→导入→启动）：

```
sudo neo4j stop

sudo neo4j-admin load --from=/home/ubuntu/graph.db.dump --database=graph.db --force

sudo neo4j start
```

5.  将上边文件夹里的application.yml.bak移动至src/main/resources/下，重命名为application.yml，并将配置逐项按个人实际情况进行设置；
5.  将上边文件夹里的nosql.zip解压后放入相应文件夹，路径与此处配置相匹配：

比如你设置profile为linux的/home，那么nosql的路径为/home/nosql；

7.  将上边文件夹里的vue.config.js.bak移动至neo4j-nosql-front/下，重命名为vue.config.js，并将配置逐项按个人实际情况进行设置；
7.  maven、npm install那些就不必多言了吧，装好之后就可以直接运行了~（记得用npm install --registry=https://registry.npm.taobao.org 来安装，国内一般我们都是这么装的……）

## 扩展开发

人物节点与人物关系均可通过编辑对应实体类完成属性的修改，若开发者希望迁移至个人业务，则修改实体类、修改mybatis、微调前端样式即可。

## 相关信息

使用技术栈：SpringBoot、neo4j、Vue.js、mybatis、echarts

推荐运行环境：Ubuntu 20.04 运存4G及以上

## 鸣谢

前后端均使用了[若依管理系统框架](https://doc.ruoyi.vip/)的代码，在此处感谢&安利下，用他们家的框架构建web应用程序真的超级快！