package com.ruoyi.create.controller;

import java.util.List;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.create.domain.CreChapter;
import com.ruoyi.create.service.ICreChapterService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 篇章管理Controller
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
@RestController
@RequestMapping("/create/chapter")
public class CreChapterController extends BaseController
{
    @Autowired
    private ICreChapterService creChapterService;

    /**
     * 查询篇章管理列表
     */
    @PreAuthorize("@ss.hasPermi('create:chapter:list')")
    @GetMapping("/list")
    public TableDataInfo list(CreChapter creChapter)
    {
        startPage();
        List<CreChapter> list = creChapterService.selectCreChapterList(creChapter);
        return getDataTable(list);
    }

    /**
     * 导出篇章管理列表
     */
    @PreAuthorize("@ss.hasPermi('create:chapter:export')")
    @Log(title = "篇章管理", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(CreChapter creChapter)
    {
        List<CreChapter> list = creChapterService.selectCreChapterList(creChapter);
        ExcelUtil<CreChapter> util = new ExcelUtil<CreChapter>(CreChapter.class);
        return util.exportExcel(list, "chapter");
    }

    /**
     * 获取篇章管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('create:chapter:query')")
    @GetMapping(value = "/{chapterStoryId}")
    public AjaxResult getInfo(@PathVariable("chapterStoryId") Long chapterStoryId)
    {
        return AjaxResult.success(creChapterService.selectCreChapterById(chapterStoryId));
    }

    /**
     * 新增篇章管理
     */
    @PreAuthorize("@ss.hasPermi('create:chapter:add')")
    @Log(title = "篇章管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody CreChapter creChapter)
    {
        return toAjax(creChapterService.insertCreChapter(creChapter));
    }

    /**
     * 修改篇章管理
     */
    @PreAuthorize("@ss.hasPermi('create:chapter:edit')")
    @Log(title = "篇章管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody CreChapter creChapter)
    {
        return toAjax(creChapterService.updateCreChapter(creChapter));
    }

    /**
     * 删除篇章管理
     */
    @PreAuthorize("@ss.hasPermi('create:chapter:remove')")
    @Log(title = "篇章管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{chapterStoryIds}")
    public AjaxResult remove(@PathVariable Long[] chapterStoryIds)
    {
        return toAjax(creChapterService.deleteCreChapterByIds(chapterStoryIds));
    }
}
