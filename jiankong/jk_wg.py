#!/usr/bin/env python3
import pandas as pd

PATH       = 'metrics.h5'    # 永远写这一个文件
KEEP_DAYS  = 10              # 只留最近 N 天
now        = pd.Timestamp.utcnow()
cutoff     = now - pd.Timedelta(days=KEEP_DAYS)

# ----------- 采集三类指标（示例造数） -----------





# ----------- 追加写 + 清理旧数据 -----------
with pd.HDFStore(PATH) as st:
    st.append('wg',  df_wg,  format='table', data_columns=True)

    # 删除各表中过期行
    for k in st.keys():                      # ['/wg', '/cpu', '/bw']
        st.remove(k, where='ts < cutoff')

# ----------- (可选) 查询最近 3 小时 wg ----------
cut3h = now - pd.Timedelta('3h')
df_recent = pd.read_hdf(PATH, 'wg', where='ts >= cut3h')
print(df_recent)


# 定时执行 先删除后追加
