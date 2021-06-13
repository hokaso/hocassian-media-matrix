package com.ruoyi.business.mapper;

import java.util.List;
import com.ruoyi.business.domain.BusSwiper;

/**
 * 主页轮播图Mapper接口
 * 
 * @author Hocassian
 * @date 2020-10-15
 */
public interface BusSwiperMapper 
{
    /**
     * 查询主页轮播图
     * 
     * @param id 主页轮播图ID
     * @return 主页轮播图
     */
    public BusSwiper selectBusSwiperById(Long id);

    /**
     * 查询主页轮播图列表
     * 
     * @param busSwiper 主页轮播图
     * @return 主页轮播图集合
     */
    public List<BusSwiper> selectBusSwiperList(BusSwiper busSwiper);

    /**
     * 改变视频上下架状态
     *
     * @param busSwiper 主页轮播图
     * @return 主页轮播图
     */
    public int changeBusSwiperStatus(BusSwiper busSwiper);

    /**
     * 新增主页轮播图
     * 
     * @param busSwiper 主页轮播图
     * @return 结果
     */
    public int insertBusSwiper(BusSwiper busSwiper);

    /**
     * 修改主页轮播图
     * 
     * @param busSwiper 主页轮播图
     * @return 结果
     */
    public int updateBusSwiper(BusSwiper busSwiper);

    /**
     * 删除主页轮播图
     * 
     * @param id 主页轮播图ID
     * @return 结果
     */
    public int deleteBusSwiperById(Long id);

    /**
     * 批量删除主页轮播图
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteBusSwiperByIds(Long[] ids);
}
