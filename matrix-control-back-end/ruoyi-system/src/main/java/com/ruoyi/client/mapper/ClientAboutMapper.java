package com.ruoyi.client.mapper;

import com.ruoyi.business.domain.BusAbout;

/**
 * 信息管理Mapper接口
 * 
 * @author Hocassian
 * @date 2021-04-22
 */
public interface ClientAboutMapper
{
    /**
     * 查询信息管理
     *
     * @return 信息管理
     */
    public BusAbout selectClientAbout();

}
