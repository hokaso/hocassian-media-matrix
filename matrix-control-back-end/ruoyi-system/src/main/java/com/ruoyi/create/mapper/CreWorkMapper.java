package com.ruoyi.create.mapper;

import java.util.List;
import com.ruoyi.create.domain.CreWork;

/**
 * 作品管理Mapper接口
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
public interface CreWorkMapper 
{
    /**
     * 查询作品管理
     * 
     * @param workStoryId 作品管理ID
     * @return 作品管理
     */
    public CreWork selectCreWorkById(Long workStoryId);

    /**
     * 查询作品管理列表
     * 
     * @param creWork 作品管理
     * @return 作品管理集合
     */
    public List<CreWork> selectCreWorkList(CreWork creWork);

    /**
     * 新增作品管理
     * 
     * @param creWork 作品管理
     * @return 结果
     */
    public int insertCreWork(CreWork creWork);

    /**
     * 修改作品管理
     * 
     * @param creWork 作品管理
     * @return 结果
     */
    public int updateCreWork(CreWork creWork);

    /**
     * 删除作品管理
     * 
     * @param workStoryId 作品管理ID
     * @return 结果
     */
    public int deleteCreWorkById(Long workStoryId);

    /**
     * 批量删除作品管理
     * 
     * @param workStoryIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteCreWorkByIds(Long[] workStoryIds);
}
