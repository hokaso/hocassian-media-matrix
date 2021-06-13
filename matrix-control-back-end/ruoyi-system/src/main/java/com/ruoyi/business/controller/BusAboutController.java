package com.ruoyi.business.controller;

import com.ruoyi.business.domain.BusAbout;
import com.ruoyi.business.service.IBusAboutService;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 信息管理Controller
 * 
 * @author Hocassian
 * @date 2021-04-22
 */
@RestController
@RequestMapping("/business/about")
public class BusAboutController extends BaseController
{
    @Autowired
    private IBusAboutService busAboutService;

    /**
     * 查询信息管理列表
     */
    @PreAuthorize("@ss.hasPermi('business:about:list')")
    @GetMapping("/list")
    public TableDataInfo list(BusAbout busAbout)
    {
        startPage();
        List<BusAbout> list = busAboutService.selectBusAboutList(busAbout);
        return getDataTable(list);
    }

    /**
     * 导出信息管理列表
     */
    @PreAuthorize("@ss.hasPermi('business:about:export')")
    @Log(title = "信息管理", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(BusAbout busAbout)
    {
        List<BusAbout> list = busAboutService.selectBusAboutList(busAbout);
        ExcelUtil<BusAbout> util = new ExcelUtil<BusAbout>(BusAbout.class);
        return util.exportExcel(list, "about");
    }

    /**
     * 获取信息管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('business:about:query')")
    @GetMapping(value = "/{aboutId}")
    public AjaxResult getInfo(@PathVariable("aboutId") Long aboutId)
    {
        return AjaxResult.success(busAboutService.selectBusAboutById(aboutId));
    }

    /**
     * 新增信息管理
     */
    @PreAuthorize("@ss.hasPermi('business:about:add')")
    @Log(title = "信息管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody BusAbout busAbout)
    {
        return toAjax(busAboutService.insertBusAbout(busAbout));
    }

    /**
     * 修改信息管理
     */
    @PreAuthorize("@ss.hasPermi('business:about:edit')")
    @Log(title = "信息管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody BusAbout busAbout)
    {
        return toAjax(busAboutService.updateBusAbout(busAbout));
    }

    /**
     * 删除信息管理
     */
    @PreAuthorize("@ss.hasPermi('business:about:remove')")
    @Log(title = "信息管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{aboutIds}")
    public AjaxResult remove(@PathVariable Long[] aboutIds)
    {
        return toAjax(busAboutService.deleteBusAboutByIds(aboutIds));
    }
}
