CREATE TABLE pipelines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 自增主键
    name TEXT NOT NULL,                          -- 管线名称
    code TEXT NOT NULL UNIQUE,                   -- 桩号，唯一
    orientation TEXT,                            -- 平面转角
    length_km REAL,                              -- 里程 (单位: Km)
    depth_m REAL,                                -- 管道埋深 (单位: m)
    distance_position_des TEXT,              -- 离管道位置描述
    wall_thickness_mm REAL,                      -- 壁厚 (单位: mm)
    material TEXT，                                 -- 材质
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    qr_code_url TEXT
    -- 确保桩号唯一
);
CREATE TABLE contact_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- 自增主键
    pipeline_id INTEGER NOT NULL,                -- 管道ID，关联到pipelines表
    company TEXT,                                -- 公司名称
    hotline TEXT,                                -- 热线电话
    dispatch_number TEXT,                        -- 调度值班电话
    emergency_number TEXT,                       -- 免费报警电话
    FOREIGN KEY (pipeline_id) REFERENCES pipelines(id)  -- 外键关联pipelines表
);
