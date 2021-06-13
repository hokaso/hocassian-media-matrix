package com.ruoyi.business.mapper;

import com.ruoyi.business.domain.BusAbout;

import java.util.List;

/**
 * 信息管理Mapper接口
 * 
 * @author Hocassian
 * @date 2021-04-22
 */
public interface BusAboutMapper 
{
    /**
     * 查询信息管理
     * 
     * @param aboutId 信息管理ID
     * @return 信息管理
     */
    public BusAbout selectBusAboutById(Long aboutId);

    /**
     * 查询信息管理列表
     * 
     * @param busAbout 信息管理
     * @return 信息管理集合
     */
    public List<BusAbout> selectBusAboutList(BusAbout busAbout);

    /**
     * 新增信息管理
     * 
     * @param busAbout 信息管理
     * @return 结果
     */
    public int insertBusAbout(BusAbout busAbout);

    /**
     * 修改信息管理
     * 
     * @param busAbout 信息管理
     * @return 结果
     */
    public int updateBusAbout(BusAbout busAbout);

    /**
     * 删除信息管理
     * 
     * @param aboutId 信息管理ID
     * @return 结果
     */
    public int deleteBusAboutById(Long aboutId);

    /**
     * 批量删除信息管理
     * 
     * @param aboutIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteBusAboutByIds(Long[] aboutIds);
}
