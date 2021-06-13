package com.ruoyi.client.controller;

import com.ruoyi.business.domain.BusVideo;
import com.ruoyi.client.service.IClientVideoService;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 视频管理Controller
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
@Api("视频管理")
@RestController
@RequestMapping("/client/video")
public class ClientVideoController extends BaseController
{
    @Autowired
    private IClientVideoService clientVideoService;

    /**
     * 查询视频管理列表
     */
    @ApiOperation("获取视频列表")
    @GetMapping("/list")
    public TableDataInfo list(BusVideo busVideo)
    {
        startPage();
        List<BusVideo> list = clientVideoService.selectClientVideoList(busVideo);
        return getDataTable(list);
    }

    /**
     * 获取视频管理详细信息
     */
    @ApiOperation("根据id获取单个视频信息")
    @GetMapping(value = "/{videoId}")
    public AjaxResult getInfo(@PathVariable("videoId") Long videoId)
    {
        return AjaxResult.success(clientVideoService.selectClientVideoById(videoId));
    }
}
