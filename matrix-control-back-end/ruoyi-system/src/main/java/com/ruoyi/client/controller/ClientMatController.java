package com.ruoyi.client.controller;

import com.alibaba.fastjson.JSON;
import com.ruoyi.client.mapper.ClientAudioMapper;
import com.ruoyi.client.mapper.ClientClipMapper;
import com.ruoyi.client.mapper.ClientImageMapper;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.material.domain.MatAudio;
import com.ruoyi.material.domain.MatClip;
import com.ruoyi.material.domain.MatImage;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Api("视频素材")
@RestController
@RequestMapping("/client/material")

public class ClientMatController extends BaseController {

    @Autowired
    private ClientClipMapper clientClipMapper;

    @Autowired
    private ClientAudioMapper clientAudioMapper;

    @Autowired
    private ClientImageMapper clientImageMapper;

    /**
     * 查询视频管理列表
     */
    @ApiOperation("获取视频列表")
    @GetMapping("/clip/list")
    public TableDataInfo listClip(MatClip matClip)
    {
        startPage();
        List<MatClip> list = clientClipMapper.selectClientClipList(matClip);
        return getDataTable(list);
    }

    /**
     * 查询视频管理列表
     */
    @ApiOperation("获取视频关键字集合")
    @GetMapping("/clip/keywords")
    public AjaxResult keywordsClip()
    {
        List<String> haveFilter = new ArrayList<>();
        for (String word : clientClipMapper.selectClipKeywords()){
            List<String> object = JSON.parseArray(word, String.class);
            List<String> collect = object.stream().filter(s -> s.length() < 5 && s.length() > 1).collect(Collectors.toList());
            haveFilter.addAll(collect);
        }
        List<String> noDuplicates = haveFilter.stream().distinct().collect(Collectors.toList());
        return AjaxResult.success(noDuplicates);
    }

    /**
     * 为音频页面提供简单的图片背景
     */
    @ApiOperation("获取图片路径集合")
    @GetMapping("/image/colorful")
    public AjaxResult colorfulImage()
    {
        return AjaxResult.success(clientImageMapper.selectImageUrls());
    }

    /**
     * 查询音频管理列表
     */
    @ApiOperation("获取视频列表")
    @GetMapping("/audio/list")
    public TableDataInfo listAudio(MatAudio matAudio)
    {
        startPage();
        List<MatAudio> list = clientAudioMapper.selectClientAudioList(matAudio);
        return getDataTable(list);
    }

    /**
     * 查询音频管理列表
     */
    @ApiOperation("获取音频关键字集合")
    @GetMapping("/audio/keywords")
    public AjaxResult keywordsAudio()
    {
        List<String> haveFilter = new ArrayList<>();
        for (String word : clientAudioMapper.selectAudioKeywords()){
            List<String> object = JSON.parseArray(word, String.class);
            List<String> collect = object.stream().filter(s -> s.length() < 5 && s.length() > 1).collect(Collectors.toList());
            haveFilter.addAll(collect);
        }
        List<String> noDuplicates = haveFilter.stream().distinct().collect(Collectors.toList());
        return AjaxResult.success(noDuplicates);
    }

    /**
     * 查询音频管理列表
     */
    @ApiOperation("获取视频列表")
    @GetMapping("/image/list")
    public TableDataInfo listImage(MatImage matImage)
    {
        startPage();
        List<MatImage> list = clientImageMapper.selectClientImageList(matImage);
        return getDataTable(list);
    }

    /**
     * 查询图片管理列表
     */
    @ApiOperation("获取图片关键字集合")
    @GetMapping("/image/keywords")
    public AjaxResult keywordsImage()
    {
        List<String> haveFilter = new ArrayList<>();
        for (String word : clientImageMapper.selectImageKeywords()){
            List<String> object = JSON.parseArray(word, String.class);
            List<String> collect = object.stream().filter(s -> s.length() < 5 && s.length() > 1).collect(Collectors.toList());
            haveFilter.addAll(collect);
        }
        List<String> noDuplicates = haveFilter.stream().distinct().collect(Collectors.toList());
        return AjaxResult.success(noDuplicates);
    }

}
