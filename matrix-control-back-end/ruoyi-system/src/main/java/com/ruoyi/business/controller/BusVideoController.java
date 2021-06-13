package com.ruoyi.business.controller;

import java.util.List;

import com.ruoyi.common.core.domain.model.LoginUser;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.SecurityUtils;
import com.ruoyi.common.utils.ServletUtils;
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
import com.ruoyi.business.domain.BusVideo;
import com.ruoyi.business.service.IBusVideoService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 视频管理Controller
 *
 * @author Hocassian
 * @date 2020-10-10
 */
@RestController
@RequestMapping("/business/video")
public class BusVideoController extends BaseController {
    @Autowired
    private IBusVideoService busVideoService;


    /**
     * 查询视频管理列表
     */
    @PreAuthorize("@ss.hasPermi('business:video:list')")
    @GetMapping("/list")
    public TableDataInfo list(BusVideo busVideo) {
        startPage();
        List<BusVideo> list = busVideoService.selectBusVideoList(busVideo);
        return getDataTable(list);
    }

    /**
     * 导出视频管理列表
     */
    @PreAuthorize("@ss.hasPermi('business:video:export')")
    @Log(title = "视频管理", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(BusVideo busVideo) {
        List<BusVideo> list = busVideoService.selectBusVideoList(busVideo);
        ExcelUtil<BusVideo> util = new ExcelUtil<BusVideo>(BusVideo.class);
        return util.exportExcel(list, "video");
    }

    /**
     * 获取视频管理详细信息
     */
    @PreAuthorize("@ss.hasPermi('business:video:query')")
    @GetMapping(value = "/{videoId}")
    public AjaxResult getInfo(@PathVariable("videoId") Long videoId) {
        return AjaxResult.success(busVideoService.selectBusVideoById(videoId));
    }

    /**
     * 改变视频上下架状态
     */
    @PreAuthorize("@ss.hasPermi('business:video:status')")
    @PutMapping(value = "/status")
    public AjaxResult changeStatus(@RequestBody BusVideo busVideo) {
        return AjaxResult.success(busVideoService.changeBusVideoStatus(busVideo));
    }

    /**
     * 新增视频管理
     */
    @PreAuthorize("@ss.hasPermi('business:video:add')")
    @Log(title = "视频管理", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody BusVideo busVideo) {
        String username = SecurityUtils.getUsername();
        busVideo.setCreateBy(username);
        busVideo.setUpdateBy(username);
        busVideo.setCreateTime(DateUtils.getNowDate());
        busVideo.setUpdateTime(DateUtils.getNowDate());
        return toAjax(busVideoService.insertBusVideo(busVideo));
    }

    /**
     * 修改视频管理
     */
    @PreAuthorize("@ss.hasPermi('business:video:edit')")
    @Log(title = "视频管理", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody BusVideo busVideo) {
        String username = SecurityUtils.getUsername();
        busVideo.setUpdateBy(username);
        busVideo.setUpdateTime(DateUtils.getNowDate());
        return toAjax(busVideoService.updateBusVideo(busVideo));
    }

    /**
     * 删除视频管理
     */
    @PreAuthorize("@ss.hasPermi('business:video:remove')")
    @Log(title = "视频管理", businessType = BusinessType.DELETE)
    @DeleteMapping("/{videoIds}")
    public AjaxResult remove(@PathVariable Long[] videoIds) {
        return toAjax(busVideoService.deleteBusVideoByIds(videoIds));
    }
}
