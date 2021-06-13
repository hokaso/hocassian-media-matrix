package com.ruoyi.business.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.business.mapper.BusSwiperMapper;
import com.ruoyi.business.domain.BusSwiper;
import com.ruoyi.business.service.IBusSwiperService;

/**
 * 主页轮播图Service业务层处理
 * 
 * @author Hocassian
 * @date 2020-10-15
 */
@Service
public class BusSwiperServiceImpl implements IBusSwiperService 
{
    @Autowired
    private BusSwiperMapper busSwiperMapper;

    /**
     * 查询主页轮播图
     * 
     * @param id 主页轮播图ID
     * @return 主页轮播图
     */
    @Override
    public BusSwiper selectBusSwiperById(Long id)
    {
        return busSwiperMapper.selectBusSwiperById(id);
    }

    /**
     * 查询主页轮播图列表
     * 
     * @param busSwiper 主页轮播图
     * @return 主页轮播图
     */
    @Override
    public List<BusSwiper> selectBusSwiperList(BusSwiper busSwiper)
    {
        return busSwiperMapper.selectBusSwiperList(busSwiper);
    }

    /**
     * 改变状态
     *
     * @param busSwiper 主页轮播图
     * @return 主页轮播图
     */
    @Override
    public int changeBusSwiperStatus(BusSwiper busSwiper)
    {
        return busSwiperMapper.changeBusSwiperStatus(busSwiper);
    }

    /**
     * 新增主页轮播图
     * 
     * @param busSwiper 主页轮播图
     * @return 结果
     */
    @Override
    public int insertBusSwiper(BusSwiper busSwiper)
    {
        return busSwiperMapper.insertBusSwiper(busSwiper);
    }

    /**
     * 修改主页轮播图
     * 
     * @param busSwiper 主页轮播图
     * @return 结果
     */
    @Override
    public int updateBusSwiper(BusSwiper busSwiper)
    {
        return busSwiperMapper.updateBusSwiper(busSwiper);
    }

    /**
     * 批量删除主页轮播图
     * 
     * @param ids 需要删除的主页轮播图ID
     * @return 结果
     */
    @Override
    public int deleteBusSwiperByIds(Long[] ids)
    {
        return busSwiperMapper.deleteBusSwiperByIds(ids);
    }

    /**
     * 删除主页轮播图信息
     * 
     * @param id 主页轮播图ID
     * @return 结果
     */
    @Override
    public int deleteBusSwiperById(Long id)
    {
        return busSwiperMapper.deleteBusSwiperById(id);
    }
}
