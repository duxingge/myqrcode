CREATE TABLE pipelines (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    name VARCHAR(100) NOT NULL COMMENT '管线名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '桩号',
    orientation VARCHAR(20) COMMENT '平面转角',
    length_km DECIMAL(10, 3) COMMENT '里程 (单位: Km)',
    depth_m DECIMAL(5, 2) COMMENT '管道埋深 (单位: m)',
    distance_position VARCHAR(10) COMMENT '离管道位置',
    wall_thickness_mm DECIMAL(4, 1) COMMENT '壁厚 (单位: mm)',
    material VARCHAR(50) COMMENT '材质'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管道基础信息表';

CREATE TABLE contact_info (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
    company VARCHAR(100) COMMENT '公司名称',
    hotline VARCHAR(20) COMMENT '热线电话',
    dispatch_number VARCHAR(20) COMMENT '调度值班电话',
    emergency_number VARCHAR(20) COMMENT '免费报警电话'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管道联系信息表';