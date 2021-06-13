package com.ruoyi.business.controller;

import java.util.List;


import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.common.utils.SecurityUtils;
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
import com.ruoyi.business.domain.BusSwiper;
import com.ruoyi.business.service.IBusSwiperService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 主页轮播图Controller
 * 
 * @author Hocassian
 * @date 2020-10-15
 */
@RestController
@RequestMapping("/business/swiper")
public class BusSwiperController extends BaseController
{
    @Autowired
    private IBusSwiperService busSwiperService;


    /**
     * 查询主页轮播图列表
     */
    @PreAuthorize("@ss.hasPermi('business:swiper:list')")
    @GetMapping("/list")
    public TableDataInfo list(BusSwiper busSwiper)
    {
        startPage();
        List<BusSwiper> list = busSwiperService.selectBusSwiperList(busSwiper);
        return getDataTable(list);
    }

    /**
     * 导出主页轮播图列表
     */
    @PreAuthorize("@ss.hasPermi('business:swiper:export')")
    @Log(title = "主页轮播图", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(BusSwiper busSwiper)
    {
        List<BusSwiper> list = busSwiperService.selectBusSwiperList(busSwiper);
        ExcelUtil<BusSwiper> util = new ExcelUtil<BusSwiper>(BusSwiper.class);
        return util.exportExcel(list, "swiper");
    }

    /**
     * 获取主页轮播图详细信息
     */
    @PreAuthorize("@ss.hasPermi('business:swiper:query')")
    @GetMapping(value = "/{swiperIds}")
    public AjaxResult getInfo(@PathVariable("swiperIds") Long swiperIds)
    {
        return AjaxResult.success(busSwiperService.selectBusSwiperById(swiperIds));
    }

    /**
     * 改变轮播图上下架状态
     */
    @PreAuthorize("@ss.hasPermi('business:swiper:status')")
    @PutMapping(value = "/status")
    public AjaxResult changeStatus(@RequestBody BusSwiper busSwiper){
        return AjaxResult.success(busSwiperService.changeBusSwiperStatus(busSwiper));
    }

    /**
     * 新增主页轮播图
     */
    @PreAuthorize("@ss.hasPermi('business:swiper:add')")
    @Log(title = "主页轮播图", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody BusSwiper busSwiper)
    {
        String username = SecurityUtils.getUsername();
        busSwiper.setCreateBy(username);
        busSwiper.setUpdateBy(username);
        busSwiper.setCreateAt(DateUtils.getNowDate());
        busSwiper.setUpdateAt(DateUtils.getNowDate());
        return toAjax(busSwiperService.insertBusSwiper(busSwiper));
    }

    /**
     * 修改主页轮播图
     */
    @PreAuthorize("@ss.hasPermi('business:swiper:edit')")
    @Log(title = "主页轮播图", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody BusSwiper busSwiper)
    {
        String username = SecurityUtils.getUsername();
        busSwiper.setUpdateBy(username);
        busSwiper.setUpdateAt(DateUtils.getNowDate());
        return toAjax(busSwiperService.updateBusSwiper(busSwiper));
    }

    /**
     * 删除主页轮播图
     */
    @PreAuthorize("@ss.hasPermi('business:swiper:remove')")
    @Log(title = "主页轮播图", businessType = BusinessType.DELETE)
	@DeleteMapping("/{swiperIds}")
    public AjaxResult remove(@PathVariable Long[] swiperIds)
    {
        return toAjax(busSwiperService.deleteBusSwiperByIds(swiperIds));
    }
}
