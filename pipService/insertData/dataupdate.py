import sqlite3
import pandas as pd
from datetime import datetime


FILE_PATH = '/Users/wangjiaxing/work/myqrcode/pipService/insertData/piplinedatas.xlsx';
DB_PATH = '/Users/wangjiaxing/work/myqrcode/pipService/db/pipline.sqlite3';

# 1. 读取Excel文件
df = pd.read_excel(FILE_PATH)

# 2. 创建SQLite数据库并建立连接
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()



# 4. 将数据插入到SQLite数据库的表中
for index, row in df.iterrows():
    insert_query = '''
    INSERT INTO pipline_pipelines (
        name, code, orientation, length_km, depth_m, distance_position_des, 
        wall_thickness_mm, material,created_at,updated_at, qr_code_url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (
        row['name'], 
        row['code'], 
        row['orientation'], 
        row['length_km'], 
        row['depth_m'], 
        row['distance_position_des'], 
        row['wall_thickness_mm'], 
        row['material'],
        datetime.now(),  # 每次创建时created_at
        datetime.now(),  # 每次更新或创建时更新updated_at
        row.get('qr_code_url', None)  # 如果Excel中有二维码地址列，可以替换None为row['qr_code_url']
    ))

# 5. 提交事务并关闭连接
conn.commit()
conn.close()

print("数据已成功插入并更新到pipelines表中。")

