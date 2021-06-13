package com.hocassian.people.utils;

import com.hocassian.people.config.web.BaseConfig;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;

/**
 * 文件上传工具类
 *
 * @author ruoyi
 */
public class FileUploadUtils
{
    /**
     * 默认大小 50M
     */
    public static final long DEFAULT_MAX_SIZE = 50 * 1024 * 1024;

    /**
     * 默认的文件名最大长度 100
     */
    public static final int DEFAULT_FILE_NAME_LENGTH = 100;

    /**
     * 默认上传的地址
     */
    private static String defaultBaseDir = BaseConfig.getProfile();

    public static void setDefaultBaseDir(String defaultBaseDir)
    {
        FileUploadUtils.defaultBaseDir = defaultBaseDir;
    }

    public static String getDefaultBaseDir()
    {
        return defaultBaseDir;
    }

    /**
     * 根据文件路径上传（无新增文件夹、无文件大小限制、无上传文件类型限制）
     *
     * @param baseDir 相对应用的基目录
     * @param file 上传的文件
     * @return 文件名称
     * @throws IOException
     */
    public static final String unsignedUpload(String baseDir, MultipartFile file) throws IOException
    {
        try
        {
            // 文件名
            String fileName = file.getOriginalFilename();
            // 后缀名
            assert fileName != null;
            String suffixName = fileName.substring(fileName.lastIndexOf("."));
            // 新文件名

            SnowflakeIdWorker snowflakeIdWorker = new SnowflakeIdWorker();
            fileName = snowflakeIdWorker.nextId() + suffixName;
            File dest = new File(baseDir + fileName);
            if (!dest.getParentFile().exists()) {
                // 若不存在该文件夹，则创建一个
                boolean e = dest.getParentFile().mkdirs();
            }
            file.transferTo(dest);
            System.out.println("返回的文件URL：" + fileName);

            return fileName;
        }
        catch (Exception e)
        {
            throw new IOException(e.getMessage(), e);
        }
    }

}
