package com.ruoyi.business.controller;

import com.ruoyi.business.domain.BusFriend;
import com.ruoyi.business.service.IBusFriendService;
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
 * 友情链接Controller
 * 
 * @author Hocassian
 * @date 2021-04-15
 */
@RestController
@RequestMapping("/business/friend")
public class BusFriendController extends BaseController
{
    @Autowired
    private IBusFriendService busFriendService;

    /**
     * 查询友情链接列表
     */
    @PreAuthorize("@ss.hasPermi('business:friend:list')")
    @GetMapping("/list")
    public TableDataInfo list(BusFriend busFriend)
    {
        startPage();
        List<BusFriend> list = busFriendService.selectBusFriendList(busFriend);
        return getDataTable(list);
    }

    /**
     * 导出友情链接列表
     */
    @PreAuthorize("@ss.hasPermi('business:friend:export')")
    @Log(title = "友情链接", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(BusFriend busFriend)
    {
        List<BusFriend> list = busFriendService.selectBusFriendList(busFriend);
        ExcelUtil<BusFriend> util = new ExcelUtil<BusFriend>(BusFriend.class);
        return util.exportExcel(list, "friend");
    }

    /**
     * 获取友情链接详细信息
     */
    @PreAuthorize("@ss.hasPermi('business:friend:query')")
    @GetMapping(value = "/{friendId}")
    public AjaxResult getInfo(@PathVariable("friendId") Long friendId)
    {
        return AjaxResult.success(busFriendService.selectBusFriendById(friendId));
    }

    /**
     * 新增友情链接
     */
    @PreAuthorize("@ss.hasPermi('business:friend:add')")
    @Log(title = "友情链接", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody BusFriend busFriend)
    {
        return toAjax(busFriendService.insertBusFriend(busFriend));
    }

    /**
     * 修改友情链接
     */
    @PreAuthorize("@ss.hasPermi('business:friend:edit')")
    @Log(title = "友情链接", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody BusFriend busFriend)
    {
        return toAjax(busFriendService.updateBusFriend(busFriend));
    }

    /**
     * 删除友情链接
     */
    @PreAuthorize("@ss.hasPermi('business:friend:remove')")
    @Log(title = "友情链接", businessType = BusinessType.DELETE)
	@DeleteMapping("/{friendIds}")
    public AjaxResult remove(@PathVariable Long[] friendIds)
    {
        return toAjax(busFriendService.deleteBusFriendByIds(friendIds));
    }
}
