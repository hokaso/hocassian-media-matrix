package com.ruoyi.material.controller;

import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.core.redis.RedisCache;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.material.domain.MatAudio;
import com.ruoyi.material.service.IMatAudioService;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;

/**
 * 音频素材Controller
 * 
 * @author Hocassian
 * @date 2021-02-28
 */
@RestController
@RequestMapping("/material/audio")
public class MatAudioController extends BaseController
{
    @Autowired
    private IMatAudioService matAudioService;

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Autowired
    private RedisCache redisCache;

    /**
     * 查询音频素材列表
     */
    @PreAuthorize("@ss.hasPermi('material:audio:list')")
    @GetMapping("/list")
    public TableDataInfo list(MatAudio matAudio)
    {
        startPage();
        List<MatAudio> list = matAudioService.selectMatAudioList(matAudio);
        return getDataTable(list);
    }

    /**
     * 导出音频素材列表
     */
    @PreAuthorize("@ss.hasPermi('material:audio:export')")
    @Log(title = "音频素材", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(MatAudio matAudio)
    {
        List<MatAudio> list = matAudioService.selectMatAudioList(matAudio);
        ExcelUtil<MatAudio> util = new ExcelUtil<MatAudio>(MatAudio.class);
        return util.exportExcel(list, "audio");
    }

    /**
     * 获取音频素材详细信息
     */
    @PreAuthorize("@ss.hasPermi('material:audio:query')")
    @GetMapping(value = "/{audioId}")
    public AjaxResult getInfo(@PathVariable("audioId") Long audioId)
    {
        return AjaxResult.success(matAudioService.selectMatAudioById(audioId));
    }

    /**
     * 改变素材状态
     */
    @PreAuthorize("@ss.hasPermi('business:audio:add')")
    @PutMapping(value = "/mode")
    public AjaxResult changeStatus(@RequestBody MatAudio matAudio) {
        return AjaxResult.success(matAudioService.changeMatAudioStatus(matAudio));
    }

    /**
     * 导入/处理素材（批操作，其中：1导入，2处理）
     */
    @PreAuthorize("@ss.hasPermi('business:audio:add')")
    @GetMapping(value = "/option/{optionalId}")
    public AjaxResult option(@PathVariable("optionalId") Long optionalId)
    {
        HashMap<String, Object> map=new HashMap<>(16);
        Long importAudio = redisCache.getCacheObject("importAudio");
        Long batchAudio = redisCache.getCacheObject("batchAudio");

        if (importAudio != null && optionalId == 1 && importAudio == 1){
            return AjaxResult.error("导入正在进行中，请等待当前处理完毕后再试！");
        }
        else if (optionalId == 1) {
            redisCache.setCacheObject("importAudio", optionalId);
            map.put("optional_id", optionalId);
        }

        if (batchAudio != null && optionalId == 2 && batchAudio == 2){
            return AjaxResult.error("批处理正在进行中，请等待当前处理完毕后再试！");
        }
        else if (optionalId == 2) {
            redisCache.setCacheObject("batchAudio", optionalId);
            map.put("optional_id", optionalId);
        }

        rabbitTemplate.convertAndSend("audioOptionalExchange", "audioOptionalRouting", map);
        return AjaxResult.success("处理指令推送成功！");
    }

    /**
     * 确定批处理那两个按钮的状态
     */
    @GetMapping("/status")
    public AjaxResult status()
    {
        HashMap<String, Object> map=new HashMap<>(16);
        Long importAudio = redisCache.getCacheObject("importAudio");
        Long batchAudio = redisCache.getCacheObject("batchAudio");
        map.put("importAudio", importAudio);
        map.put("batchAudio", batchAudio);
        return AjaxResult.success(map);
    }

    /**
     * 新增音频素材
     */
    @PreAuthorize("@ss.hasPermi('material:audio:add')")
    @Log(title = "音频素材", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody MatAudio matAudio)
    {
        return toAjax(matAudioService.insertMatAudio(matAudio));
    }

    /**
     * 修改音频素材
     */
    @PreAuthorize("@ss.hasPermi('material:audio:edit')")
    @Log(title = "音频素材", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody MatAudio matAudio)
    {
        return toAjax(matAudioService.updateMatAudio(matAudio));
    }

    /**
     * 删除音频素材
     */
    @PreAuthorize("@ss.hasPermi('material:audio:remove')")
    @Log(title = "音频素材", businessType = BusinessType.DELETE)
	@DeleteMapping("/{audioIds}")
    public AjaxResult remove(@PathVariable Long[] audioIds)
    {
        return toAjax(matAudioService.deleteMatAudioByIds(audioIds));
    }
}
