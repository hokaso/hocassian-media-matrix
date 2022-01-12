/*
 Navicat MySQL Data Transfer

 Source Server         : 本地数据库
 Source Server Type    : MySQL
 Source Server Version : 80021
 Source Host           : localhost:3306
 Source Schema         : media_matrix

 Target Server Type    : MySQL
 Target Server Version : 80021
 File Encoding         : 65001

 Date: 11/06/2021 10:56:33
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bus_about
-- ----------------------------
DROP TABLE IF EXISTS `bus_about`;
CREATE TABLE `bus_about`
(
    `about_id`          int NOT NULL AUTO_INCREMENT COMMENT '组织信息id',
    `about_info`        longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '组织简介',
    `about_keyword`     varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '组织关键字',
    `about_declaration` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '组织宣言',
    `about_qrcode`      longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '大众平台',
    `about_name`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '组织名称',
    `about_contact`     longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '联系方式',
    `about_icon`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '组织图标',
    `about_status`      char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否上架',
    `about_copyright`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '页脚声明',
    `about_record`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '页脚备案',
    PRIMARY KEY (`about_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 2
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='信息管理';

-- ----------------------------
-- Records of bus_about
-- ----------------------------
BEGIN;
INSERT INTO `bus_about`
VALUES (1,
        '物欲横流，谁主沉浮？同和系视频矩阵由多个亚文化小众KOL组成，迄今为止已为数十位天才级视频博主提供了多元化的信息流传播服务，在保证原创作者多项权益不受侵害的同时，我们也在持续建设为一个成熟的去中心小众亚文化推广平台。未来的PGC&UGC平台必定符合这三大定律：分类明确、高度集成和精致包装，我们的终极目标即通过最少量的资源达到上述三点的极致，通过最少量的信息输入，借由机器自动生成完整的「数据礼盒」并分发，以创造最大化的舆论价值。',
        '同和', '致力于以唯物主义的角度解读世界玄学和因果，向世界呈现中国左派青年的态度！',
        '[{\"name\":\"screenshot-20210423-105940_01.png\",\"url\":\"582930879362641920.png\"},{\"name\":\"screenshot-20210423-105940_02.png\",\"url\":\"582930900208332800.png\"},{\"name\":\"screenshot-20210423-105940_03.png\",\"url\":\"582930917086212096.png\"},{\"name\":\"screenshot-20210423-105940_04.png\",\"url\":\"582930933766959104.png\"},{\"name\":\"screenshot-20210423-105940_05.png\",\"url\":\"582930950124744704.png\"},{\"name\":\"screenshot-20210423-105940_06.png\",\"url\":\"582930967610798080.png\"},{\"name\":\"screenshot-20210423-105940_07.png\",\"url\":\"582930983561736192.png\"},{\"name\":\"screenshot-20210423-105940_08.png\",\"url\":\"582930998359240704.png\"}]',
        '同和新媒体矩阵', '广东省广州市海珠区西滘村吴家大街一巷1号\nQQ：3342614805 邮编：510000 Email：hokaso@qq.com', '582927238220230656.png', '0',
        'Copyright@ 2018-2021 同和新媒体矩阵·版权所有', '粤ICP备18016897号');
COMMIT;

-- ----------------------------
-- Table structure for bus_channel
-- ----------------------------
DROP TABLE IF EXISTS `bus_channel`;
CREATE TABLE `bus_channel`
(
    `channel_id`          int NOT NULL AUTO_INCREMENT COMMENT '频道id',
    `channel_url`         varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '频道链接',
    `channel_logo`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '频道图标',
    `channel_owner`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '频道所有者',
    `channel_video_count` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '频道视频数',
    `channel_status`      char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '频道是否完成抓取',
    `create_by`           varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time`         datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`           varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time`         datetime                                                      DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`channel_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Table structure for bus_friend
-- ----------------------------
DROP TABLE IF EXISTS `bus_friend`;
CREATE TABLE `bus_friend`
(
    `friend_id`     int NOT NULL AUTO_INCREMENT COMMENT '友链id',
    `friend_name`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '友链名称',
    `friend_url`    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '友链链接',
    `friend_info`   longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '友链信息',
    `friend_pic`    varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '友链图片',
    `friend_type`   char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     DEFAULT NULL COMMENT '友链类型',
    `friend_status` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     DEFAULT NULL COMMENT '友链状态',
    PRIMARY KEY (`friend_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 31
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='友情链接';

-- ----------------------------
-- Records of bus_friend
-- ----------------------------
BEGIN;
INSERT INTO `bus_friend`
VALUES (2, '视频大拍档', 'http://www.spdpd.net/', '剪辑助手是整合了视频剪辑中非常实用的功能于一体的桌面程序', '580129103655743488.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (3, '图层云', 'https://tucengyun.com/',
        '专注于海外精品AE模板、各种最新AE插件，PR模板、PR插件、转场预设、视频素材、音频素材。LR调色预设、LUT调色预设等资源，提供海外平面资源下载。', '580130419123695616.jpg', '0',
        '0');
INSERT INTO `bus_friend`
VALUES (4, '果子坤', 'https://www.sockite.com/',
        '果子坤sockite，联萌后期工作室；这里是果子坤sockite的个人博客也是联萌后期的交流站，这里有pr2018基本图形模板正在更新中，ps国外大师创意精品教程正在更新中,更有ps资源ae资源下载,ae原创教程,ae脚本教程果子坤在这里为你准备了资源大餐，希望你能够喜欢！',
        '580132096660746240.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (5, '月幕Galgame', 'https://www.ymgal.com/', '请感受这绝妙的故事体裁！', '580133042165919744.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (6, '文章同步助手', 'https://www.wechatsync.com/', '一次排版发布，多平台同步发布。解放自媒体人生产力，专注于写作本身！', '580133855420493824.jpg', '0',
        '0');
INSERT INTO `bus_friend`
VALUES (7, '澄空学园论坛', 'https://bbs.sumisora.net/', '元老级ACGN论坛', '580134859373293568.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (8, '阿Q的项目', 'https://www.qqworld.org/', '本站创建于2009年，站长是一名全栈工程师；主要作品有 QQWorld收藏家、QQWorld主题制造 和 QQWorld收银台。',
        '580135903834681344.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (9, 'Librian', 'https://librian.net/', '世界第一(自稱)的galgame引擎！', '580137868358594560.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (10, 'AVGPlus', 'https://avg-engine.com/', '用心创作，用爱发电；快速、优雅、灵活的跨平台的文字冒险游戏开发工具。', '580138986987859968.jpg', '0',
        '0');
INSERT INTO `bus_friend`
VALUES (11, 'KOLpower', 'https://kolpower.cc/', 'KOLpower為六指淵創辦之品牌，宗旨為『透過工具賜與創作者超能力』', '580143756473544704.jpg', '0',
        '0');
INSERT INTO `bus_friend`
VALUES (12, 'Spleeter', 'https://research.deezer.com/projects/spleeter.html',
        'Spleeter is Deezer source separation library with pretrained models written in Python and uses Tensorflow.',
        '580144985979236352.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (13, 'QuickCut', 'https://github.com/HaujetZhao/QuickCut',
        'Quick Cut 是一款轻量、强大、好用的视频处理软件。它是一个轻量的工具，而不是像 Davinci Resolve、Adobe Premiere 那样专业的、复杂的庞然大物。Quick Cut 可以满足普通人一般的视频处理需求：压缩视频、转码视频、倒放视频、合并片段、根据字幕裁切片段、自动配字幕、自动剪辑……',
        '580147850877612032.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (14, 'youtube-dl', 'http://ytdl-org.github.io/youtube-dl/',
        'youtube-dl is a command-line program to download videos from YouTube.com and a few more sites. It requires the Python interpreter (2.6, 2.7, or 3.2+), and it is not platform specific. We also provide a Windows executable that includes Python. youtube-dl should work in your Unix box, in Windows or in Mac OS X. It is released to the public domain, which means you can modify it, redistribute it or use it however you like.',
        '580148805228572672.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (15, 'WordPress Travel Mini Program', 'https://github.com/dchijack/Travel-Mini-Program',
        '基于 WordPress Mini Program API 插件创建的 WordPress 小程序之 Travel 主题，包括微信小程序、 QQ 小程序、百度智能小程序及今日头条小程序。虽然说是旅游类型，但是同样也适用于日记类型小程序，博客类型小程序。',
        '580150209984868352.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (27, '邓西软件', 'http://www.dllprotect.com/soft/', '专注小众软件开发定制', '582661172881534976.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (28, '有专自媒体助手', 'https://www.yzzmtzs.com/', '自媒体内容高效运营工具，一键同步文章和视频至30+家自媒体平台，多账号管理，爆文系统等。',
        '582670800075894784.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (29, 'dmit', 'https://www.dmit.io/index.php', '我們擁有全球多地的雲解決方案，性能強大、簡單易用且經濟實惠。利用網路從未如此簡單，現在就開始使用吧。',
        '584940955136962560.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (30, '腾讯云', 'https://cloud.tencent.com', '性能强大、安全、稳定的云产品。', '584941978798796800.jpg', '0', '0');
INSERT INTO `bus_friend`
VALUES (31, '若依管理系统', 'http://www.ruoyi.vip/', '一直想做一款后台管理系统，看了很多优秀的开源项目但是发现没有合适的。于是利用空闲休息时间开始自己写了一套后台系统，如此有了若依。',
        '600871880421027840.jpg', '0', '0');

COMMIT;

-- ----------------------------
-- Table structure for bus_swiper
-- ----------------------------
DROP TABLE IF EXISTS `bus_swiper`;
CREATE TABLE `bus_swiper`
(
    `swiper_id`     int NOT NULL AUTO_INCREMENT COMMENT '客户端轮播图id',
    `swiper_pic`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '轮播图地址',
    `swiper_name`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '轮播图名称',
    `swiper_status` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '轮播图状态',
    `create_at`     datetime                                                      DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建者',
    `create_by`     varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '创建时间',
    `update_at`     datetime                                                      DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新者',
    `update_by`     varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`swiper_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 10
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='主页轮播图';

-- ----------------------------
-- Records of bus_swiper
-- ----------------------------
BEGIN;
INSERT INTO `bus_swiper`
VALUES (1, '519324485657309184.jpg', '锋芒毕露', '0', '2021-03-18 03:39:57', NULL, '2021-03-18 03:39:57', 'admin');
INSERT INTO `bus_swiper`
VALUES (2, '519329514413895680.jpg', '暧昧情境', '0', '2021-01-02 01:33:30', 'admin', '2021-01-02 01:33:30', 'admin');
INSERT INTO `bus_swiper`
VALUES (3, '519332992104280064.jpg', '暮色城市', '0', '2021-01-02 01:33:32', 'admin', '2021-01-02 01:33:32', 'admin');
INSERT INTO `bus_swiper`
VALUES (4, '542683535631462400.jpg', '校园风光', '0', '2021-03-10 04:51:35', 'admin', '2021-03-10 04:51:35', 'admin');
INSERT INTO `bus_swiper`
VALUES (6, '567012644985516032.jpg', '同和新媒体矩阵概览图', '1', '2021-03-10 04:51:33', 'admin', '2021-03-10 04:51:33', 'admin');
INSERT INTO `bus_swiper`
VALUES (7, '569893850165030912.jpg', '被看见的价值', '1', '2021-03-18 03:39:56', 'admin', '2021-03-18 03:39:56', 'admin');
INSERT INTO `bus_swiper`
VALUES (8, '572517144903036928.jpg', '灵魂发问', '1', '2021-03-25 09:23:25', 'admin', '2021-03-25 09:23:25', 'admin');
INSERT INTO `bus_swiper`
VALUES (9, '572609174316527616.jpg', '抱团求存', '1', '2021-03-25 09:23:52', 'admin', '2021-03-25 23:29:08', 'admin');
COMMIT;

-- ----------------------------
-- Table structure for bus_video
-- ----------------------------
DROP TABLE IF EXISTS `bus_video`;
CREATE TABLE `bus_video`
(
    `video_id`       int NOT NULL AUTO_INCREMENT COMMENT '视频id',
    `video_ytb_id`   varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '视频ytb_id',
    `video_title`    text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '视频标题',
    `video_profile`  text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '视频简介',
    `video_url`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '视频采集链接',
    `video_pic`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '视频封面',
    `video_status`   char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '视频状态（0：未上线，1：已上线，2：未下载）',
    `video_class`    text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '视频分类',
    `video_publish`  datetime                                                      DEFAULT NULL COMMENT '视频发布时间',
    `video_author`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '视频作者（默认为频道主）',
    `video_is_huge`  char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否为带制作视频',
    `video_huge_pic` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '带制作视频封面',
    `video_path`     varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '文件路径',
    `video_json`     varchar(127) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '视频详情',
    `create_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time`    datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time`    datetime                                                      DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`video_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='视频管理';

-- ----------------------------
-- Table structure for cre_chapter
-- ----------------------------
DROP TABLE IF EXISTS `cre_chapter`;
CREATE TABLE `cre_chapter`
(
    `chapter_story_id`          int NOT NULL COMMENT '段落编号',
    `chapter_work_id`           int                                                           DEFAULT NULL COMMENT '作品编号',
    `chapter_story_name`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '段落标题',
    `chapter_story_description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '段落描述',
    `chapter_story_times`       int                                                           DEFAULT NULL COMMENT '段落周目',
    `chapter_story_ending`      int                                                           DEFAULT NULL COMMENT '段落结局编号',
    `chapter_story_type`        char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '段落类型',
    `chapter_story_condiation`  longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '段落条件',
    `chapter_story_operation`   longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '段落变更',
    `chapter_story_next`        longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '下一段落',
    `chapter_story_previous`    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '上一段落',
    `chapter_story_addtional`   longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '附加信息',
    PRIMARY KEY (`chapter_story_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='篇章管理';

-- ----------------------------
-- Table structure for cre_work
-- ----------------------------
DROP TABLE IF EXISTS `cre_work`;
CREATE TABLE `cre_work`
(
    `work_story_id`      int NOT NULL AUTO_INCREMENT COMMENT '作品编号',
    `work_story_name`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '作品名称',
    `work_story_en_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '作品英文名称',
    `work_story_info`    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '作品简介',
    `work_story_author`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '作品作者',
    PRIMARY KEY (`work_story_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='作品管理';

-- ----------------------------
-- Table structure for gen_table
-- ----------------------------
DROP TABLE IF EXISTS `gen_table`;
CREATE TABLE `gen_table`
(
    `table_id`          bigint NOT NULL AUTO_INCREMENT COMMENT '编号',
    `table_name`        varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '表名称',
    `table_comment`     varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '表描述',
    `sub_table_name`    varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '关联子表的表名',
    `sub_table_fk_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '子表关联的外键名',
    `class_name`        varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '实体类名称',
    `tpl_category`      varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT 'crud' COMMENT '使用的模板（crud单表操作 tree树表操作）',
    `package_name`      varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '生成包路径',
    `module_name`       varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '生成模块名',
    `business_name`     varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '生成业务名',
    `function_name`     varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '生成功能名',
    `function_author`   varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '生成功能作者',
    `gen_type`          char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci       DEFAULT '0' COMMENT '生成代码方式（0zip压缩包 1自定义路径）',
    `gen_path`          varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '/' COMMENT '生成路径（不填默认项目路径）',
    `options`           varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '其它生成选项',
    `create_by`         varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '' COMMENT '创建者',
    `create_time`       datetime                                                       DEFAULT NULL COMMENT '创建时间',
    `update_by`         varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '' COMMENT '更新者',
    `update_time`       datetime                                                       DEFAULT NULL COMMENT '更新时间',
    `remark`            varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`table_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='代码生成业务表';

-- ----------------------------
-- Table structure for gen_table_column
-- ----------------------------
DROP TABLE IF EXISTS `gen_table_column`;
CREATE TABLE `gen_table_column`
(
    `column_id`      bigint NOT NULL AUTO_INCREMENT COMMENT '编号',
    `table_id`       varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '归属表编号',
    `column_name`    varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '列名称',
    `column_comment` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '列描述',
    `column_type`    varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '列类型',
    `java_type`      varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'JAVA类型',
    `java_field`     varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'JAVA字段名',
    `is_pk`          char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否主键（1是）',
    `is_increment`   char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否自增（1是）',
    `is_required`    char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否必填（1是）',
    `is_insert`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否为插入字段（1是）',
    `is_edit`        char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否编辑字段（1是）',
    `is_list`        char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否列表字段（1是）',
    `is_query`       char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否查询字段（1是）',
    `query_type`     varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'EQ' COMMENT '查询方式（等于、不等于、大于、小于、范围）',
    `html_type`      varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）',
    `dict_type`      varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典类型',
    `sort`           int                                                           DEFAULT NULL COMMENT '排序',
    `create_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time`    datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time`    datetime                                                      DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`column_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='代码生成业务表字段';

-- ----------------------------
-- Table structure for mat_audio
-- ----------------------------
DROP TABLE IF EXISTS `mat_audio`;
CREATE TABLE `mat_audio`
(
    `audio_id`      int NOT NULL AUTO_INCREMENT COMMENT '音频素材id',
    `audio_path`    varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '音频素材路径',
    `audio_name`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '音频素材名称',
    `audio_author`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '音频素材作者',
    `audio_type`    char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '音频素材类型（0纯音乐，1歌曲）',
    `audio_status`  char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '音频素材状态（0处理完毕，1待处理，2无需处理，3正在处理）',
    `audio_emotion` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '音频素材情感标签',
    `audio_note`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '音频素材备注',
    `audio_time`    varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '音频素材时长',
    `is_copyright`  char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '音频素材版权（0有版权，1无版权）',
    `is_show`       char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否上架（0上架，1未上架）',
    `audio_meta`    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '音频素材情感识别元数据',
    PRIMARY KEY (`audio_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='音频素材表';

-- ----------------------------
-- Table structure for mat_clip
-- ----------------------------
DROP TABLE IF EXISTS `mat_clip`;
CREATE TABLE `mat_clip`
(
    `material_id`           int NOT NULL AUTO_INCREMENT COMMENT '素材id',
    `material_path`         varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '素材名称',
    `material_size`         varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '素材尺寸',
    `material_time`         varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT NULL COMMENT '素材时长',
    `material_note`         varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '素材标注',
    `material_mark`         decimal(5, 2)                                                 DEFAULT NULL COMMENT '素材打分',
    `material_status`       char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '素材状态（0处理完毕，1初入库，2正在处理，3准备处理）',
    `material_tag`          longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '素材标签',
    `material_create`       datetime(6)                                                   DEFAULT NULL COMMENT '素材创建时间',
    `material_type`         char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '素材类型（0高质素材，1普通素材）',
    `material_start`        decimal(10, 4)                                                DEFAULT NULL COMMENT '分割入点',
    `material_end`          decimal(10, 4)                                                DEFAULT NULL COMMENT '分割出点',
    `material_analyze_meta` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '素材识别元信息',
    `is_copyright`          char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '素材版权（0有版权，1无版权）',
    `is_show`               char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否上架（0上架，1未上架）',
    `is_merge`              char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否已合并（0归档，1未归档）',
    `has_uploaded`          char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '分发矩阵使用情况（0没发布过，1已经发布过）',
    `error_info`            longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '失败原因',
    PRIMARY KEY (`material_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='视频素材表';

-- ----------------------------
-- Table structure for mat_image
-- ----------------------------
DROP TABLE IF EXISTS `mat_image`;
CREATE TABLE `mat_image`
(
    `image_id`     int NOT NULL AUTO_INCREMENT COMMENT '图片素材id',
    `image_path`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '图片素材路径',
    `image_note`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '图片素材标注',
    `image_size`   varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '图片素材尺寸',
    `image_tag`    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '图片素材标签',
    `image_mark`   decimal(5, 2)                                                 DEFAULT NULL COMMENT '图片素材打分',
    `image_status` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '图片素材状态',
    `image_type`   char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '图片素材类型（0高质素材，1普通素材）',
    `is_copyright` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '素材版权（0有版权，1无版权）',
    `is_show`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '是否上架（0上架，1未上架）',
    `image_meta`   longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '图片素材元数据',
    `error_info`   longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '失败原因',
    PRIMARY KEY (`image_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='图片素材表';

-- ----------------------------
-- Table structure for pub_distribution
-- ----------------------------
DROP TABLE IF EXISTS `pub_distribution`;
CREATE TABLE `pub_distribution`
(
    `dis_id`      int NOT NULL COMMENT '内容id',
    `dis_title`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '内容标题',
    `dis_contain` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '内容正文',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                      DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`dis_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='消息分发';

-- ----------------------------
-- Table structure for pub_mail
-- ----------------------------
DROP TABLE IF EXISTS `pub_mail`;
CREATE TABLE `pub_mail`
(
    `mail_id`        int NOT NULL COMMENT '发出邮箱id',
    `mail_name`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '发出邮箱标注',
    `mail_type`      char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '发出邮箱类型',
    `mail_address`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '发出邮箱地址',
    `mail_custom_01` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '发出邮箱保留字段01',
    `mail_custom_02` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '发出邮箱保留字段02',
    `mail_custom_03` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '发出邮箱保留字段03',
    `mail_custom_04` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '发出邮箱保留字段04',
    `create_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time`    datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time`    datetime                                                      DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`mail_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='分发邮箱';

-- ----------------------------
-- Table structure for pub_model
-- ----------------------------
DROP TABLE IF EXISTS `pub_model`;
CREATE TABLE `pub_model`
(
    `model_id`        int NOT NULL COMMENT '模板id',
    `model_name`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '模板名称',
    `model_unit_list` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '包含单位列表',
    PRIMARY KEY (`model_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='分发单位模板';

-- ----------------------------
-- Table structure for pub_unit
-- ----------------------------
DROP TABLE IF EXISTS `pub_unit`;
CREATE TABLE `pub_unit`
(
    `unit_id`     int NOT NULL AUTO_INCREMENT COMMENT '媒体单位id',
    `unit_name`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '媒体单位名称',
    `unit_info`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '媒体单位简介',
    `unit_email`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '媒体单位邮箱',
    `unit_type`   char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '媒体单位类型',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                      DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`unit_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='媒体单位';

-- ----------------------------
-- Table structure for pub_unit_dis
-- ----------------------------
DROP TABLE IF EXISTS `pub_unit_dis`;
CREATE TABLE `pub_unit_dis`
(
    `unit_id` int DEFAULT NULL COMMENT '单位id',
    `dis_id`  int DEFAULT NULL COMMENT '分发id'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='单位-分发-中间表';

-- ----------------------------
-- Table structure for QRTZ_BLOB_TRIGGERS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_BLOB_TRIGGERS`;
CREATE TABLE `QRTZ_BLOB_TRIGGERS`
(
    `sched_name`    varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_name`  varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_group` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `blob_data`     blob,
    PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`),
    CONSTRAINT `qrtz_blob_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `QRTZ_TRIGGERS` (`sched_name`, `trigger_name`, `trigger_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Table structure for QRTZ_CALENDARS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_CALENDARS`;
CREATE TABLE `QRTZ_CALENDARS`
(
    `sched_name`    varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `calendar_name` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `calendar`      blob                                    NOT NULL,
    PRIMARY KEY (`sched_name`, `calendar_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Table structure for QRTZ_CRON_TRIGGERS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_CRON_TRIGGERS`;
CREATE TABLE `QRTZ_CRON_TRIGGERS`
(
    `sched_name`      varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_name`    varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_group`   varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `cron_expression` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `time_zone_id`    varchar(80) COLLATE utf8mb4_general_ci DEFAULT NULL,
    PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`),
    CONSTRAINT `qrtz_cron_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `QRTZ_TRIGGERS` (`sched_name`, `trigger_name`, `trigger_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of QRTZ_CRON_TRIGGERS
-- ----------------------------
BEGIN;
INSERT INTO `QRTZ_CRON_TRIGGERS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME1', 'DEFAULT', '0/10 * * * * ?', 'Asia/Shanghai');
INSERT INTO `QRTZ_CRON_TRIGGERS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME2', 'DEFAULT', '0/15 * * * * ?', 'Asia/Shanghai');
INSERT INTO `QRTZ_CRON_TRIGGERS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME3', 'DEFAULT', '0/20 * * * * ?', 'Asia/Shanghai');
COMMIT;

-- ----------------------------
-- Table structure for QRTZ_FIRED_TRIGGERS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_FIRED_TRIGGERS`;
CREATE TABLE `QRTZ_FIRED_TRIGGERS`
(
    `sched_name`        varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `entry_id`          varchar(95) COLLATE utf8mb4_general_ci  NOT NULL,
    `trigger_name`      varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_group`     varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `instance_name`     varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `fired_time`        bigint                                  NOT NULL,
    `sched_time`        bigint                                  NOT NULL,
    `priority`          int                                     NOT NULL,
    `state`             varchar(16) COLLATE utf8mb4_general_ci  NOT NULL,
    `job_name`          varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `job_group`         varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `is_nonconcurrent`  varchar(1) COLLATE utf8mb4_general_ci   DEFAULT NULL,
    `requests_recovery` varchar(1) COLLATE utf8mb4_general_ci   DEFAULT NULL,
    PRIMARY KEY (`sched_name`, `entry_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Table structure for QRTZ_JOB_DETAILS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_JOB_DETAILS`;
CREATE TABLE `QRTZ_JOB_DETAILS`
(
    `sched_name`        varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `job_name`          varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `job_group`         varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `description`       varchar(250) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `job_class_name`    varchar(250) COLLATE utf8mb4_general_ci NOT NULL,
    `is_durable`        varchar(1) COLLATE utf8mb4_general_ci   NOT NULL,
    `is_nonconcurrent`  varchar(1) COLLATE utf8mb4_general_ci   NOT NULL,
    `is_update_data`    varchar(1) COLLATE utf8mb4_general_ci   NOT NULL,
    `requests_recovery` varchar(1) COLLATE utf8mb4_general_ci   NOT NULL,
    `job_data`          blob,
    PRIMARY KEY (`sched_name`, `job_name`, `job_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of QRTZ_JOB_DETAILS
-- ----------------------------
BEGIN;
INSERT INTO `QRTZ_JOB_DETAILS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME1', 'DEFAULT', NULL,
        'com.ruoyi.quartz.util.QuartzDisallowConcurrentExecution', '0', '1', '0', '0',
        0xACED0005737200156F72672E71756172747A2E4A6F62446174614D61709FB083E8BFA9B0CB020000787200266F72672E71756172747A2E7574696C732E537472696E674B65794469727479466C61674D61708208E8C3FBC55D280200015A0013616C6C6F77735472616E7369656E74446174617872001D6F72672E71756172747A2E7574696C732E4469727479466C61674D617013E62EAD28760ACE0200025A000564697274794C00036D617074000F4C6A6176612F7574696C2F4D61703B787001737200116A6176612E7574696C2E486173684D61700507DAC1C31660D103000246000A6C6F6164466163746F724900097468726573686F6C6478703F4000000000000C7708000000100000000174000F5441534B5F50524F504552544945537372001E636F6D2E72756F79692E71756172747A2E646F6D61696E2E5379734A6F6200000000000000010200084C000A636F6E63757272656E747400124C6A6176612F6C616E672F537472696E673B4C000E63726F6E45787072657373696F6E71007E00094C000C696E766F6B6554617267657471007E00094C00086A6F6247726F757071007E00094C00056A6F6249647400104C6A6176612F6C616E672F4C6F6E673B4C00076A6F624E616D6571007E00094C000D6D697366697265506F6C69637971007E00094C000673746174757371007E000978720027636F6D2E72756F79692E636F6D6D6F6E2E636F72652E646F6D61696E2E42617365456E7469747900000000000000010200074C0008637265617465427971007E00094C000A63726561746554696D657400104C6A6176612F7574696C2F446174653B4C0006706172616D7371007E00034C000672656D61726B71007E00094C000B73656172636856616C756571007E00094C0008757064617465427971007E00094C000A75706461746554696D6571007E000C787074000561646D696E7372000E6A6176612E7574696C2E44617465686A81014B59741903000078707708000001622CDE29E078707400007070707400013174000E302F3130202A202A202A202A203F74001172795461736B2E72794E6F506172616D7374000744454641554C547372000E6A6176612E6C616E672E4C6F6E673B8BE490CC8F23DF0200014A000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B02000078700000000000000001740018E7B3BBE7BB9FE9BB98E8AEA4EFBC88E697A0E58F82EFBC8974000133740001317800);
INSERT INTO `QRTZ_JOB_DETAILS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME2', 'DEFAULT', NULL,
        'com.ruoyi.quartz.util.QuartzDisallowConcurrentExecution', '0', '1', '0', '0',
        0xACED0005737200156F72672E71756172747A2E4A6F62446174614D61709FB083E8BFA9B0CB020000787200266F72672E71756172747A2E7574696C732E537472696E674B65794469727479466C61674D61708208E8C3FBC55D280200015A0013616C6C6F77735472616E7369656E74446174617872001D6F72672E71756172747A2E7574696C732E4469727479466C61674D617013E62EAD28760ACE0200025A000564697274794C00036D617074000F4C6A6176612F7574696C2F4D61703B787001737200116A6176612E7574696C2E486173684D61700507DAC1C31660D103000246000A6C6F6164466163746F724900097468726573686F6C6478703F4000000000000C7708000000100000000174000F5441534B5F50524F504552544945537372001E636F6D2E72756F79692E71756172747A2E646F6D61696E2E5379734A6F6200000000000000010200084C000A636F6E63757272656E747400124C6A6176612F6C616E672F537472696E673B4C000E63726F6E45787072657373696F6E71007E00094C000C696E766F6B6554617267657471007E00094C00086A6F6247726F757071007E00094C00056A6F6249647400104C6A6176612F6C616E672F4C6F6E673B4C00076A6F624E616D6571007E00094C000D6D697366697265506F6C69637971007E00094C000673746174757371007E000978720027636F6D2E72756F79692E636F6D6D6F6E2E636F72652E646F6D61696E2E42617365456E7469747900000000000000010200074C0008637265617465427971007E00094C000A63726561746554696D657400104C6A6176612F7574696C2F446174653B4C0006706172616D7371007E00034C000672656D61726B71007E00094C000B73656172636856616C756571007E00094C0008757064617465427971007E00094C000A75706461746554696D6571007E000C787074000561646D696E7372000E6A6176612E7574696C2E44617465686A81014B59741903000078707708000001622CDE29E078707400007070707400013174000E302F3135202A202A202A202A203F74001572795461736B2E7279506172616D7328277279272974000744454641554C547372000E6A6176612E6C616E672E4C6F6E673B8BE490CC8F23DF0200014A000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B02000078700000000000000002740018E7B3BBE7BB9FE9BB98E8AEA4EFBC88E69C89E58F82EFBC8974000133740001317800);
INSERT INTO `QRTZ_JOB_DETAILS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME3', 'DEFAULT', NULL,
        'com.ruoyi.quartz.util.QuartzDisallowConcurrentExecution', '0', '1', '0', '0',
        0xACED0005737200156F72672E71756172747A2E4A6F62446174614D61709FB083E8BFA9B0CB020000787200266F72672E71756172747A2E7574696C732E537472696E674B65794469727479466C61674D61708208E8C3FBC55D280200015A0013616C6C6F77735472616E7369656E74446174617872001D6F72672E71756172747A2E7574696C732E4469727479466C61674D617013E62EAD28760ACE0200025A000564697274794C00036D617074000F4C6A6176612F7574696C2F4D61703B787001737200116A6176612E7574696C2E486173684D61700507DAC1C31660D103000246000A6C6F6164466163746F724900097468726573686F6C6478703F4000000000000C7708000000100000000174000F5441534B5F50524F504552544945537372001E636F6D2E72756F79692E71756172747A2E646F6D61696E2E5379734A6F6200000000000000010200084C000A636F6E63757272656E747400124C6A6176612F6C616E672F537472696E673B4C000E63726F6E45787072657373696F6E71007E00094C000C696E766F6B6554617267657471007E00094C00086A6F6247726F757071007E00094C00056A6F6249647400104C6A6176612F6C616E672F4C6F6E673B4C00076A6F624E616D6571007E00094C000D6D697366697265506F6C69637971007E00094C000673746174757371007E000978720027636F6D2E72756F79692E636F6D6D6F6E2E636F72652E646F6D61696E2E42617365456E7469747900000000000000010200074C0008637265617465427971007E00094C000A63726561746554696D657400104C6A6176612F7574696C2F446174653B4C0006706172616D7371007E00034C000672656D61726B71007E00094C000B73656172636856616C756571007E00094C0008757064617465427971007E00094C000A75706461746554696D6571007E000C787074000561646D696E7372000E6A6176612E7574696C2E44617465686A81014B59741903000078707708000001622CDE29E078707400007070707400013174000E302F3230202A202A202A202A203F74003872795461736B2E72794D756C7469706C65506172616D7328277279272C20747275652C20323030304C2C203331362E3530442C203130302974000744454641554C547372000E6A6176612E6C616E672E4C6F6E673B8BE490CC8F23DF0200014A000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B02000078700000000000000003740018E7B3BBE7BB9FE9BB98E8AEA4EFBC88E5A49AE58F82EFBC8974000133740001317800);
COMMIT;

-- ----------------------------
-- Table structure for QRTZ_LOCKS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_LOCKS`;
CREATE TABLE `QRTZ_LOCKS`
(
    `sched_name` varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `lock_name`  varchar(40) COLLATE utf8mb4_general_ci  NOT NULL,
    PRIMARY KEY (`sched_name`, `lock_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of QRTZ_LOCKS
-- ----------------------------
BEGIN;
INSERT INTO `QRTZ_LOCKS`
VALUES ('RuoyiScheduler', 'STATE_ACCESS');
INSERT INTO `QRTZ_LOCKS`
VALUES ('RuoyiScheduler', 'TRIGGER_ACCESS');
COMMIT;

-- ----------------------------
-- Table structure for QRTZ_PAUSED_TRIGGER_GRPS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_PAUSED_TRIGGER_GRPS`;
CREATE TABLE `QRTZ_PAUSED_TRIGGER_GRPS`
(
    `sched_name`    varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_group` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    PRIMARY KEY (`sched_name`, `trigger_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Table structure for QRTZ_SCHEDULER_STATE
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_SCHEDULER_STATE`;
CREATE TABLE `QRTZ_SCHEDULER_STATE`
(
    `sched_name`        varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `instance_name`     varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `last_checkin_time` bigint                                  NOT NULL,
    `checkin_interval`  bigint                                  NOT NULL,
    PRIMARY KEY (`sched_name`, `instance_name`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of QRTZ_SCHEDULER_STATE
-- ----------------------------
BEGIN;
INSERT INTO `QRTZ_SCHEDULER_STATE`
VALUES ('RuoyiScheduler', 'BytedancedeMacBook-Pro.local1623379877021', 1623380180067, 15000);
COMMIT;

-- ----------------------------
-- Table structure for QRTZ_SIMPLE_TRIGGERS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_SIMPLE_TRIGGERS`;
CREATE TABLE `QRTZ_SIMPLE_TRIGGERS`
(
    `sched_name`      varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_name`    varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_group`   varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `repeat_count`    bigint                                  NOT NULL,
    `repeat_interval` bigint                                  NOT NULL,
    `times_triggered` bigint                                  NOT NULL,
    PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`),
    CONSTRAINT `qrtz_simple_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `QRTZ_TRIGGERS` (`sched_name`, `trigger_name`, `trigger_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Table structure for QRTZ_SIMPROP_TRIGGERS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_SIMPROP_TRIGGERS`;
CREATE TABLE `QRTZ_SIMPROP_TRIGGERS`
(
    `sched_name`    varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_name`  varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_group` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `str_prop_1`    varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `str_prop_2`    varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `str_prop_3`    varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `int_prop_1`    int                                     DEFAULT NULL,
    `int_prop_2`    int                                     DEFAULT NULL,
    `long_prop_1`   bigint                                  DEFAULT NULL,
    `long_prop_2`   bigint                                  DEFAULT NULL,
    `dec_prop_1`    decimal(13, 4)                          DEFAULT NULL,
    `dec_prop_2`    decimal(13, 4)                          DEFAULT NULL,
    `bool_prop_1`   varchar(1) COLLATE utf8mb4_general_ci   DEFAULT NULL,
    `bool_prop_2`   varchar(1) COLLATE utf8mb4_general_ci   DEFAULT NULL,
    PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`),
    CONSTRAINT `qrtz_simprop_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `QRTZ_TRIGGERS` (`sched_name`, `trigger_name`, `trigger_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Table structure for QRTZ_TRIGGERS
-- ----------------------------
DROP TABLE IF EXISTS `QRTZ_TRIGGERS`;
CREATE TABLE `QRTZ_TRIGGERS`
(
    `sched_name`     varchar(120) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_name`   varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `trigger_group`  varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `job_name`       varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `job_group`      varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
    `description`    varchar(250) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `next_fire_time` bigint                                  DEFAULT NULL,
    `prev_fire_time` bigint                                  DEFAULT NULL,
    `priority`       int                                     DEFAULT NULL,
    `trigger_state`  varchar(16) COLLATE utf8mb4_general_ci  NOT NULL,
    `trigger_type`   varchar(8) COLLATE utf8mb4_general_ci   NOT NULL,
    `start_time`     bigint                                  NOT NULL,
    `end_time`       bigint                                  DEFAULT NULL,
    `calendar_name`  varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `misfire_instr`  smallint                                DEFAULT NULL,
    `job_data`       blob,
    PRIMARY KEY (`sched_name`, `trigger_name`, `trigger_group`),
    KEY `sched_name` (`sched_name`, `job_name`, `job_group`),
    CONSTRAINT `qrtz_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `job_name`, `job_group`) REFERENCES `QRTZ_JOB_DETAILS` (`sched_name`, `job_name`, `job_group`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of QRTZ_TRIGGERS
-- ----------------------------
BEGIN;
INSERT INTO `QRTZ_TRIGGERS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME1', 'DEFAULT', 'TASK_CLASS_NAME1', 'DEFAULT', NULL, 1623379880000, -1, 5,
        'PAUSED', 'CRON', 1623379877000, 0, NULL, 2, '');
INSERT INTO `QRTZ_TRIGGERS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME2', 'DEFAULT', 'TASK_CLASS_NAME2', 'DEFAULT', NULL, 1623379890000, -1, 5,
        'PAUSED', 'CRON', 1623379877000, 0, NULL, 2, '');
INSERT INTO `QRTZ_TRIGGERS`
VALUES ('RuoyiScheduler', 'TASK_CLASS_NAME3', 'DEFAULT', 'TASK_CLASS_NAME3', 'DEFAULT', NULL, 1623379880000, -1, 5,
        'PAUSED', 'CRON', 1623379877000, 0, NULL, 2, '');
COMMIT;

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config`
(
    `config_id`    int NOT NULL AUTO_INCREMENT COMMENT '参数主键',
    `config_name`  varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '参数名称',
    `config_key`   varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '参数键名',
    `config_value` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '参数键值',
    `config_type`  char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT 'N' COMMENT '系统内置（Y是 N否）',
    `create_by`    varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time`  datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`    varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time`  datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`       varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`config_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 100
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='参数配置表';

-- ----------------------------
-- Records of sys_config
-- ----------------------------
BEGIN;
INSERT INTO `sys_config`
VALUES (1, '主框架页-默认皮肤样式名称', 'sys.index.skinName', 'skin-blue', 'Y', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '蓝色 skin-blue、绿色 skin-green、紫色 skin-purple、红色 skin-red、黄色 skin-yellow');
INSERT INTO `sys_config`
VALUES (2, '用户管理-账号初始密码', 'sys.user.initPassword', '123456', 'Y', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '初始化密码 123456');
INSERT INTO `sys_config`
VALUES (3, '主框架页-侧边栏主题', 'sys.index.sideTheme', 'theme-dark', 'Y', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '深色主题theme-dark，浅色主题theme-light');
COMMIT;

-- ----------------------------
-- Table structure for sys_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_dept`;
CREATE TABLE `sys_dept`
(
    `dept_id`     bigint NOT NULL AUTO_INCREMENT COMMENT '部门id',
    `parent_id`   bigint                                                       DEFAULT '0' COMMENT '父部门id',
    `ancestors`   varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '祖级列表',
    `dept_name`   varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '部门名称',
    `order_num`   int                                                          DEFAULT '0' COMMENT '显示顺序',
    `leader`      varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '负责人',
    `phone`       varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '联系电话',
    `email`       varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱',
    `status`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     DEFAULT '0' COMMENT '部门状态（0正常 1停用）',
    `del_flag`    char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                     DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                     DEFAULT NULL COMMENT '更新时间',
    PRIMARY KEY (`dept_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 201
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='部门表';

-- ----------------------------
-- Records of sys_dept
-- ----------------------------
BEGIN;
INSERT INTO `sys_dept`
VALUES (100, 0, '0', '家庭', 0, 'Hocassian', '13640851646', 'hokaso@qq.com', '0', '0', 'admin', '2018-03-16 11:33:00',
        'admin', '2020-09-10 10:31:37');
INSERT INTO `sys_dept`
VALUES (101, 100, '0,100', '事务', 1, 'Hocassian', '13640851646', '', '0', '0', 'admin', '2018-03-16 11:33:00', 'admin',
        '2020-09-10 10:31:37');
INSERT INTO `sys_dept`
VALUES (102, 100, '0,100', '长沙分公司', 2, '若依', '15888888888', 'ry@qq.com', '0', '2', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00');
INSERT INTO `sys_dept`
VALUES (103, 101, '0,100,101', '研发', 1, '', '', '', '0', '0', 'admin', '2018-03-16 11:33:00', 'admin',
        '2020-09-10 10:31:37');
INSERT INTO `sys_dept`
VALUES (104, 101, '0,100,101', '市场部门', 2, '若依', '15888888888', 'ry@qq.com', '0', '2', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00');
INSERT INTO `sys_dept`
VALUES (105, 101, '0,100,101', '测试部门', 3, '若依', '15888888888', 'ry@qq.com', '0', '2', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00');
INSERT INTO `sys_dept`
VALUES (106, 101, '0,100,101', '财务部门', 4, '若依', '15888888888', 'ry@qq.com', '0', '2', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00');
INSERT INTO `sys_dept`
VALUES (107, 101, '0,100,101', '运维部门', 5, '若依', '15888888888', 'ry@qq.com', '0', '2', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00');
INSERT INTO `sys_dept`
VALUES (108, 102, '0,100,102', '市场部门', 1, '若依', '15888888888', 'ry@qq.com', '0', '2', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00');
INSERT INTO `sys_dept`
VALUES (109, 102, '0,100,102', '财务部门', 2, '若依', '15888888888', 'ry@qq.com', '0', '2', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00');
INSERT INTO `sys_dept`
VALUES (200, 100, '0,100', '媒体', 1, NULL, NULL, NULL, '0', '0', 'admin', '2020-09-10 10:29:43', '', NULL);
COMMIT;

-- ----------------------------
-- Table structure for sys_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_data`;
CREATE TABLE `sys_dict_data`
(
    `dict_code`   bigint NOT NULL AUTO_INCREMENT COMMENT '字典编码',
    `dict_sort`   int                                                           DEFAULT '0' COMMENT '字典排序',
    `dict_label`  varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典标签',
    `dict_value`  varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典键值',
    `dict_type`   varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典类型',
    `css_class`   varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
    `list_class`  varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '表格回显样式',
    `is_default`  char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT 'N' COMMENT '是否默认（Y是 N否）',
    `status`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '状态（0正常 1停用）',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`      varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`dict_code`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 151
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='字典数据表';

-- ----------------------------
-- Records of sys_dict_data
-- ----------------------------
BEGIN;
INSERT INTO `sys_dict_data`
VALUES (1, 1, '男', '0', 'sys_user_sex', '', '', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00',
        '性别男');
INSERT INTO `sys_dict_data`
VALUES (2, 2, '女', '1', 'sys_user_sex', '', '', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00',
        '性别女');
INSERT INTO `sys_dict_data`
VALUES (3, 3, '未知', '2', 'sys_user_sex', '', '', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00',
        '性别未知');
INSERT INTO `sys_dict_data`
VALUES (4, 1, '显示', '0', 'sys_show_hide', '', 'primary', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '显示菜单');
INSERT INTO `sys_dict_data`
VALUES (5, 2, '隐藏', '1', 'sys_show_hide', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '隐藏菜单');
INSERT INTO `sys_dict_data`
VALUES (6, 1, '正常', '0', 'sys_normal_disable', '', 'primary', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '正常状态');
INSERT INTO `sys_dict_data`
VALUES (7, 2, '停用', '1', 'sys_normal_disable', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '停用状态');
INSERT INTO `sys_dict_data`
VALUES (8, 1, '正常', '0', 'sys_job_status', '', 'primary', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '正常状态');
INSERT INTO `sys_dict_data`
VALUES (9, 2, '暂停', '1', 'sys_job_status', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '停用状态');
INSERT INTO `sys_dict_data`
VALUES (10, 1, '默认', 'DEFAULT', 'sys_job_group', '', '', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '默认分组');
INSERT INTO `sys_dict_data`
VALUES (11, 2, '系统', 'SYSTEM', 'sys_job_group', '', '', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '系统分组');
INSERT INTO `sys_dict_data`
VALUES (12, 1, '是', 'Y', 'sys_yes_no', '', 'primary', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '系统默认是');
INSERT INTO `sys_dict_data`
VALUES (13, 2, '否', 'N', 'sys_yes_no', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '系统默认否');
INSERT INTO `sys_dict_data`
VALUES (14, 1, '通知', '1', 'sys_notice_type', '', 'warning', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '通知');
INSERT INTO `sys_dict_data`
VALUES (15, 2, '公告', '2', 'sys_notice_type', '', 'success', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '公告');
INSERT INTO `sys_dict_data`
VALUES (16, 1, '正常', '0', 'sys_notice_status', '', 'primary', 'Y', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '正常状态');
INSERT INTO `sys_dict_data`
VALUES (17, 2, '关闭', '1', 'sys_notice_status', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '关闭状态');
INSERT INTO `sys_dict_data`
VALUES (18, 1, '新增', '1', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '新增操作');
INSERT INTO `sys_dict_data`
VALUES (19, 2, '修改', '2', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '修改操作');
INSERT INTO `sys_dict_data`
VALUES (20, 3, '删除', '3', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '删除操作');
INSERT INTO `sys_dict_data`
VALUES (21, 4, '授权', '4', 'sys_oper_type', '', 'primary', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '授权操作');
INSERT INTO `sys_dict_data`
VALUES (22, 5, '导出', '5', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '导出操作');
INSERT INTO `sys_dict_data`
VALUES (23, 6, '导入', '6', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '导入操作');
INSERT INTO `sys_dict_data`
VALUES (24, 7, '强退', '7', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '强退操作');
INSERT INTO `sys_dict_data`
VALUES (25, 8, '生成代码', '8', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '生成操作');
INSERT INTO `sys_dict_data`
VALUES (26, 9, '清空数据', '9', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '清空操作');
INSERT INTO `sys_dict_data`
VALUES (27, 1, '成功', '0', 'sys_common_status', '', 'primary', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '正常状态');
INSERT INTO `sys_dict_data`
VALUES (28, 2, '失败', '1', 'sys_common_status', '', 'danger', 'N', '0', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '停用状态');
INSERT INTO `sys_dict_data`
VALUES (100, 0, 'OCR识别', '0', 'bus_pic_type', NULL, NULL, 'N', '0', 'admin', '2020-09-08 11:41:13', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (101, 1, '识景识物', '1', 'bus_pic_type', NULL, NULL, 'N', '0', 'admin', '2020-09-08 11:41:44', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (102, 1, '滴滴快车', '1', 'bus_travel_car', NULL, NULL, 'N', '0', 'admin', '2020-09-23 10:05:33', 'admin',
        '2020-11-13 14:11:07', NULL);
INSERT INTO `sys_dict_data`
VALUES (103, 2, '滴滴专车', '2', 'bus_travel_car', NULL, NULL, 'N', '0', 'admin', '2020-09-23 10:05:42', 'admin',
        '2020-11-13 06:31:42', NULL);
INSERT INTO `sys_dict_data`
VALUES (104, 1, '处理完成', '1', 'bus_invoice_status', NULL, NULL, 'N', '0', 'admin', '2020-09-23 14:46:48', '', NULL,
        NULL);
INSERT INTO `sys_dict_data`
VALUES (105, 2, '未处理', '2', 'bus_invoice_status', NULL, NULL, 'N', '0', 'admin', '2020-09-23 14:46:55', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (106, 3, '处理失败', '3', 'bus_invoice_status', NULL, NULL, 'N', '0', 'admin', '2020-09-23 14:47:05', '', NULL,
        NULL);
INSERT INTO `sys_dict_data`
VALUES (107, 4, '处理中', '4', 'bus_invoice_status', NULL, NULL, 'N', '0', 'admin', '2020-09-23 15:12:19', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (108, 1, '普通', '1', 'bus_video_type', NULL, NULL, 'N', '0', 'admin', '2020-10-10 19:02:04', '', NULL,
        '普通的视频（适应横版16：9的封面）');
INSERT INTO `sys_dict_data`
VALUES (109, 2, '带制作', '2', 'bus_video_type', NULL, NULL, 'N', '0', 'admin', '2020-10-10 19:07:46', '', NULL,
        '带制作视频（使用竖版封面突出重要性）');
INSERT INTO `sys_dict_data`
VALUES (110, 1, '广播/电视', '1', 'pub_unit_type', NULL, NULL, 'N', '0', 'admin', '2020-11-24 06:15:12', '', NULL,
        '地区级别（或以上）的音（视）频节目制作单位');
INSERT INTO `sys_dict_data`
VALUES (111, 2, '报纸/杂志', '2', 'pub_unit_type', NULL, NULL, 'N', '0', 'admin', '2020-11-24 06:16:43', '', NULL,
        '事业、市政、企业单位（行政或商业）以纸张为载体的媒体');
INSERT INTO `sys_dict_data`
VALUES (112, 3, '自媒体', '3', 'pub_unit_type', NULL, NULL, 'N', '0', 'admin', '2020-11-24 06:20:30', 'admin',
        '2020-11-24 06:20:52', '公众号、视频号、音频号等由中小型企业、公益组织或个人运营的私域流量主体');
INSERT INTO `sys_dict_data`
VALUES (113, 0, '未定义', '0', 'person_sex', NULL, NULL, 'N', '0', 'admin', '2021-01-17 15:08:52', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (114, 1, '男', '1', 'person_sex', NULL, NULL, 'N', '0', 'admin', '2021-01-17 15:09:00', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (115, 2, '女', '2', 'person_sex', NULL, NULL, 'N', '0', 'admin', '2021-01-17 15:09:06', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (116, 2, '相馆画廊', '2', 'bus_pic_type', NULL, NULL, 'N', '0', 'admin', '2021-02-21 09:13:43', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (117, 0, '高质素材', '0', 'material_type', NULL, NULL, 'N', '0', 'admin', '2021-02-21 09:30:29', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (118, 1, '普通素材', '1', 'material_type', NULL, NULL, 'N', '0', 'admin', '2021-02-21 09:30:57', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (119, 0, '已归档', '0', 'material_merge', NULL, NULL, 'N', '0', 'admin', '2021-02-21 14:49:00', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (120, 1, '未合并', '1', 'material_merge', NULL, NULL, 'N', '0', 'admin', '2021-02-21 14:58:47', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (121, 1, '初入库', '1', 'material_status', NULL, NULL, 'N', '0', 'admin', '2021-02-21 16:24:25', '', NULL,
        '刚入库，仅帧率处理完成，id、尺寸、时长、创建时间、类别，未打分，未打标签，未转码');
INSERT INTO `sys_dict_data`
VALUES (122, 2, '正在处理', '2', 'material_status', NULL, NULL, 'N', '0', 'admin', '2021-02-21 16:26:49', 'admin',
        '2021-02-21 16:27:52', '筛选（手动删除拍得不好的片段），截取（手动掐头去尾）操作后，提交给服务器进行切片处理');
INSERT INTO `sys_dict_data`
VALUES (123, 0, '处理完毕', '0', 'material_status', NULL, NULL, 'N', '0', 'admin', '2021-02-21 16:40:02', '', NULL,
        '通过筛选并打标签同时完成截图、截取和转码');
INSERT INTO `sys_dict_data`
VALUES (124, 0, '已上架', '0', 'material_public', NULL, NULL, 'N', '0', 'admin', '2021-02-22 03:29:04', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (125, 1, '未发布', '1', 'material_public', NULL, NULL, 'N', '0', 'admin', '2021-02-22 03:29:39', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (126, 0, '有版权', '0', 'material_copyright', NULL, NULL, 'N', '0', 'admin', '2021-02-22 03:43:22', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (127, 1, '无版权', '1', 'material_copyright', NULL, NULL, 'N', '0', 'admin', '2021-02-22 03:43:32', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (128, 3, '准备处理', '3', 'material_status', NULL, NULL, 'N', '0', 'admin', '2021-02-22 10:18:21', 'admin',
        '2021-02-22 10:19:14', '入库后手动将出入点等参数调整完毕，等待裁剪和截图处理');
INSERT INTO `sys_dict_data`
VALUES (129, 0, '纯音乐', '0', 'audio_classify', NULL, NULL, 'N', '0', 'admin', '2021-02-28 08:16:10', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (130, 1, '歌曲', '1', 'audio_classify', NULL, NULL, 'N', '0', 'admin', '2021-02-28 08:16:22', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (131, 0, '处理完毕', '0', 'mat_audio_status', NULL, NULL, 'N', '0', 'admin', '2021-02-28 08:23:52', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (132, 1, '待处理', '1', 'mat_audio_status', NULL, NULL, 'N', '0', 'admin', '2021-02-28 08:24:03', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (133, 2, '无需处理', '2', 'mat_audio_status', NULL, NULL, 'N', '0', 'admin', '2021-02-28 08:24:11', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (134, 3, '正在处理', '3', 'mat_audio_status', NULL, NULL, 'N', '0', 'admin', '2021-03-02 09:06:54', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (135, 0, '哔哩哔哩', '0', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:20:51', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (136, 1, '今日头条', '1', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:21:03', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (137, 2, '抖音', '2', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:21:12', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (138, 3, '西瓜视频', '3', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:21:21', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (139, 4, 'YouTube', '4', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:21:29', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (140, 5, '知乎', '5', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:22:06', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (141, 6, '小红书', '6', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:22:17', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (142, 7, '快手', '7', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:22:27', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (143, 8, 'Acfun', '8', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:22:49', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (144, 9, '网易云音乐', '9', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:23:05', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (145, 10, '豆瓣', '10', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:23:34', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (146, 11, '微博', '11', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:23:52', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (147, 12, '新片场', '12', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:24:34', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (148, 13, '图虫', '13', 'media_platform', NULL, NULL, 'N', '0', 'admin', '2021-03-26 10:24:50', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (149, 0, '平台', '0', 'promotion_type', NULL, NULL, 'N', '0', 'admin', '2021-04-08 09:28:32', '', NULL, NULL);
INSERT INTO `sys_dict_data`
VALUES (150, 1, '栏目', '1', 'promotion_type', NULL, NULL, 'N', '0', 'admin', '2021-04-08 09:28:40', '', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for sys_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_type`;
CREATE TABLE `sys_dict_type`
(
    `dict_id`     bigint NOT NULL AUTO_INCREMENT COMMENT '字典主键',
    `dict_name`   varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典名称',
    `dict_type`   varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典类型',
    `status`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '状态（0正常 1停用）',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`      varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`dict_id`) USING BTREE,
    UNIQUE KEY `dict_type` (`dict_type`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 116
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='字典类型表';

-- ----------------------------
-- Records of sys_dict_type
-- ----------------------------
BEGIN;
INSERT INTO `sys_dict_type`
VALUES (1, '用户性别', 'sys_user_sex', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '用户性别列表');
INSERT INTO `sys_dict_type`
VALUES (2, '菜单状态', 'sys_show_hide', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '菜单状态列表');
INSERT INTO `sys_dict_type`
VALUES (3, '系统开关', 'sys_normal_disable', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '系统开关列表');
INSERT INTO `sys_dict_type`
VALUES (4, '任务状态', 'sys_job_status', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '任务状态列表');
INSERT INTO `sys_dict_type`
VALUES (5, '任务分组', 'sys_job_group', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '任务分组列表');
INSERT INTO `sys_dict_type`
VALUES (6, '系统是否', 'sys_yes_no', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '系统是否列表');
INSERT INTO `sys_dict_type`
VALUES (7, '通知类型', 'sys_notice_type', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '通知类型列表');
INSERT INTO `sys_dict_type`
VALUES (8, '通知状态', 'sys_notice_status', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '通知状态列表');
INSERT INTO `sys_dict_type`
VALUES (9, '操作类型', 'sys_oper_type', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '操作类型列表');
INSERT INTO `sys_dict_type`
VALUES (10, '系统状态', 'sys_common_status', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '登录状态列表');
INSERT INTO `sys_dict_type`
VALUES (100, '识别类型', 'bus_pic_type', '0', 'admin', '2020-09-08 11:40:33', 'admin', '2021-02-21 02:15:15', '便于后期分类');
INSERT INTO `sys_dict_type`
VALUES (101, '滴滴车型', 'bus_travel_car', '0', 'admin', '2020-09-23 10:04:55', 'admin', '2021-02-21 02:14:47', '滴滴打车乘车类型');
INSERT INTO `sys_dict_type`
VALUES (102, '处理状态', 'bus_invoice_status', '0', 'admin', '2020-09-23 14:46:31', 'admin', '2021-02-21 02:14:31',
        '发票处理的生命周期');
INSERT INTO `sys_dict_type`
VALUES (103, '视频种类', 'bus_video_type', '0', 'admin', '2020-10-10 18:50:30', '', NULL, '是否为带制作视频');
INSERT INTO `sys_dict_type`
VALUES (104, '视频上架', 'bus_video_onload', '0', 'admin', '2020-10-10 18:53:03', '', NULL, '管理客户端能够看到的视频');
INSERT INTO `sys_dict_type`
VALUES (105, '媒体类型', 'pub_unit_type', '0', 'admin', '2020-11-24 06:13:33', 'admin', '2021-01-17 15:07:35', '常见的媒体形式');
INSERT INTO `sys_dict_type`
VALUES (106, '人物性别', 'person_sex', '0', 'admin', '2021-01-17 15:08:19', '', NULL, '适用于多人脉层的属性之一');
INSERT INTO `sys_dict_type`
VALUES (107, '素材类型', 'material_type', '0', 'admin', '2021-02-21 02:14:08', 'admin', '2021-02-21 09:14:11', '为视频素材分类');
INSERT INTO `sys_dict_type`
VALUES (108, '素材状态', 'material_status', '0', 'admin', '2021-02-21 09:37:27', 'admin', '2021-02-21 09:37:44',
        '视频素材处理中的必要阶段');
INSERT INTO `sys_dict_type`
VALUES (109, '素材版权', 'material_copyright', '0', 'admin', '2021-02-21 09:38:54', '', NULL, '当前素材是否能够公开给所有用户');
INSERT INTO `sys_dict_type`
VALUES (110, '素材上架', 'material_public', '0', 'admin', '2021-02-21 09:40:13', '', NULL, '是否上架公开给所有用户查看');
INSERT INTO `sys_dict_type`
VALUES (111, '素材归档', 'material_merge', '0', 'admin', '2021-02-21 09:41:01', 'admin', '2021-02-21 14:48:37',
        '素材是否已经合并归档');
INSERT INTO `sys_dict_type`
VALUES (112, '音频类型', 'audio_classify', '0', 'admin', '2021-02-28 08:14:50', 'admin', '2021-02-28 08:15:34',
        '入库的音乐类型，目前只入这两种和视频剪辑相关联的');
INSERT INTO `sys_dict_type`
VALUES (113, '音频素材状态', 'mat_audio_status', '0', 'admin', '2021-02-28 08:23:30', '', NULL, '音频素材直接通过上传接口入库');
INSERT INTO `sys_dict_type`
VALUES (114, '媒体平台', 'media_platform', '0', 'admin', '2021-03-26 10:20:16', '', NULL, '国内外常见的UGC平台');
INSERT INTO `sys_dict_type`
VALUES (115, '推广类型', 'promotion_type', '0', 'admin', '2021-04-08 09:27:52', 'admin', '2021-04-08 09:28:08',
        '展示在官网的小众类型');
COMMIT;

-- ----------------------------
-- Table structure for sys_job
-- ----------------------------
DROP TABLE IF EXISTS `sys_job`;
CREATE TABLE `sys_job`
(
    `job_id`          bigint                                                        NOT NULL AUTO_INCREMENT COMMENT '任务ID',
    `job_name`        varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL DEFAULT '' COMMENT '任务名称',
    `job_group`       varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL DEFAULT 'DEFAULT' COMMENT '任务组名',
    `invoke_target`   varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调用目标字符串',
    `cron_expression` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci          DEFAULT '' COMMENT 'cron执行表达式',
    `misfire_policy`  varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci           DEFAULT '3' COMMENT '计划执行错误策略（1立即执行 2执行一次 3放弃执行）',
    `concurrent`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci               DEFAULT '1' COMMENT '是否并发执行（0允许 1禁止）',
    `status`          char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci               DEFAULT '0' COMMENT '状态（0正常 1暂停）',
    `create_by`       varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci           DEFAULT '' COMMENT '创建者',
    `create_time`     datetime                                                               DEFAULT NULL COMMENT '创建时间',
    `update_by`       varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci           DEFAULT '' COMMENT '更新者',
    `update_time`     datetime                                                               DEFAULT NULL COMMENT '更新时间',
    `remark`          varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci          DEFAULT '' COMMENT '备注信息',
    PRIMARY KEY (`job_id`, `job_name`, `job_group`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 100
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='定时任务调度表';

-- ----------------------------
-- Records of sys_job
-- ----------------------------
BEGIN;
INSERT INTO `sys_job`
VALUES (1, '系统默认（无参）', 'DEFAULT', 'ryTask.ryNoParams', '0/10 * * * * ?', '3', '1', '1', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_job`
VALUES (2, '系统默认（有参）', 'DEFAULT', 'ryTask.ryParams(\'ry\')', '0/15 * * * * ?', '3', '1', '1', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_job`
VALUES (3, '系统默认（多参）', 'DEFAULT', 'ryTask.ryMultipleParams(\'ry\', true, 2000L, 316.50D, 100)', '0/20 * * * * ?', '3',
        '1', '1', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
COMMIT;

-- ----------------------------
-- Table structure for sys_job_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_job_log`;
CREATE TABLE `sys_job_log`
(
    `job_log_id`     bigint                                                        NOT NULL AUTO_INCREMENT COMMENT '任务日志ID',
    `job_name`       varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL COMMENT '任务名称',
    `job_group`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL COMMENT '任务组名',
    `invoke_target`  varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调用目标字符串',
    `job_message`    varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '日志信息',
    `status`         char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci       DEFAULT '0' COMMENT '执行状态（0正常 1失败）',
    `exception_info` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '异常信息',
    `create_time`    datetime                                                       DEFAULT NULL COMMENT '创建时间',
    PRIMARY KEY (`job_log_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 3
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='定时任务调度日志表';

-- ----------------------------
-- Records of sys_job_log
-- ----------------------------
BEGIN;
INSERT INTO `sys_job_log`
VALUES (1, '系统默认（无参）', 'DEFAULT', 'ryTask.ryNoParams', '系统默认（无参） 总共耗时：4毫秒', '0', '', '2021-03-10 08:02:30');
INSERT INTO `sys_job_log`
VALUES (2, '系统默认（无参）', 'DEFAULT', 'ryTask.ryNoParams', '系统默认（无参） 总共耗时：0毫秒', '0', '', '2021-03-10 09:17:54');
COMMIT;

-- ----------------------------
-- Table structure for sys_logininfor
-- ----------------------------
DROP TABLE IF EXISTS `sys_logininfor`;
CREATE TABLE `sys_logininfor`
(
    `info_id`        bigint NOT NULL AUTO_INCREMENT COMMENT '访问ID',
    `user_name`      varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '用户账号',
    `ipaddr`         varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '登录IP地址',
    `login_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '登录地点',
    `browser`        varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '浏览器类型',
    `os`             varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '操作系统',
    `status`         char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '登录状态（0成功 1失败）',
    `msg`            varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '提示消息',
    `login_time`     datetime                                                      DEFAULT NULL COMMENT '访问时间',
    PRIMARY KEY (`info_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 2
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='系统访问记录';

-- ----------------------------
-- Records of sys_logininfor
-- ----------------------------
BEGIN;
INSERT INTO `sys_logininfor`
VALUES (1, 'admin', '127.0.0.1', '内网IP', 'Chrome 9', 'Mac OS X', '0', '登录成功', '2021-06-11 10:53:27');
COMMIT;

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`
(
    `menu_id`     bigint                                                       NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
    `menu_name`   varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单名称',
    `parent_id`   bigint                                                        DEFAULT '0' COMMENT '父菜单ID',
    `order_num`   int                                                           DEFAULT '0' COMMENT '显示顺序',
    `path`        varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '路由地址',
    `component`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '组件路径',
    `is_frame`    int                                                           DEFAULT '1' COMMENT '是否为外链（0是 1否）',
    `is_cache`    int(1) unsigned zerofill                                      DEFAULT NULL COMMENT '是否缓存（0缓存 1不缓存）',
    `menu_type`   char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '' COMMENT '菜单类型（M目录 C菜单 F按钮）',
    `visible`     char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '菜单状态（0显示 1隐藏）',
    `status`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '菜单状态（0正常 1停用）',
    `perms`       varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '权限标识',
    `icon`        varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '#' COMMENT '菜单图标',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`      varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '备注',
    PRIMARY KEY (`menu_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 2089
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='菜单权限表';

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
BEGIN;
INSERT INTO `sys_menu`
VALUES (1, '系统管理', 0, 4, 'system', NULL, 1, NULL, 'M', '0', '0', '', 'system', 'admin', '2018-03-16 11:33:00', 'admin',
        '2020-09-08 11:57:37', '系统管理目录');
INSERT INTO `sys_menu`
VALUES (2, '系统监控', 0, 2, 'monitor', NULL, 1, NULL, 'M', '0', '0', '', 'monitor', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '系统监控目录');
INSERT INTO `sys_menu`
VALUES (3, '系统工具', 0, 3, 'tool', NULL, 1, NULL, 'M', '0', '0', '', 'tool', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '系统工具目录');
INSERT INTO `sys_menu`
VALUES (4, '若依官网', 0, 1, 'http://ruoyi.vip', NULL, 0, NULL, 'M', '1', '0', '', 'guide', 'admin', '2018-03-16 11:33:00',
        'admin', '2020-12-29 00:56:14', '若依官网地址');
INSERT INTO `sys_menu`
VALUES (100, '用户管理', 1, 1, 'user', 'system/user/index', 1, NULL, 'C', '0', '0', 'system:user:list', 'user', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '用户管理菜单');
INSERT INTO `sys_menu`
VALUES (101, '角色管理', 1, 2, 'role', 'system/role/index', 1, NULL, 'C', '0', '0', 'system:role:list', 'peoples', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '角色管理菜单');
INSERT INTO `sys_menu`
VALUES (102, '菜单管理', 1, 3, 'menu', 'system/menu/index', 1, NULL, 'C', '0', '0', 'system:menu:list', 'tree-table',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '菜单管理菜单');
INSERT INTO `sys_menu`
VALUES (103, '部门管理', 1, 4, 'dept', 'system/dept/index', 1, NULL, 'C', '0', '0', 'system:dept:list', 'tree', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '部门管理菜单');
INSERT INTO `sys_menu`
VALUES (104, '岗位管理', 1, 5, 'post', 'system/post/index', 1, NULL, 'C', '0', '0', 'system:post:list', 'post', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '岗位管理菜单');
INSERT INTO `sys_menu`
VALUES (105, '字典管理', 1, 6, 'dict', 'system/dict/index', 1, NULL, 'C', '0', '0', 'system:dict:list', 'dict', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '字典管理菜单');
INSERT INTO `sys_menu`
VALUES (106, '参数设置', 1, 7, 'config', 'system/config/index', 1, NULL, 'C', '0', '0', 'system:config:list', 'edit',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '参数设置菜单');
INSERT INTO `sys_menu`
VALUES (107, '通知公告', 1, 8, 'notice', 'system/notice/index', 1, NULL, 'C', '0', '0', 'system:notice:list', 'message',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '通知公告菜单');
INSERT INTO `sys_menu`
VALUES (108, '日志管理', 1, 9, 'log', '', 1, 0, 'M', '0', '0', '', 'log', 'admin', '2018-03-16 11:33:00', 'ry',
        '2018-03-16 11:33:00', '日志管理菜单');
INSERT INTO `sys_menu`
VALUES (109, '在线用户', 2, 1, 'online', 'monitor/online/index', 1, NULL, 'C', '0', '0', 'monitor:online:list', 'online',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '在线用户菜单');
INSERT INTO `sys_menu`
VALUES (110, '定时任务', 2, 2, 'job', 'monitor/job/index', 1, NULL, 'C', '0', '0', 'monitor:job:list', 'job', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '定时任务菜单');
INSERT INTO `sys_menu`
VALUES (111, '数据监控', 2, 3, 'druid', 'monitor/druid/index', 1, NULL, 'C', '0', '0', 'monitor:druid:list', 'druid',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '数据监控菜单');
INSERT INTO `sys_menu`
VALUES (112, '服务监控', 2, 4, 'server', 'monitor/server/index', 1, NULL, 'C', '0', '0', 'monitor:server:list', 'server',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '服务监控菜单');
INSERT INTO `sys_menu`
VALUES (113, '表单构建', 3, 1, 'build', 'tool/build/index', 1, NULL, 'C', '0', '0', 'tool:build:list', 'build', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '表单构建菜单');
INSERT INTO `sys_menu`
VALUES (114, '代码生成', 3, 2, 'gen', 'tool/gen/index', 1, NULL, 'C', '0', '0', 'tool:gen:list', 'code', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '代码生成菜单');
INSERT INTO `sys_menu`
VALUES (115, '系统接口', 3, 3, 'swagger', 'tool/swagger/index', 1, 0, 'C', '0', '0', 'tool:swagger:list', 'swagger',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '系统接口菜单');
INSERT INTO `sys_menu`
VALUES (500, '操作日志', 108, 1, 'operlog', 'monitor/operlog/index', 1, 0, 'C', '0', '0', 'monitor:operlog:list', 'form',
        'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '操作日志菜单');
INSERT INTO `sys_menu`
VALUES (501, '登录日志', 108, 2, 'logininfor', 'monitor/logininfor/index', 1, NULL, 'C', '0', '0',
        'monitor:logininfor:list', 'logininfor', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '登录日志菜单');
INSERT INTO `sys_menu`
VALUES (1001, '用户查询', 100, 1, '', '', 1, NULL, 'F', '0', '0', 'system:user:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1002, '用户新增', 100, 2, '', '', 1, NULL, 'F', '0', '0', 'system:user:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1003, '用户修改', 100, 3, '', '', 1, NULL, 'F', '0', '0', 'system:user:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1004, '用户删除', 100, 4, '', '', 1, NULL, 'F', '0', '0', 'system:user:remove', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1005, '用户导出', 100, 5, '', '', 1, NULL, 'F', '0', '0', 'system:user:export', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1006, '用户导入', 100, 6, '', '', 1, NULL, 'F', '0', '0', 'system:user:import', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1007, '重置密码', 100, 7, '', '', 1, NULL, 'F', '0', '0', 'system:user:resetPwd', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1008, '角色查询', 101, 1, '', '', 1, NULL, 'F', '0', '0', 'system:role:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1009, '角色新增', 101, 2, '', '', 1, NULL, 'F', '0', '0', 'system:role:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1010, '角色修改', 101, 3, '', '', 1, NULL, 'F', '0', '0', 'system:role:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1011, '角色删除', 101, 4, '', '', 1, NULL, 'F', '0', '0', 'system:role:remove', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1012, '角色导出', 101, 5, '', '', 1, NULL, 'F', '0', '0', 'system:role:export', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1013, '菜单查询', 102, 1, '', '', 1, NULL, 'F', '0', '0', 'system:menu:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1014, '菜单新增', 102, 2, '', '', 1, NULL, 'F', '0', '0', 'system:menu:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1015, '菜单修改', 102, 3, '', '', 1, NULL, 'F', '0', '0', 'system:menu:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1016, '菜单删除', 102, 4, '', '', 1, NULL, 'F', '0', '0', 'system:menu:remove', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1017, '部门查询', 103, 1, '', '', 1, NULL, 'F', '0', '0', 'system:dept:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1018, '部门新增', 103, 2, '', '', 1, NULL, 'F', '0', '0', 'system:dept:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1019, '部门修改', 103, 3, '', '', 1, NULL, 'F', '0', '0', 'system:dept:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1020, '部门删除', 103, 4, '', '', 1, NULL, 'F', '0', '0', 'system:dept:remove', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1021, '岗位查询', 104, 1, '', '', 1, NULL, 'F', '0', '0', 'system:post:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1022, '岗位新增', 104, 2, '', '', 1, NULL, 'F', '0', '0', 'system:post:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1023, '岗位修改', 104, 3, '', '', 1, NULL, 'F', '0', '0', 'system:post:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1024, '岗位删除', 104, 4, '', '', 1, NULL, 'F', '0', '0', 'system:post:remove', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1025, '岗位导出', 104, 5, '', '', 1, NULL, 'F', '0', '0', 'system:post:export', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1026, '字典查询', 105, 1, '#', '', 1, NULL, 'F', '0', '0', 'system:dict:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1027, '字典新增', 105, 2, '#', '', 1, NULL, 'F', '0', '0', 'system:dict:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1028, '字典修改', 105, 3, '#', '', 1, NULL, 'F', '0', '0', 'system:dict:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1029, '字典删除', 105, 4, '#', '', 1, NULL, 'F', '0', '0', 'system:dict:remove', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1030, '字典导出', 105, 5, '#', '', 1, NULL, 'F', '0', '0', 'system:dict:export', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1031, '参数查询', 106, 1, '#', '', 1, NULL, 'F', '0', '0', 'system:config:query', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1032, '参数新增', 106, 2, '#', '', 1, NULL, 'F', '0', '0', 'system:config:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1033, '参数修改', 106, 3, '#', '', 1, NULL, 'F', '0', '0', 'system:config:edit', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1034, '参数删除', 106, 4, '#', '', 1, NULL, 'F', '0', '0', 'system:config:remove', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1035, '参数导出', 106, 5, '#', '', 1, NULL, 'F', '0', '0', 'system:config:export', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1036, '公告查询', 107, 1, '#', '', 1, NULL, 'F', '0', '0', 'system:notice:query', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1037, '公告新增', 107, 2, '#', '', 1, NULL, 'F', '0', '0', 'system:notice:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1038, '公告修改', 107, 3, '#', '', 1, NULL, 'F', '0', '0', 'system:notice:edit', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1039, '公告删除', 107, 4, '#', '', 1, NULL, 'F', '0', '0', 'system:notice:remove', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1040, '操作查询', 500, 1, '#', '', 1, NULL, 'F', '0', '0', 'monitor:operlog:query', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1041, '操作删除', 500, 2, '#', '', 1, NULL, 'F', '0', '0', 'monitor:operlog:remove', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1042, '日志导出', 500, 4, '#', '', 1, NULL, 'F', '0', '0', 'monitor:operlog:export', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1043, '登录查询', 501, 1, '#', '', 1, NULL, 'F', '0', '0', 'monitor:logininfor:query', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1044, '登录删除', 501, 2, '#', '', 1, NULL, 'F', '0', '0', 'monitor:logininfor:remove', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1045, '日志导出', 501, 3, '#', '', 1, NULL, 'F', '0', '0', 'monitor:logininfor:export', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1046, '在线查询', 109, 1, '#', '', 1, NULL, 'F', '0', '0', 'monitor:online:query', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1047, '批量强退', 109, 2, '#', '', 1, NULL, 'F', '0', '0', 'monitor:online:batchLogout', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1048, '单条强退', 109, 3, '#', '', 1, NULL, 'F', '0', '0', 'monitor:online:forceLogout', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1049, '任务查询', 110, 1, '#', '', 1, NULL, 'F', '0', '0', 'monitor:job:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1050, '任务新增', 110, 2, '#', '', 1, NULL, 'F', '0', '0', 'monitor:job:add', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1051, '任务修改', 110, 3, '#', '', 1, NULL, 'F', '0', '0', 'monitor:job:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1052, '任务删除', 110, 4, '#', '', 1, NULL, 'F', '0', '0', 'monitor:job:remove', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1053, '状态修改', 110, 5, '#', '', 1, NULL, 'F', '0', '0', 'monitor:job:changeStatus', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1054, '任务导出', 110, 7, '#', '', 1, NULL, 'F', '0', '0', 'monitor:job:export', '#', 'admin',
        '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1055, '生成查询', 114, 1, '#', '', 1, NULL, 'F', '0', '0', 'tool:gen:query', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1056, '生成修改', 114, 2, '#', '', 1, NULL, 'F', '0', '0', 'tool:gen:edit', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1057, '生成删除', 114, 3, '#', '', 1, NULL, 'F', '0', '0', 'tool:gen:remove', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1058, '导入代码', 114, 2, '#', '', 1, NULL, 'F', '0', '0', 'tool:gen:import', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1059, '预览代码', 114, 4, '#', '', 1, NULL, 'F', '0', '0', 'tool:gen:preview', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (1060, '生成代码', 114, 5, '#', '', 1, NULL, 'F', '0', '0', 'tool:gen:code', '#', 'admin', '2018-03-16 11:33:00',
        'ry', '2018-03-16 11:33:00', '');
INSERT INTO `sys_menu`
VALUES (2006, '媒体工具', 0, 5, 'business', NULL, 1, NULL, 'M', '0', '0', NULL, 'edit', 'admin', '2020-09-08 11:55:22', '',
        NULL, '');
INSERT INTO `sys_menu`
VALUES (2013, '频道管理', 2051, 1, 'channel', 'business/channel/index', 1, NULL, 'C', '0', '0', 'business:channel:list',
        'star', 'admin', '2018-03-01 00:00:00', 'admin', '2021-02-08 10:39:46', '频道管理菜单');
INSERT INTO `sys_menu`
VALUES (2014, '频道管理查询', 2013, 1, '#', '', 1, NULL, 'F', '0', '0', 'business:channel:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2015, '频道管理新增', 2013, 2, '#', '', 1, NULL, 'F', '0', '0', 'business:channel:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2016, '频道管理修改', 2013, 3, '#', '', 1, NULL, 'F', '0', '0', 'business:channel:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2017, '频道管理删除', 2013, 4, '#', '', 1, NULL, 'F', '0', '0', 'business:channel:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2018, '频道管理导出', 2013, 5, '#', '', 1, NULL, 'F', '0', '0', 'business:channel:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2019, '视频管理', 2051, 1, 'video', 'business/video/index', 1, NULL, 'C', '0', '0', 'business:video:list', 'video',
        'admin', '2018-03-01 00:00:00', 'admin', '2021-02-08 10:39:54', '视频管理菜单');
INSERT INTO `sys_menu`
VALUES (2020, '视频管理查询', 2019, 1, '#', '', 1, NULL, 'F', '0', '0', 'business:video:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2021, '视频管理新增', 2019, 2, '#', '', 1, NULL, 'F', '0', '0', 'business:video:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2022, '视频管理修改', 2019, 3, '#', '', 1, NULL, 'F', '0', '0', 'business:video:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2023, '视频管理删除', 2019, 4, '#', '', 1, NULL, 'F', '0', '0', 'business:video:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2024, '视频管理导出', 2019, 5, '#', '', 1, NULL, 'F', '0', '0', 'business:video:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2025, '素材矩阵', 0, 6, 'material', NULL, 1, NULL, 'M', '0', '0', NULL, 'example', 'admin', '2020-10-10 12:12:35',
        '', NULL, '');
INSERT INTO `sys_menu`
VALUES (2026, '主页轮播图', 2006, 1, 'swiper', 'business/swiper/index', 1, NULL, 'C', '0', '0', 'business:swiper:list',
        'textarea', 'admin', '2018-03-01 00:00:00', 'admin', '2021-04-22 03:43:05', '主页轮播图菜单');
INSERT INTO `sys_menu`
VALUES (2027, '主页轮播图查询', 2026, 1, '#', '', 1, NULL, 'F', '0', '0', 'business:swiper:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2028, '主页轮播图新增', 2026, 2, '#', '', 1, NULL, 'F', '0', '0', 'business:swiper:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2029, '主页轮播图修改', 2026, 3, '#', '', 1, NULL, 'F', '0', '0', 'business:swiper:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2030, '主页轮播图删除', 2026, 4, '#', '', 1, NULL, 'F', '0', '0', 'business:swiper:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2031, '主页轮播图导出', 2026, 5, '#', '', 1, NULL, 'F', '0', '0', 'business:swiper:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2032, '分发矩阵', 0, 7, 'publish', NULL, 1, NULL, 'M', '0', '0', '', 'upload', 'admin', '2020-11-24 06:23:59',
        'admin', '2021-03-01 08:43:16', '');
INSERT INTO `sys_menu`
VALUES (2033, '媒体单位', 2032, 1, 'unit', 'publish/unit/index', 1, NULL, 'C', '0', '0', 'publish:unit:list', 'people',
        'admin', '2018-03-01 00:00:00', 'admin', '2020-11-24 07:04:04', '媒体单位菜单');
INSERT INTO `sys_menu`
VALUES (2034, '媒体单位查询', 2033, 1, '#', '', 1, NULL, 'F', '0', '0', 'publish:unit:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2035, '媒体单位新增', 2033, 2, '#', '', 1, NULL, 'F', '0', '0', 'publish:unit:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2036, '媒体单位修改', 2033, 3, '#', '', 1, NULL, 'F', '0', '0', 'publish:unit:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2037, '媒体单位删除', 2033, 4, '#', '', 1, NULL, 'F', '0', '0', 'publish:unit:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2038, '媒体单位导出', 2033, 5, '#', '', 1, NULL, 'F', '0', '0', 'publish:unit:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2045, '作品管理', 2052, 1, 'work', 'create/work/index', 1, NULL, 'C', '0', '0', 'create:work:list', 'dict', 'admin',
        '2018-03-01 00:00:00', 'admin', '2021-02-08 13:46:59', '作品管理菜单');
INSERT INTO `sys_menu`
VALUES (2046, '作品管理查询', 2045, 1, '#', '', 1, NULL, 'F', '0', '0', 'create:work:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2047, '作品管理新增', 2045, 2, '#', '', 1, NULL, 'F', '0', '0', 'create:work:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2048, '作品管理修改', 2045, 3, '#', '', 1, NULL, 'F', '0', '0', 'create:work:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2049, '作品管理删除', 2045, 4, '#', '', 1, NULL, 'F', '0', '0', 'create:work:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2050, '作品管理导出', 2045, 5, '#', '', 1, NULL, 'F', '0', '0', 'create:work:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2051, '视频矩阵', 0, 8, 'video', NULL, 1, NULL, 'M', '0', '0', '', 'build', 'admin', '2021-02-08 10:38:54', 'admin',
        '2021-02-08 10:39:17', '');
INSERT INTO `sys_menu`
VALUES (2052, '创作矩阵', 0, 9, 'create', NULL, 1, NULL, 'M', '0', '0', NULL, 'post', 'admin', '2021-02-08 10:41:26', '',
        NULL, '');
INSERT INTO `sys_menu`
VALUES (2053, '篇章管理', 2052, 1, 'chapter', 'create/chapter/index', 1, NULL, 'C', '0', '0', 'create:chapter:list',
        'nested', 'admin', '2018-03-01 00:00:00', 'admin', '2021-02-08 13:47:08', '篇章管理菜单');
INSERT INTO `sys_menu`
VALUES (2054, '篇章管理查询', 2053, 1, '#', '', 1, NULL, 'F', '0', '0', 'create:chapter:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2055, '篇章管理新增', 2053, 2, '#', '', 1, NULL, 'F', '0', '0', 'create:chapter:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2056, '篇章管理修改', 2053, 3, '#', '', 1, NULL, 'F', '0', '0', 'create:chapter:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2057, '篇章管理删除', 2053, 4, '#', '', 1, NULL, 'F', '0', '0', 'create:chapter:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2058, '篇章管理导出', 2053, 5, '#', '', 1, NULL, 'F', '0', '0', 'create:chapter:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2059, '视频素材', 2025, 1, 'clip', 'material/clip/index', 1, NULL, 'C', '0', '0', 'material:clip:list',
        'documentation', 'admin', '2018-03-01 00:00:00', 'admin', '2021-02-22 03:05:34', '视频素材菜单');
INSERT INTO `sys_menu`
VALUES (2060, '视频素材查询', 2059, 1, '#', '', 1, NULL, 'F', '0', '0', 'material:clip:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2061, '视频素材新增', 2059, 2, '#', '', 1, NULL, 'F', '0', '0', 'material:clip:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2062, '视频素材修改', 2059, 3, '#', '', 1, NULL, 'F', '0', '0', 'material:clip:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2063, '视频素材删除', 2059, 4, '#', '', 1, NULL, 'F', '0', '0', 'material:clip:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2064, '视频素材导出', 2059, 5, '#', '', 1, NULL, 'F', '0', '0', 'material:clip:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2065, '音频素材', 2025, 1, 'audio', 'material/audio/index', 1, NULL, 'C', '0', '0', 'material:audio:list', 'wechat',
        'admin', '2018-03-01 00:00:00', 'admin', '2021-03-01 07:59:00', '音频素材菜单');
INSERT INTO `sys_menu`
VALUES (2066, '音频素材查询', 2065, 1, '#', '', 1, NULL, 'F', '0', '0', 'system:audio:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2067, '音频素材新增', 2065, 2, '#', '', 1, NULL, 'F', '0', '0', 'system:audio:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2068, '音频素材修改', 2065, 3, '#', '', 1, NULL, 'F', '0', '0', 'system:audio:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2069, '音频素材删除', 2065, 4, '#', '', 1, NULL, 'F', '0', '0', 'system:audio:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2070, '音频素材导出', 2065, 5, '#', '', 1, NULL, 'F', '0', '0', 'system:audio:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2071, '图片素材', 2025, 1, 'image', 'material/image/index', 1, NULL, 'C', '0', '0', 'material:image:list',
        'component', 'admin', '2018-03-01 00:00:00', 'admin', '2021-03-09 03:42:04', '图片素材菜单');
INSERT INTO `sys_menu`
VALUES (2072, '图片素材查询', 2071, 1, '#', '', 1, NULL, 'F', '0', '0', 'material:image:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2073, '图片素材新增', 2071, 2, '#', '', 1, NULL, 'F', '0', '0', 'material:image:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2074, '图片素材修改', 2071, 3, '#', '', 1, NULL, 'F', '0', '0', 'material:image:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2075, '图片素材删除', 2071, 4, '#', '', 1, NULL, 'F', '0', '0', 'material:image:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2076, '图片素材导出', 2071, 5, '#', '', 1, NULL, 'F', '0', '0', 'material:image:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2077, '友情链接', 2006, 1, 'friend', 'business/friend/index', 1, NULL, 'C', '0', '0', 'business:friend:list',
        'eye-open', 'admin', '2018-03-01 00:00:00', 'admin', '2021-04-15 09:04:55', '友情链接菜单');
INSERT INTO `sys_menu`
VALUES (2078, '友情链接查询', 2077, 1, '#', '', 1, NULL, 'F', '0', '0', 'business:friend:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2079, '友情链接新增', 2077, 2, '#', '', 1, NULL, 'F', '0', '0', 'business:friend:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2080, '友情链接修改', 2077, 3, '#', '', 1, NULL, 'F', '0', '0', 'business:friend:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2081, '友情链接删除', 2077, 4, '#', '', 1, NULL, 'F', '0', '0', 'business:friend:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2082, '友情链接导出', 2077, 5, '#', '', 1, NULL, 'F', '0', '0', 'business:friend:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2083, '信息管理', 2006, 1, 'about', 'business/about/index', 1, NULL, 'C', '0', '0', 'business:about:list', 'drag',
        'admin', '2018-03-01 00:00:00', 'admin', '2021-04-22 03:42:44', '信息管理菜单');
INSERT INTO `sys_menu`
VALUES (2084, '信息管理查询', 2083, 1, '#', '', 1, NULL, 'F', '0', '0', 'business:about:query', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2085, '信息管理新增', 2083, 2, '#', '', 1, NULL, 'F', '0', '0', 'business:about:add', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2086, '信息管理修改', 2083, 3, '#', '', 1, NULL, 'F', '0', '0', 'business:about:edit', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2087, '信息管理删除', 2083, 4, '#', '', 1, NULL, 'F', '0', '0', 'business:about:remove', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
INSERT INTO `sys_menu`
VALUES (2088, '信息管理导出', 2083, 5, '#', '', 1, NULL, 'F', '0', '0', 'business:about:export', '#', 'admin',
        '2018-03-01 00:00:00', 'ry', '2018-03-01 00:00:00', '');
COMMIT;

-- ----------------------------
-- Table structure for sys_notice
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice`;
CREATE TABLE `sys_notice`
(
    `notice_id`      int                                                          NOT NULL AUTO_INCREMENT COMMENT '公告ID',
    `notice_title`   varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告标题',
    `notice_type`    char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NOT NULL COMMENT '公告类型（1通知 2公告）',
    `notice_content` longblob COMMENT '公告内容',
    `status`         char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '公告状态（0正常 1关闭）',
    `create_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time`    datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time`    datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`         varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`notice_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 10
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='通知公告表';

-- ----------------------------
-- Records of sys_notice
-- ----------------------------
BEGIN;
INSERT INTO `sys_notice`
VALUES (1, '我们的目标是星辰大海！', '2', 0x3C703E3C62723E3C2F703E, '0', 'admin', '2018-03-16 11:33:00', 'admin',
        '2020-11-07 14:32:26', '管理员');
COMMIT;

-- ----------------------------
-- Table structure for sys_oper_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_oper_log`;
CREATE TABLE `sys_oper_log`
(
    `oper_id`        bigint NOT NULL AUTO_INCREMENT COMMENT '日志主键',
    `title`          varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '' COMMENT '模块标题',
    `business_type`  int                                                            DEFAULT '0' COMMENT '业务类型（0其它 1新增 2修改 3删除）',
    `method`         varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '方法名称',
    `request_method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '' COMMENT '请求方式',
    `operator_type`  int                                                            DEFAULT '0' COMMENT '操作类别（0其它 1后台用户 2手机端用户）',
    `oper_name`      varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '' COMMENT '操作人员',
    `dept_name`      varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '' COMMENT '部门名称',
    `oper_url`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '请求URL',
    `oper_ip`        varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '' COMMENT '主机地址',
    `oper_location`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '操作地点',
    `oper_param`     varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '请求参数',
    `json_result`    varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '返回参数',
    `status`         int                                                            DEFAULT '0' COMMENT '操作状态（0正常 1异常）',
    `error_msg`      varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '错误消息',
    `oper_time`      datetime                                                       DEFAULT NULL COMMENT '操作时间',
    PRIMARY KEY (`oper_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 10
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='操作日志记录';

-- ----------------------------
-- Records of sys_oper_log
-- ----------------------------
BEGIN;
INSERT INTO `sys_oper_log`
VALUES (1, '用户管理', 3, 'com.ruoyi.web.controller.system.SysUserController.remove()', 'DELETE', 1, 'admin', NULL,
        '/system/user/2', '127.0.0.1', '内网IP', '{userIds=2}', '{\"msg\":\"操作成功\",\"code\":200}', 0, NULL,
        '2021-06-11 10:53:45');
COMMIT;

-- ----------------------------
-- Table structure for sys_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_post`;
CREATE TABLE `sys_post`
(
    `post_id`     bigint                                                       NOT NULL AUTO_INCREMENT COMMENT '岗位ID',
    `post_code`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '岗位编码',
    `post_name`   varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '岗位名称',
    `post_sort`   int                                                          NOT NULL COMMENT '显示顺序',
    `status`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NOT NULL COMMENT '状态（0正常 1停用）',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`      varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`post_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 5
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='岗位信息表';

-- ----------------------------
-- Records of sys_post
-- ----------------------------
BEGIN;
INSERT INTO `sys_post`
VALUES (1, 'ceo', '开发者', 1, '0', 'admin', '2018-03-16 11:33:00', 'admin', '2020-09-10 10:33:03', '');
INSERT INTO `sys_post`
VALUES (4, 'user', '使用者', 4, '0', 'admin', '2018-03-16 11:33:00', 'admin', '2020-09-10 10:33:10', '');
COMMIT;

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`
(
    `role_id`             bigint                                                        NOT NULL AUTO_INCREMENT COMMENT '角色ID',
    `role_name`           varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL COMMENT '角色名称',
    `role_key`            varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色权限字符串',
    `role_sort`           int                                                           NOT NULL COMMENT '显示顺序',
    `data_scope`          char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '1' COMMENT '数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）',
    `status`              char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      NOT NULL COMMENT '角色状态（0正常 1停用）',
    `del_flag`            char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
    `create_by`           varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time`         datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`           varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time`         datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`              varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
    `menu_check_strictly` tinyint(1)                                                    DEFAULT '1' COMMENT '菜单树选择项是否关联显示',
    `dept_check_strictly` tinyint(1)                                                    DEFAULT '1' COMMENT '部门树选择项是否关联显示',
    PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 103
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='角色信息表';

-- ----------------------------
-- Records of sys_role
-- ----------------------------
BEGIN;
INSERT INTO `sys_role`
VALUES (1, '超级管理员', 'admin', 1, '1', '0', '0', 'admin', '2018-03-16 11:33:00', 'ry', '2018-03-16 11:33:00', '超级管理员', 1,
        1);
INSERT INTO `sys_role`
VALUES (2, '普通发票角色', 'common', 2, '2', '0', '2', 'admin', '2018-03-16 11:33:00', 'admin', '2021-06-05 12:11:49', '普通角色',
        1, 1);
INSERT INTO `sys_role`
VALUES (100, '普通媒体角色', 'media', 2, '1', '0', '0', 'admin', '2020-10-17 10:11:49', 'admin', '2021-06-05 12:14:15', NULL,
        1, 1);
INSERT INTO `sys_role`
VALUES (101, '普通开发角色', 'develop', 3, '1', '0', '0', 'admin', '2020-10-17 10:30:05', 'admin', '2021-06-05 12:14:21',
        NULL, 1, 1);
INSERT INTO `sys_role`
VALUES (102, '审核菌', 'reviewer', 102, '1', '0', '0', 'admin', '2021-03-06 08:46:48', '', NULL, NULL, 1, 1);
COMMIT;

-- ----------------------------
-- Table structure for sys_role_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_dept`;
CREATE TABLE `sys_role_dept`
(
    `role_id` bigint NOT NULL COMMENT '角色ID',
    `dept_id` bigint NOT NULL COMMENT '部门ID',
    PRIMARY KEY (`role_id`, `dept_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='角色和部门关联表';

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu`
(
    `role_id` bigint NOT NULL COMMENT '角色ID',
    `menu_id` bigint NOT NULL COMMENT '菜单ID',
    PRIMARY KEY (`role_id`, `menu_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='角色和菜单关联表';

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
BEGIN;
INSERT INTO `sys_role_menu`
VALUES (100, 2006);
INSERT INTO `sys_role_menu`
VALUES (100, 2013);
INSERT INTO `sys_role_menu`
VALUES (100, 2014);
INSERT INTO `sys_role_menu`
VALUES (100, 2015);
INSERT INTO `sys_role_menu`
VALUES (100, 2016);
INSERT INTO `sys_role_menu`
VALUES (100, 2017);
INSERT INTO `sys_role_menu`
VALUES (100, 2018);
INSERT INTO `sys_role_menu`
VALUES (100, 2019);
INSERT INTO `sys_role_menu`
VALUES (100, 2020);
INSERT INTO `sys_role_menu`
VALUES (100, 2021);
INSERT INTO `sys_role_menu`
VALUES (100, 2022);
INSERT INTO `sys_role_menu`
VALUES (100, 2023);
INSERT INTO `sys_role_menu`
VALUES (100, 2024);
INSERT INTO `sys_role_menu`
VALUES (100, 2026);
INSERT INTO `sys_role_menu`
VALUES (100, 2027);
INSERT INTO `sys_role_menu`
VALUES (100, 2028);
INSERT INTO `sys_role_menu`
VALUES (100, 2029);
INSERT INTO `sys_role_menu`
VALUES (100, 2030);
INSERT INTO `sys_role_menu`
VALUES (100, 2031);
INSERT INTO `sys_role_menu`
VALUES (100, 2032);
INSERT INTO `sys_role_menu`
VALUES (100, 2033);
INSERT INTO `sys_role_menu`
VALUES (100, 2034);
INSERT INTO `sys_role_menu`
VALUES (100, 2035);
INSERT INTO `sys_role_menu`
VALUES (100, 2036);
INSERT INTO `sys_role_menu`
VALUES (100, 2037);
INSERT INTO `sys_role_menu`
VALUES (100, 2038);
INSERT INTO `sys_role_menu`
VALUES (100, 2051);
INSERT INTO `sys_role_menu`
VALUES (100, 2077);
INSERT INTO `sys_role_menu`
VALUES (100, 2078);
INSERT INTO `sys_role_menu`
VALUES (100, 2079);
INSERT INTO `sys_role_menu`
VALUES (100, 2080);
INSERT INTO `sys_role_menu`
VALUES (100, 2081);
INSERT INTO `sys_role_menu`
VALUES (100, 2082);
INSERT INTO `sys_role_menu`
VALUES (100, 2083);
INSERT INTO `sys_role_menu`
VALUES (100, 2084);
INSERT INTO `sys_role_menu`
VALUES (100, 2085);
INSERT INTO `sys_role_menu`
VALUES (100, 2086);
INSERT INTO `sys_role_menu`
VALUES (100, 2087);
INSERT INTO `sys_role_menu`
VALUES (100, 2088);
INSERT INTO `sys_role_menu`
VALUES (101, 3);
INSERT INTO `sys_role_menu`
VALUES (101, 113);
INSERT INTO `sys_role_menu`
VALUES (101, 114);
INSERT INTO `sys_role_menu`
VALUES (101, 115);
INSERT INTO `sys_role_menu`
VALUES (101, 1055);
INSERT INTO `sys_role_menu`
VALUES (101, 1056);
INSERT INTO `sys_role_menu`
VALUES (101, 1057);
INSERT INTO `sys_role_menu`
VALUES (101, 1058);
INSERT INTO `sys_role_menu`
VALUES (101, 1059);
INSERT INTO `sys_role_menu`
VALUES (101, 1060);
INSERT INTO `sys_role_menu`
VALUES (101, 2006);
INSERT INTO `sys_role_menu`
VALUES (101, 2013);
INSERT INTO `sys_role_menu`
VALUES (101, 2014);
INSERT INTO `sys_role_menu`
VALUES (101, 2015);
INSERT INTO `sys_role_menu`
VALUES (101, 2016);
INSERT INTO `sys_role_menu`
VALUES (101, 2017);
INSERT INTO `sys_role_menu`
VALUES (101, 2018);
INSERT INTO `sys_role_menu`
VALUES (101, 2019);
INSERT INTO `sys_role_menu`
VALUES (101, 2020);
INSERT INTO `sys_role_menu`
VALUES (101, 2021);
INSERT INTO `sys_role_menu`
VALUES (101, 2022);
INSERT INTO `sys_role_menu`
VALUES (101, 2023);
INSERT INTO `sys_role_menu`
VALUES (101, 2024);
INSERT INTO `sys_role_menu`
VALUES (101, 2025);
INSERT INTO `sys_role_menu`
VALUES (101, 2026);
INSERT INTO `sys_role_menu`
VALUES (101, 2027);
INSERT INTO `sys_role_menu`
VALUES (101, 2028);
INSERT INTO `sys_role_menu`
VALUES (101, 2029);
INSERT INTO `sys_role_menu`
VALUES (101, 2030);
INSERT INTO `sys_role_menu`
VALUES (101, 2031);
INSERT INTO `sys_role_menu`
VALUES (101, 2051);
INSERT INTO `sys_role_menu`
VALUES (101, 2059);
INSERT INTO `sys_role_menu`
VALUES (101, 2060);
INSERT INTO `sys_role_menu`
VALUES (101, 2061);
INSERT INTO `sys_role_menu`
VALUES (101, 2062);
INSERT INTO `sys_role_menu`
VALUES (101, 2063);
INSERT INTO `sys_role_menu`
VALUES (101, 2064);
INSERT INTO `sys_role_menu`
VALUES (101, 2065);
INSERT INTO `sys_role_menu`
VALUES (101, 2066);
INSERT INTO `sys_role_menu`
VALUES (101, 2067);
INSERT INTO `sys_role_menu`
VALUES (101, 2068);
INSERT INTO `sys_role_menu`
VALUES (101, 2069);
INSERT INTO `sys_role_menu`
VALUES (101, 2070);
INSERT INTO `sys_role_menu`
VALUES (101, 2071);
INSERT INTO `sys_role_menu`
VALUES (101, 2072);
INSERT INTO `sys_role_menu`
VALUES (101, 2073);
INSERT INTO `sys_role_menu`
VALUES (101, 2074);
INSERT INTO `sys_role_menu`
VALUES (101, 2075);
INSERT INTO `sys_role_menu`
VALUES (101, 2076);
INSERT INTO `sys_role_menu`
VALUES (101, 2077);
INSERT INTO `sys_role_menu`
VALUES (101, 2078);
INSERT INTO `sys_role_menu`
VALUES (101, 2079);
INSERT INTO `sys_role_menu`
VALUES (101, 2080);
INSERT INTO `sys_role_menu`
VALUES (101, 2081);
INSERT INTO `sys_role_menu`
VALUES (101, 2082);
INSERT INTO `sys_role_menu`
VALUES (101, 2083);
INSERT INTO `sys_role_menu`
VALUES (101, 2084);
INSERT INTO `sys_role_menu`
VALUES (101, 2085);
INSERT INTO `sys_role_menu`
VALUES (101, 2086);
INSERT INTO `sys_role_menu`
VALUES (101, 2087);
INSERT INTO `sys_role_menu`
VALUES (101, 2088);
INSERT INTO `sys_role_menu`
VALUES (102, 2025);
INSERT INTO `sys_role_menu`
VALUES (102, 2059);
INSERT INTO `sys_role_menu`
VALUES (102, 2060);
INSERT INTO `sys_role_menu`
VALUES (102, 2062);
COMMIT;

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`
(
    `user_id`     bigint                                                       NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `dept_id`     bigint                                                        DEFAULT NULL COMMENT '部门ID',
    `user_name`   varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户账号',
    `nick_name`   varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户昵称',
    `user_type`   varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci   DEFAULT '00' COMMENT '用户类型（00系统用户）',
    `email`       varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '用户邮箱',
    `phonenumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '手机号码',
    `sex`         char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '用户性别（0男 1女 2未知）',
    `avatar`      varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '头像地址',
    `password`    varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '密码',
    `status`      char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '帐号状态（0正常 1停用）',
    `del_flag`    char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
    `login_ip`    varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '最后登陆IP',
    `login_date`  datetime                                                      DEFAULT NULL COMMENT '最后登陆时间',
    `create_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '创建者',
    `create_time` datetime                                                      DEFAULT NULL COMMENT '创建时间',
    `update_by`   varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT '' COMMENT '更新者',
    `update_time` datetime                                                      DEFAULT NULL COMMENT '更新时间',
    `remark`      varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
    PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 103
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='用户信息表';

-- ----------------------------
-- Records of sys_user
-- ----------------------------
BEGIN;
INSERT INTO `sys_user`
VALUES (1, 103, 'admin', 'Hocassian', '00', '88888888@qq.com', '18888888888', '0',
        '/profile/avatar/2020/09/10/06e22868-69cb-4c10-84b8-9cec15778380.jpeg',
        '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '0', '127.0.0.1', '2018-03-16 11:33:00',
        'admin', '2018-03-16 11:33:00', 'ry', '2020-09-10 10:25:07', '管理员');
INSERT INTO `sys_user`
VALUES (2, 200, 'maggie', 'maggie', '00', '88888888@qq.com', '18888888888', '1', '',
        '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '2', '127.0.0.1', '2018-03-16 11:33:00',
        'admin', '2018-03-16 11:33:00', 'admin', '2021-06-05 12:15:19', '普通用户');
INSERT INTO `sys_user`
VALUES (100, 103, 'developer', 'developer', '00', '88888888@qq.com', '18888888888', '0',
        '/profile/avatar/2021/03/11/f5696e06-3d33-43ce-b380-f9252128a912.jpeg',
        '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '0', '', NULL, 'admin',
        '2020-10-17 10:28:05', 'admin', '2021-06-11 10:54:34', NULL);
INSERT INTO `sys_user`
VALUES (101, 200, 'reborn', 'reborn', '00', '88888888@qq.com', '18888888888', '0', '',
        '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '2', '', NULL, 'admin',
        '2020-11-24 13:48:21', '', NULL, NULL);
INSERT INTO `sys_user`
VALUES (102, 200, 'reviewer', 'reviewer', '00', '88888888@qq.com', '18888888888', '2', '',
        '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', '2', '', NULL, 'admin',
        '2021-03-06 08:47:53', '', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for sys_user_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_post`;
CREATE TABLE `sys_user_post`
(
    `user_id` bigint NOT NULL COMMENT '用户ID',
    `post_id` bigint NOT NULL COMMENT '岗位ID',
    PRIMARY KEY (`user_id`, `post_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='用户与岗位关联表';

-- ----------------------------
-- Records of sys_user_post
-- ----------------------------
BEGIN;
INSERT INTO `sys_user_post`
VALUES (1, 1);
INSERT INTO `sys_user_post`
VALUES (100, 1);
COMMIT;

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`
(
    `user_id` bigint NOT NULL COMMENT '用户ID',
    `role_id` bigint NOT NULL COMMENT '角色ID',
    PRIMARY KEY (`user_id`, `role_id`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='用户和角色关联表';

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
BEGIN;
INSERT INTO `sys_user_role`
VALUES (1, 1);
INSERT INTO `sys_user_role`
VALUES (100, 101);
COMMIT;

-- ----------------------------
-- Table structure for flow_distribute
-- ----------------------------
DROP TABLE IF EXISTS `flow_distribute`;
CREATE TABLE `flow_distribute`
(
    `id`               int NOT NULL AUTO_INCREMENT,
    `duration`         int                                                           DEFAULT NULL COMMENT '分发素材时长（单位：秒）',
    `status`           char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci      DEFAULT NULL COMMENT '流程状态（0：无效；1：初创建；2：确定音乐；3：确定封面（正在渲染）；4：渲染完成；5：分发完成）',
    `mat_list`         longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '素材列表',
    `audio_path`       varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '稿件对应音乐audio_path',
    `operator_open_id` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '操作人open_id',
    `cover_pic`        varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '封面图path',
    `keywords`         longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '素材关键字列表（用于定义标题和封面）',
    `adj_keywords`     longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '素材属性形容词',
    `youtube_id`       varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT '油管地址',
    `bilibili_id`      varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  DEFAULT NULL COMMENT 'b站地址',
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 64
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

SET FOREIGN_KEY_CHECKS = 1;
