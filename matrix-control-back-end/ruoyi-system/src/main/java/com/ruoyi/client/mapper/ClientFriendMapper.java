package com.ruoyi.client.mapper;

import com.ruoyi.business.domain.BusFriend;

import java.util.List;

/**
 * 主页轮播图Mapper接口
 *
 * @author Hocassian
 * @date 2020-10-15
 */
public interface ClientFriendMapper {

    /**
     * 查询平台
     *
     * @param busFriend 官网展示平台
     * @return 平台集合
     */
    public List<BusFriend> selectClientPlatformList();

    /**
     * 查询栏目
     *
     * @param busFriend 官网展示栏目
     * @return 栏目集合
     */
    public List<BusFriend> selectClientColumnList();
}
