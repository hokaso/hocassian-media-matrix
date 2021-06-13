package com.ruoyi.material.controller;

import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.core.redis.RedisCache;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.material.domain.MatClip;
import com.ruoyi.material.service.IMatClipService;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;

/**
 * 视频素材Controller
 * 
 * @author Hocassian
 * @date 2021-02-22
 */
@RestController
@RequestMapping("/material/clip")
public class MatClipController extends BaseController
{
    @Autowired
    private IMatClipService matClipService;

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Autowired
    private RedisCache redisCache;

    /**
     * 查询视频素材列表
     */
    @PreAuthorize("@ss.hasPermi('material:clip:list')")
    @GetMapping("/list")
    public TableDataInfo list(MatClip matClip)
    {
        startPage();
        List<MatClip> list = matClipService.selectMatClipList(matClip);
        return getDataTable(list);
    }

    /**
     * 导出视频素材列表
     */
    @PreAuthorize("@ss.hasPermi('material:clip:export')")
    @Log(title = "视频素材", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(MatClip matClip)
    {
        List<MatClip> list = matClipService.selectMatClipList(matClip);
        ExcelUtil<MatClip> util = new ExcelUtil<MatClip>(MatClip.class);
        return util.exportExcel(list, "clip");
    }

    /**
     * 获取视频素材详细信息
     */
    @PreAuthorize("@ss.hasPermi('material:clip:query')")
    @GetMapping(value = "/{materialId}")
    public AjaxResult getInfo(@PathVariable("materialId") Long materialId)
    {
        return AjaxResult.success(matClipService.selectMatClipById(materialId));
    }

    /**
     * 改变素材状态
     */
    @PreAuthorize("@ss.hasPermi('material:clip:add')")
    @PutMapping(value = "/mode")
    public AjaxResult changeStatus(@RequestBody MatClip matClip) {
        return AjaxResult.success(matClipService.changeMatClipStatus(matClip));
    }

    /**
     * 导入/处理素材（批操作，其中：1导入，2处理，3导出）
     */
    @PreAuthorize("@ss.hasPermi('material:clip:add')")
    @GetMapping(value = "/option/{optionalId}")
    public AjaxResult option(@PathVariable("optionalId") Long optionalId)
    {
        int IMPORT_CLIP = 1;
        int BATCH_CLIP = 2;
        int TRANSLATE_CLIP = 3;

        HashMap<String, Object> map=new HashMap<>(16);
        Long importClip = redisCache.getCacheObject("importClip");
        Long batchClip = redisCache.getCacheObject("batchClip");
        Long translateClip = redisCache.getCacheObject("translateClip");

        if (importClip != null && optionalId == IMPORT_CLIP && importClip == IMPORT_CLIP){
            return AjaxResult.error("导入正在进行中，请等待当前处理完毕后再试！");
        }
        else if (optionalId == IMPORT_CLIP) {
            redisCache.setCacheObject("importClip", optionalId);
            map.put("optional_id", optionalId);
        }

        if (batchClip != null && optionalId == BATCH_CLIP && batchClip == BATCH_CLIP){
            return AjaxResult.error("批处理正在进行中，请等待当前处理完毕后再试！");
        }
        else if (optionalId == BATCH_CLIP) {
            redisCache.setCacheObject("batchClip", optionalId);
            map.put("optional_id", optionalId);
        }

        if (translateClip != null && optionalId == TRANSLATE_CLIP && translateClip == TRANSLATE_CLIP){
            return AjaxResult.error("批处理正在进行中，请等待当前处理完毕后再试！");
        }
        else if (optionalId == TRANSLATE_CLIP) {
            redisCache.setCacheObject("translateClip", optionalId);
            map.put("optional_id", optionalId);
        }

        rabbitTemplate.convertAndSend("clipOptionalExchange", "clipOptionalRouting", map);
        return AjaxResult.success("处理指令推送成功！");
    }

    /**
     * 确定批处理那三个按钮的状态
     */
    @GetMapping("/status")
    public AjaxResult status()
    {
        HashMap<String, Object> map=new HashMap<>(16);
        Long importClip = redisCache.getCacheObject("importClip");
        Long batchClip = redisCache.getCacheObject("batchClip");
        Long translateClip = redisCache.getCacheObject("translateClip");
        map.put("importClip", importClip);
        map.put("batchClip", batchClip);
        map.put("translateClip", translateClip);
        return AjaxResult.success(map);
    }

    /**
     * 新增视频素材
     */
    @PreAuthorize("@ss.hasPermi('material:clip:add')")
    @Log(title = "视频素材", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody MatClip matClip)
    {
        return toAjax(matClipService.insertMatClip(matClip));
    }

    /**
     * 修改视频素材
     */
    @PreAuthorize("@ss.hasPermi('material:clip:edit')")
    @Log(title = "视频素材", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody MatClip matClip)
    {
        return toAjax(matClipService.updateMatClip(matClip));
    }

    /**
     * 删除视频素材
     */
    @PreAuthorize("@ss.hasPermi('material:clip:remove')")
    @Log(title = "视频素材", businessType = BusinessType.DELETE)
	@DeleteMapping("/{materialIds}")
    public AjaxResult remove(@PathVariable Long[] materialIds)
    {
        return toAjax(matClipService.deleteMatClipByIds(materialIds));
    }
}
