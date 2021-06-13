package com.ruoyi.client.service;

import com.ruoyi.business.domain.BusSwiper;

import java.util.List;

/**
 * 主页轮播图Service接口
 * 
 * @author Hocassian
 * @date 2020-10-15
 */
public interface IClientSwiperService
{
    /**
     * 查询主页轮播图
     * 
     * @param id 主页轮播图ID
     * @return 主页轮播图
     */
    public BusSwiper selectClientSwiperById(Long id);

    /**
     * 查询主页轮播图列表
     * 
     * @param busSwiper 主页轮播图
     * @return 主页轮播图集合
     */
    public List<BusSwiper> selectClientSwiperList(BusSwiper busSwiper);
}
