package com.ruoyi.client.service.impl;

import com.ruoyi.business.domain.BusSwiper;
import com.ruoyi.client.mapper.ClientSwiperMapper;
import com.ruoyi.client.service.IClientSwiperService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 主页轮播图Service业务层处理
 * 
 * @author Hocassian
 * @date 2020-10-15
 */
@Service
public class ClientSwiperServiceImpl implements IClientSwiperService
{
    @Autowired
    private ClientSwiperMapper clientSwiperMapper;

    /**
     * 查询主页轮播图
     * 
     * @param id 主页轮播图ID
     * @return 主页轮播图
     */
    @Override
    public BusSwiper selectClientSwiperById(Long id)
    {
        return clientSwiperMapper.selectClientSwiperById(id);
    }

    /**
     * 查询主页轮播图列表
     * 
     * @param busSwiper 主页轮播图
     * @return 主页轮播图
     */
    @Override
    public List<BusSwiper> selectClientSwiperList(BusSwiper busSwiper)
    {
        return clientSwiperMapper.selectClientSwiperList(busSwiper);
    }
}
