package com.hocassian.people.utils;
import org.springframework.stereotype.Component;

/**
 * 描述: Twitter的分布式自增ID雪花算法snowflake (Java版)
 * https://github.com/souyunku/SnowFlake
 * @create 2018-03-13 12:37
 **/
@Component
public class SnowflakeIdWorker {

    /**
     * 起始的时间戳
     */
    private final static long START_STMP = 1480166465631L;
//    private final static long START_STMP = System.currentTimeMillis();

    /**
     * 每一部分占用的位数
     *
     * 序列号占用的位数
     * 机器标识占用的位数
     * 数据中心占用的位数
     */
    private final static long SEQUENCE_BIT = 12;
    private final static long MACHINE_BIT = 5;
    private final static long DATACENTER_BIT = 5;

    /**
     * 每一部分的最大值
     */
    private final static long MAX_DATACENTER_NUM = ~(-1L << DATACENTER_BIT);
    private final static long MAX_MACHINE_NUM = ~(-1L << MACHINE_BIT);
    private final static long MAX_SEQUENCE = ~(-1L << SEQUENCE_BIT);

    /**
     * 每一部分向左的位移
     */
    private final static long MACHINE_LEFT = SEQUENCE_BIT;
    private final static long DATA_CENTER_LEFT = SEQUENCE_BIT + MACHINE_BIT;
    private final static long TIMESTMP_LEFT = DATA_CENTER_LEFT + DATACENTER_BIT;

    /**
     * 每一部分向左的位移
     *
     * 数据中心
     * 机器标识
     * 序列号
     * 上一次时间戳
     */
    private long datacenterId;
    private long machineId;
    private long sequence = 0L;
    private long lastStmp = -1L;

    public SnowflakeIdWorker() {
        if (2 > MAX_DATACENTER_NUM) {
            throw new IllegalArgumentException("datacenterId can't be greater than MAX_DATACENTER_NUM or less than 0");
        }
        if (3 > MAX_MACHINE_NUM) {
            throw new IllegalArgumentException("machineId can't be greater than MAX_MACHINE_NUM or less than 0");
        }
        this.datacenterId = 2;
        this.machineId = 3;
    }

    /**
     * 产生下一个ID
     *我改返回类型，long->String
     * @return
     *
     * 时间戳部分
     * 数据中心部分
     * 机器标识部分
     * 序列号部分
     */
    public synchronized String nextId() {
        long currStmp = getNewstmp();
        if (currStmp < lastStmp) {
            throw new RuntimeException("Clock moved backwards.  Refusing to generate id");
        }

        if (currStmp == lastStmp) {
            //相同毫秒内，序列号自增
            sequence = (sequence + 1) & MAX_SEQUENCE;
            //同一毫秒的序列数已经达到最大
            if (sequence == 0L) {
                currStmp = getNextMill();
            }
        } else {
            //不同毫秒内，序列号置为0
            sequence = 0L;
        }

        lastStmp = currStmp;

        return String.valueOf((currStmp - START_STMP) << TIMESTMP_LEFT
                | datacenterId << DATA_CENTER_LEFT
                | machineId << MACHINE_LEFT
                | sequence);
    }

    private long getNextMill() {
        long mill = getNewstmp();
        while (mill <= lastStmp) {
            mill = getNewstmp();
        }
        return mill;
    }

    private long getNewstmp() {
        return System.currentTimeMillis();
    }


}