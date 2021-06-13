package com.ruoyi.publish.service;

import java.util.List;
import com.ruoyi.publish.domain.PubUnit;

/**
 * 媒体单位Service接口
 * 
 * @author Hocassian
 * @date 2020-11-24
 */
public interface IPubUnitService 
{
    /**
     * 查询媒体单位
     * 
     * @param unitId 媒体单位ID
     * @return 媒体单位
     */
    public PubUnit selectPubUnitById(Long unitId);

    /**
     * 查询媒体单位列表
     * 
     * @param pubUnit 媒体单位
     * @return 媒体单位集合
     */
    public List<PubUnit> selectPubUnitList(PubUnit pubUnit);

    /**
     * 新增媒体单位
     * 
     * @param pubUnit 媒体单位
     * @return 结果
     */
    public int insertPubUnit(PubUnit pubUnit);

    /**
     * 修改媒体单位
     * 
     * @param pubUnit 媒体单位
     * @return 结果
     */
    public int updatePubUnit(PubUnit pubUnit);

    /**
     * 批量删除媒体单位
     * 
     * @param unitIds 需要删除的媒体单位ID
     * @return 结果
     */
    public int deletePubUnitByIds(Long[] unitIds);

    /**
     * 删除媒体单位信息
     * 
     * @param unitId 媒体单位ID
     * @return 结果
     */
    public int deletePubUnitById(Long unitId);
}
