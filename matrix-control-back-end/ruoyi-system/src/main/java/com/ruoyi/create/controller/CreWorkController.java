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
import com.ruoyi.create.domain.CreWork;
import com.ruoyi.create.service.ICreWorkService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 作品管理Controller
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
@RestController
@RequestMapping("/create/work")
public class CreWorkController extends BaseController
{
    @Autowired
    private ICreWorkService creWorkService;

    /**
     * 查询作品管理列表
     */
    @PreAuthorize("@ss.hasPermi('create:work:list')")
    @GetMapping("/list")
    public TableDataInfo list(CreWork creWork)
    {
        startPage();
        List<CreWork> list = creWorkService.selectCreWorkList(creWork);
        return getDataTable(list);
    }

    /**
     * 导出作品管理列表
     */
    @PreAuthorize("@ss.hasPermi('create:work:export')")
    @Log(title = "作品管理", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(CreWork creWork)
    {
        List<CreWork> list = creWorkService.selectCreWorkList(creWork);
        ExcelUtil<CreWork> util = new ExcelUtil<CreWork>(CreWork.class);
        return util.exportExcel(list, "work");
    }

    /**
     * 获取作品管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('create:work:query')")
    @GetMapping(value = "/{workStoryId}")
    public AjaxResult getInfo(@PathVariable("workStoryId") Long workStoryId)
    {
        return AjaxResult.success(creWorkService.selectCreWorkById(workStoryId));
    }

    /**
     * 新增作品管理
     */
    @PreAuthorize("@ss.hasPermi('create:work:add')")
    @Log(title = "作品管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody CreWork creWork)
    {
        return toAjax(creWorkService.insertCreWork(creWork));
    }

    /**
     * 修改作品管理
     */
    @PreAuthorize("@ss.hasPermi('create:work:edit')")
    @Log(title = "作品管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody CreWork creWork)
    {
        return toAjax(creWorkService.updateCreWork(creWork));
    }

    /**
     * 删除作品管理
     */
    @PreAuthorize("@ss.hasPermi('create:work:remove')")
    @Log(title = "作品管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{workStoryIds}")
    public AjaxResult remove(@PathVariable Long[] workStoryIds)
    {
        return toAjax(creWorkService.deleteCreWorkByIds(workStoryIds));
    }
}
