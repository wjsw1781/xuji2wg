from itertools import cycle
mobiles = [1, 2, 3, 4, 5]           # 5 台手机
proxies = [101, 102]                # 2 个代理

pairs = list(zip(mobiles, cycle(proxies)))

for mobile, proxy in pairs:
    print(f"手机 {mobile} 绑定代理 {proxy}")