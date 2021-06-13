package com.ruoyi.business.controller;

import java.util.List;

import com.ruoyi.common.core.domain.model.LoginUser;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.common.utils.ServletUtils;
import com.ruoyi.common.utils.spring.SpringUtils;
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
import com.ruoyi.business.domain.BusChannel;
import com.ruoyi.business.service.IBusChannelService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 频道管理Controller
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
@RestController
@RequestMapping("/business/channel")
public class BusChannelController extends BaseController
{
    @Autowired
    private IBusChannelService busChannelService;



    /**
     * 查询频道管理列表
     */
    @PreAuthorize("@ss.hasPermi('business:channel:list')")
    @GetMapping("/list")
    public TableDataInfo list(BusChannel busChannel)
    {
        startPage();
        List<BusChannel> list = busChannelService.selectBusChannelList(busChannel);
        return getDataTable(list);
    }

    /**
     * 导出频道管理列表
     */
    @PreAuthorize("@ss.hasPermi('business:channel:export')")
    @Log(title = "频道管理", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(BusChannel busChannel)
    {
        List<BusChannel> list = busChannelService.selectBusChannelList(busChannel);
        ExcelUtil<BusChannel> util = new ExcelUtil<BusChannel>(BusChannel.class);
        return util.exportExcel(list, "channel");
    }

    /**
     * 获取频道管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('business:channel:query')")
    @GetMapping(value = "/{channelId}")
    public AjaxResult getInfo(@PathVariable("channelId") Long channelId)
    {
        return AjaxResult.success(busChannelService.selectBusChannelById(channelId));
    }

    /**
     * 新增频道管理
     */
    @PreAuthorize("@ss.hasPermi('business:channel:add')")
    @Log(title = "频道管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody BusChannel busChannel)
    {
        String username = SecurityUtils.getUsername();
        busChannel.setCreateBy(username);
        busChannel.setCreateTime(DateUtils.getNowDate());
        busChannel.setUpdateTime(DateUtils.getNowDate());
        busChannel.setUpdateBy(username);
        return toAjax(busChannelService.insertBusChannel(busChannel));
    }

    /**
     * 修改频道管理
     */
    @PreAuthorize("@ss.hasPermi('business:channel:edit')")
    @Log(title = "频道管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody BusChannel busChannel)
    {

        String username = SecurityUtils.getUsername();
        busChannel.setUpdateBy(username);
        busChannel.setUpdateTime(DateUtils.getNowDate());
        return toAjax(busChannelService.updateBusChannel(busChannel));
    }

    /**
     * 删除频道管理
     */
    @PreAuthorize("@ss.hasPermi('business:channel:remove')")
    @Log(title = "频道管理", businessType = BusinessType.DELETE)
	@DeleteMapping("/{channelIds}")
    public AjaxResult remove(@PathVariable Long[] channelIds)
    {
        return toAjax(busChannelService.deleteBusChannelByIds(channelIds));
    }
}
