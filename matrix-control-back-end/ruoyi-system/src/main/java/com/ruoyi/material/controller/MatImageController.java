package com.ruoyi.material.controller;

import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.core.redis.RedisCache;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.material.domain.MatImage;
import com.ruoyi.material.service.IMatImageService;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;

/**
 * 图片素材Controller
 * 
 * @author Hocassian
 * @date 2021-03-04
 */
@RestController
@RequestMapping("/material/image")
public class MatImageController extends BaseController
{
    @Autowired
    private IMatImageService matImageService;

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Autowired
    private RedisCache redisCache;

    /**
     * 查询图片素材列表
     */
    @PreAuthorize("@ss.hasPermi('material:image:list')")
    @GetMapping("/list")
    public TableDataInfo list(MatImage matImage)
    {
        startPage();
        List<MatImage> list = matImageService.selectMatImageList(matImage);
        return getDataTable(list);
    }

    /**
     * 导出图片素材列表
     */
    @PreAuthorize("@ss.hasPermi('material:image:export')")
    @Log(title = "图片素材", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(MatImage matImage)
    {
        List<MatImage> list = matImageService.selectMatImageList(matImage);
        ExcelUtil<MatImage> util = new ExcelUtil<MatImage>(MatImage.class);
        return util.exportExcel(list, "image");
    }

    /**
     * 获取图片素材详细信息
     */
    @PreAuthorize("@ss.hasPermi('material:image:query')")
    @GetMapping(value = "/{imageId}")
    public AjaxResult getInfo(@PathVariable("imageId") Long imageId)
    {
        return AjaxResult.success(matImageService.selectMatImageById(imageId));
    }

    /**
     * 改变素材状态
     */
    @PreAuthorize("@ss.hasPermi('material:image:add')")
    @PutMapping(value = "/mode")
    public AjaxResult changeStatus(@RequestBody MatImage matImage) {
        return AjaxResult.success(matImageService.changeMatImageStatus(matImage));
    }

    /**
     * 导入/处理素材（批操作，其中：1导入，2处理）
     */
    @PreAuthorize("@ss.hasPermi('material:image:add')")
    @GetMapping(value = "/option/{optionalId}")
    public AjaxResult option(@PathVariable("optionalId") Long optionalId)
    {
        HashMap<String, Object> map=new HashMap<>(16);
        Long importImage = redisCache.getCacheObject("importImage");
        Long batchImage = redisCache.getCacheObject("batchImage");

        if (importImage != null && optionalId == 1 && importImage == 1){
            return AjaxResult.error("导入正在进行中，请等待当前处理完毕后再试！");
        }
        else if (optionalId == 1) {
            redisCache.setCacheObject("importImage", optionalId);
            map.put("optional_id", optionalId);
        }

        if (batchImage != null && optionalId == 2 && batchImage == 2){
            return AjaxResult.error("批处理正在进行中，请等待当前处理完毕后再试！");
        }
        else if (optionalId == 2) {
            redisCache.setCacheObject("batchImage", optionalId);
            map.put("optional_id", optionalId);
        }

        rabbitTemplate.convertAndSend("imageOptionalExchange", "imageOptionalRouting", map);
        return AjaxResult.success("处理指令推送成功！");
    }

    /**
     * 确定批处理那两个按钮的状态
     */
    @GetMapping("/status")
    public AjaxResult status()
    {
        HashMap<String, Object> map=new HashMap<>(16);
        Long importImage = redisCache.getCacheObject("importImage");
        Long batchImage = redisCache.getCacheObject("batchImage");
        map.put("importImage", importImage);
        map.put("batchImage", batchImage);
        return AjaxResult.success(map);
    }


    /**
     * 新增图片素材
     */
    @PreAuthorize("@ss.hasPermi('material:image:add')")
    @Log(title = "图片素材", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody MatImage matImage)
    {
        return toAjax(matImageService.insertMatImage(matImage));
    }

    /**
     * 修改图片素材
     */
    @PreAuthorize("@ss.hasPermi('material:image:edit')")
    @Log(title = "图片素材", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody MatImage matImage)
    {
        return toAjax(matImageService.updateMatImage(matImage));
    }

    /**
     * 删除图片素材
     */
    @PreAuthorize("@ss.hasPermi('material:image:remove')")
    @Log(title = "图片素材", businessType = BusinessType.DELETE)
	@DeleteMapping("/{imageIds}")
    public AjaxResult remove(@PathVariable Long[] imageIds)
    {
        return toAjax(matImageService.deleteMatImageByIds(imageIds));
    }
}
