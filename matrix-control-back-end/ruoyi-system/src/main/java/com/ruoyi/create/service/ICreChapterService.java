package com.ruoyi.create.service;

import java.util.List;
import com.ruoyi.create.domain.CreChapter;

/**
 * 篇章管理Service接口
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
public interface ICreChapterService 
{
    /**
     * 查询篇章管理
     * 
     * @param chapterStoryId 篇章管理ID
     * @return 篇章管理
     */
    public CreChapter selectCreChapterById(Long chapterStoryId);

    /**
     * 查询篇章管理列表
     * 
     * @param creChapter 篇章管理
     * @return 篇章管理集合
     */
    public List<CreChapter> selectCreChapterList(CreChapter creChapter);

    /**
     * 新增篇章管理
     * 
     * @param creChapter 篇章管理
     * @return 结果
     */
    public int insertCreChapter(CreChapter creChapter);

    /**
     * 修改篇章管理
     * 
     * @param creChapter 篇章管理
     * @return 结果
     */
    public int updateCreChapter(CreChapter creChapter);

    /**
     * 批量删除篇章管理
     * 
     * @param chapterStoryIds 需要删除的篇章管理ID
     * @return 结果
     */
    public int deleteCreChapterByIds(Long[] chapterStoryIds);

    /**
     * 删除篇章管理信息
     * 
     * @param chapterStoryId 篇章管理ID
     * @return 结果
     */
    public int deleteCreChapterById(Long chapterStoryId);
}
