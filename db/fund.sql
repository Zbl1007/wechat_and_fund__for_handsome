-- phpMyAdmin SQL Dump
-- version 4.4.15.10
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2021-11-10 23:38:58
-- 服务器版本： 5.5.62-log
-- PHP Version: 7.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fund`
--

-- --------------------------------------------------------

--
-- 表的结构 `cross`
--

CREATE TABLE IF NOT EXISTS `cross` (
  `id` int(11) NOT NULL,
  `openid` varchar(255) CHARACTER SET utf8mb4 NOT NULL DEFAULT '',
  `url` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `timecode` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `mid` int(11) DEFAULT NULL,
  `msg_type` varchar(16) CHARACTER SET utf8mb4 DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- 转存表中的数据 `cross`
--


--
-- 表的结构 `fund`
--

CREATE TABLE IF NOT EXISTS `fund` (
  `id` int(11) NOT NULL COMMENT '主键',
  `code` varchar(8) DEFAULT NULL COMMENT '基金代码',
  `name` varchar(50) DEFAULT NULL COMMENT '基金名称',
  `share` decimal(20,3) DEFAULT NULL COMMENT '份额'
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COMMENT='基金信息表';

--
-- 转存表中的数据 `fund`
--


--
-- 表的结构 `rela_wx_fund`
--

CREATE TABLE IF NOT EXISTS `rela_wx_fund` (
  `id` int(11) NOT NULL COMMENT '主键',
  `wx_info_id` int(11) DEFAULT NULL COMMENT '微信信息表主键id',
  `fund_id` int(11) DEFAULT NULL COMMENT '基金表主键id'
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COMMENT='微信-基金关联表';

--
-- 转存表中的数据 `rela_wx_fund`
--


--
-- 表的结构 `wx_info`
--

CREATE TABLE IF NOT EXISTS `wx_info` (
  `id` int(11) NOT NULL COMMENT '主键',
  `wx_id` varchar(50) DEFAULT NULL COMMENT '微信id',
  `wx_name` varchar(50) DEFAULT NULL COMMENT '微信名',
  `is_del` varchar(1) DEFAULT NULL COMMENT '是否删除'
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='微信信息表';

--
-- 转存表中的数据 `wx_info`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cross`
--
ALTER TABLE `cross`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indexes for table `fund`
--
ALTER TABLE `fund`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `rela_wx_fund`
--
ALTER TABLE `rela_wx_fund`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wx_info`
--
ALTER TABLE `wx_info`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cross`
--
ALTER TABLE `cross`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=24;
--
-- AUTO_INCREMENT for table `fund`
--
ALTER TABLE `fund`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',AUTO_INCREMENT=31;
--
-- AUTO_INCREMENT for table `rela_wx_fund`
--
ALTER TABLE `rela_wx_fund`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',AUTO_INCREMENT=23;
--
-- AUTO_INCREMENT for table `wx_info`
--
ALTER TABLE `wx_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',AUTO_INCREMENT=4;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
