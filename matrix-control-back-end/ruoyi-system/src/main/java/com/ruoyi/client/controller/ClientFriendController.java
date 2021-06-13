package com.ruoyi.client.controller;


import com.ruoyi.business.domain.BusFriend;
import com.ruoyi.client.mapper.ClientFriendMapper;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.page.TableDataInfo;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 主页轮播图Controller
 *
 * @author Hocassian
 * @date 2020-10-15
 */

@Api("友链管理")
@RestController
@RequestMapping("/client/friend")
public class ClientFriendController extends BaseController {

    @Autowired
    private ClientFriendMapper clientFriendMapper;

    /**
     * 查询平台列表
     */
    @ApiOperation("获取平台列表")
    @GetMapping("/platform")
    public TableDataInfo listPlatform()
    {
        startPage();
        List<BusFriend> list = clientFriendMapper.selectClientPlatformList();
        return getDataTable(list);
    }

    /**
     * 查询栏目列表
     */
    @ApiOperation("获取栏目列表")
    @GetMapping("/column")
    public TableDataInfo listColumn()
    {
        startPage();
        List<BusFriend> list = clientFriendMapper.selectClientColumnList();
        return getDataTable(list);
    }


}
