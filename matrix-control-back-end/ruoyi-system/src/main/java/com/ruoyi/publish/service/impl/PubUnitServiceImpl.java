package com.ruoyi.publish.service.impl;

import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.publish.mapper.PubUnitMapper;
import com.ruoyi.publish.domain.PubUnit;
import com.ruoyi.publish.service.IPubUnitService;

/**
 * 媒体单位Service业务层处理
 * 
 * @author Hocassian
 * @date 2020-11-24
 */
@Service
public class PubUnitServiceImpl implements IPubUnitService 
{
    @Autowired
    private PubUnitMapper pubUnitMapper;

    /**
     * 查询媒体单位
     * 
     * @param unitId 媒体单位ID
     * @return 媒体单位
     */
    @Override
    public PubUnit selectPubUnitById(Long unitId)
    {
        return pubUnitMapper.selectPubUnitById(unitId);
    }

    /**
     * 查询媒体单位列表
     * 
     * @param pubUnit 媒体单位
     * @return 媒体单位
     */
    @Override
    public List<PubUnit> selectPubUnitList(PubUnit pubUnit)
    {
        return pubUnitMapper.selectPubUnitList(pubUnit);
    }

    /**
     * 新增媒体单位
     * 
     * @param pubUnit 媒体单位
     * @return 结果
     */
    @Override
    public int insertPubUnit(PubUnit pubUnit)
    {
        pubUnit.setCreateTime(DateUtils.getNowDate());
        return pubUnitMapper.insertPubUnit(pubUnit);
    }

    /**
     * 修改媒体单位
     * 
     * @param pubUnit 媒体单位
     * @return 结果
     */
    @Override
    public int updatePubUnit(PubUnit pubUnit)
    {
        pubUnit.setUpdateTime(DateUtils.getNowDate());
        return pubUnitMapper.updatePubUnit(pubUnit);
    }

    /**
     * 批量删除媒体单位
     * 
     * @param unitIds 需要删除的媒体单位ID
     * @return 结果
     */
    @Override
    public int deletePubUnitByIds(Long[] unitIds)
    {
        return pubUnitMapper.deletePubUnitByIds(unitIds);
    }

    /**
     * 删除媒体单位信息
     * 
     * @param unitId 媒体单位ID
     * @return 结果
     */
    @Override
    public int deletePubUnitById(Long unitId)
    {
        return pubUnitMapper.deletePubUnitById(unitId);
    }
}
