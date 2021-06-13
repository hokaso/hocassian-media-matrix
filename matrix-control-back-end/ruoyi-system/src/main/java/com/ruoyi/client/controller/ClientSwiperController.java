package com.ruoyi.client.controller;

import com.ruoyi.business.domain.BusSwiper;
import com.ruoyi.client.service.IClientSwiperService;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 主页轮播图Controller
 * 
 * @author Hocassian
 * @date 2020-10-15
 */

@Api("轮播图管理")
@RestController
@RequestMapping("/client/swiper")
public class ClientSwiperController extends BaseController
{
    @Autowired
    private IClientSwiperService clientSwiperService;

    /**
     * 查询主页轮播图列表
     */
    @ApiOperation("获取轮播图列表")
    @PostMapping("/list")
    public TableDataInfo list(@RequestBody BusSwiper busSwiper)
    {
        startPage();
        List<BusSwiper> list = clientSwiperService.selectClientSwiperList(busSwiper);
        return getDataTable(list);
    }

    /**
     * 获取主页轮播图详细信息
     */
    @ApiOperation("根据id获取单个轮播图信息")
    @GetMapping(value = "/{swiperIds}")
    public AjaxResult getInfo(@PathVariable("swiperIds") Long swiperIds)
    {
        return AjaxResult.success(clientSwiperService.selectClientSwiperById(swiperIds));
    }
}
