package com.ruoyi.business.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.business.mapper.BusAboutMapper;
import com.ruoyi.business.domain.BusAbout;
import com.ruoyi.business.service.IBusAboutService;

/**
 * 信息管理Service业务层处理
 * 
 * @author Hocassian
 * @date 2021-04-22
 */
@Service
public class BusAboutServiceImpl implements IBusAboutService 
{
    @Autowired
    private BusAboutMapper busAboutMapper;

    /**
     * 查询信息管理
     * 
     * @param aboutId 信息管理ID
     * @return 信息管理
     */
    @Override
    public BusAbout selectBusAboutById(Long aboutId)
    {
        return busAboutMapper.selectBusAboutById(aboutId);
    }

    /**
     * 查询信息管理列表
     * 
     * @param busAbout 信息管理
     * @return 信息管理
     */
    @Override
    public List<BusAbout> selectBusAboutList(BusAbout busAbout)
    {
        return busAboutMapper.selectBusAboutList(busAbout);
    }

    /**
     * 新增信息管理
     * 
     * @param busAbout 信息管理
     * @return 结果
     */
    @Override
    public int insertBusAbout(BusAbout busAbout)
    {
        return busAboutMapper.insertBusAbout(busAbout);
    }

    /**
     * 修改信息管理
     * 
     * @param busAbout 信息管理
     * @return 结果
     */
    @Override
    public int updateBusAbout(BusAbout busAbout)
    {
        return busAboutMapper.updateBusAbout(busAbout);
    }

    /**
     * 批量删除信息管理
     * 
     * @param aboutIds 需要删除的信息管理ID
     * @return 结果
     */
    @Override
    public int deleteBusAboutByIds(Long[] aboutIds)
    {
        return busAboutMapper.deleteBusAboutByIds(aboutIds);
    }

    /**
     * 删除信息管理信息
     * 
     * @param aboutId 信息管理ID
     * @return 结果
     */
    @Override
    public int deleteBusAboutById(Long aboutId)
    {
        return busAboutMapper.deleteBusAboutById(aboutId);
    }
}
