package com.hocassian.people.controller.common;
import com.hocassian.people.config.web.BaseConfig;
import com.hocassian.people.config.web.ServerConfig;
import com.hocassian.people.transport.AjaxResult;

import com.hocassian.people.utils.FileUploadUtils;
import org.apache.tomcat.util.http.fileupload.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * 通用请求处理
 * 
 * @author ruoyi
 */
@RestController
public class CommonController
{

    @Autowired
    private ServerConfig serverConfig;

    /**
     * 上传请求
     */
    @PostMapping("/common/upload")
    public AjaxResult videoMatrixUploadFile(MultipartFile file) throws Exception
    {
        try
        {
            // 上传文件路径
            String filePath = BaseConfig.getUploadPath();
            // 上传并返回新文件名称
//            System.out.println("到此一游");
            String fileName = FileUploadUtils.unsignedUpload(filePath, file);
//            String url = serverConfig.getUrl() + fileName;
            AjaxResult ajax = AjaxResult.success();
            ajax.put("fileName", fileName);
//            ajax.put("url", url);
            return ajax;
        }
        catch (Exception e)
        {
            return AjaxResult.error(e.getMessage());
        }
    }
}
