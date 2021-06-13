package com.ruoyi.publish.controller;

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
import com.ruoyi.publish.domain.PubUnit;
import com.ruoyi.publish.service.IPubUnitService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 媒体单位Controller
 * 
 * @author Hocassian
 * @date 2020-11-24
 */
@RestController
@RequestMapping("/publish/unit")
public class PubUnitController extends BaseController
{
    @Autowired
    private IPubUnitService pubUnitService;

    /**
     * 查询媒体单位列表
     */
    @PreAuthorize("@ss.hasPermi('publish:unit:list')")
    @GetMapping("/list")
    public TableDataInfo list(PubUnit pubUnit)
    {
        startPage();
        List<PubUnit> list = pubUnitService.selectPubUnitList(pubUnit);
        return getDataTable(list);
    }

    /**
     * 导出媒体单位列表
     */
    @PreAuthorize("@ss.hasPermi('publish:unit:export')")
    @Log(title = "媒体单位", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(PubUnit pubUnit)
    {
        List<PubUnit> list = pubUnitService.selectPubUnitList(pubUnit);
        ExcelUtil<PubUnit> util = new ExcelUtil<PubUnit>(PubUnit.class);
        return util.exportExcel(list, "unit");
    }

    /**
     * 获取媒体单位详细信息
     */
    @PreAuthorize("@ss.hasPermi('publish:unit:query')")
    @GetMapping(value = "/{unitId}")
    public AjaxResult getInfo(@PathVariable("unitId") Long unitId)
    {
        return AjaxResult.success(pubUnitService.selectPubUnitById(unitId));
    }

    /**
     * 新增媒体单位
     */
    @PreAuthorize("@ss.hasPermi('publish:unit:add')")
    @Log(title = "媒体单位", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody PubUnit pubUnit)
    {
        return toAjax(pubUnitService.insertPubUnit(pubUnit));
    }

    /**
     * 修改媒体单位
     */
    @PreAuthorize("@ss.hasPermi('publish:unit:edit')")
    @Log(title = "媒体单位", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody PubUnit pubUnit)
    {
        return toAjax(pubUnitService.updatePubUnit(pubUnit));
    }

    /**
     * 删除媒体单位
     */
    @PreAuthorize("@ss.hasPermi('publish:unit:remove')")
    @Log(title = "媒体单位", businessType = BusinessType.DELETE)
	@DeleteMapping("/{unitIds}")
    public AjaxResult remove(@PathVariable Long[] unitIds)
    {
        return toAjax(pubUnitService.deletePubUnitByIds(unitIds));
    }
}
