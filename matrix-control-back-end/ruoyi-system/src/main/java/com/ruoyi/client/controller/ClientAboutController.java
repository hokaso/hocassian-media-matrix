package com.ruoyi.client.controller;

import com.ruoyi.client.mapper.ClientAboutMapper;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Api("信息管理")
@RestController
@RequestMapping("/client/about")
public class ClientAboutController extends BaseController {

    @Autowired
    private ClientAboutMapper clientAboutMapper;

    /**
     * 获取主页轮播图详细信息
     */
    @ApiOperation("获取当前矩阵基础信息")
    @GetMapping("/info")
    public AjaxResult getInfo()
    {
        return AjaxResult.success(clientAboutMapper.selectClientAbout());
    }

}
