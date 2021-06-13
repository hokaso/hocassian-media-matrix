package com.hocassian.people.controller.base;

import com.hocassian.people.transport.AjaxResult;
import com.hocassian.people.transport.Result;
import com.hocassian.people.utils.HttpStatus;

import java.util.List;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-16 13:41
 */
public class BaseController {


    /**
     * 响应请求分页数据
     */
    @SuppressWarnings({ "rawtypes"})
    protected Result getDataResult(List<?> list)
    {
        Result rspData = new Result();
        rspData.setCode(HttpStatus.SUCCESS);
        rspData.setMsg("查询成功");
        rspData.setRows(list);
        return rspData;
    }

    /**
     * 响应返回结果
     *
     * @param rows 影响行数
     * @return 操作结果
     */
    protected AjaxResult toAjax(int rows)
    {
        return rows > 0 ? AjaxResult.success() : AjaxResult.error();
    }
}
