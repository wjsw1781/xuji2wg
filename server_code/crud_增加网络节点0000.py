



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger


from crud import *
table = 'wg_node_0000'


"""

wg_client_ip
wg_conf
public_key
private_key
"""


# 查找



def get_公私钥(ip: str):

    data ={
        "wg_client_ip": "10.96.0.1",
        "table":table,
    }
    res = requests.post(crud_c_url,data=data)
    print(data)
    # 已存在，直接返回
    if res:                       
        return {
            "public": res["public_key"],
            "private": res["private_key"],
        }
    

    # 3. 生成新公私钥
    priv = subprocess.check_output(["wg", "genkey"]).strip().decode()
    pub = subprocess.check_output(["wg", "pubkey"], input=priv.encode()).strip().decode()

    # 4. 写入数据库
    cur.execute(
        f"INSERT INTO {TABLE_NAME} (ip, public_key, private_key) VALUES (?, ?, ?)",
        (ip, pub, priv)
    )
    conn.commit()
    new_id = cur.lastrowid

    return {"public": pub, "private": priv,'id': new_id}


# 需要多少个客户端配置
need_how_many_client = 500
# 基础配置    # udp 接受的 mtu 必须要小
MTU = 1380
prefixlen = 32

wg_ip_use_area = "10.97.0.0/16"
wg_main_server_ip = '8.217.224.52'
wg_main_server_ip_加速 = '47.99.89.181'
logger.error(f"请注意   这里进行了加速 ip 替换掉原始 ip  海外 wg 必须加速才能使用  {wg_main_server_ip} =======>   加速后 {wg_main_server_ip_加速}"'')
wg_main_server_ip = wg_main_server_ip_加速

RT_table_ID = 601
ListenPort = 58002

wg_server_client_ips = []


# 规定 服务器端ip 客户端 ip 网段信息
wg_ip_obj = ipaddress.ip_network(wg_ip_use_area).subnets(new_prefix=prefixlen)
for subnet in wg_ip_obj:                                                    # 10.101.0.0/24 … 10.101.255.0/24
    server_ip = subnet.network_address + 1  
    wg_ip =f"{server_ip}/{subnet.prefixlen}"
    wg_server_client_ips.append(wg_ip)
wg_server_client_ips= wg_server_client_ips[2:-2]

wg_ip_server = wg_server_client_ips.pop(0).split('/')[0]
wg_table_server = f"{wg_ip_server.replace('.','_')}"
wg_if_server =wg_table_server
wg_conf_file_server = f"/etc/wireguard/{wg_table_server}.conf"
wg_conf_file_server_sh= f"/etc/wireguard/{wg_table_server}.sh"
wg_conf_file_server_sh_this_dir=f"./wg_client_sh/{wg_ip_use_area.replace('/','_').replace('.','_')}/{wg_table_server}_server.sh"


server_pub_pri=get_公私钥(wg_ip_server)
srv_priv = server_pub_pri['private']
srv_pub = server_pub_pri['public']




peer_templets=[] 
ip_rule_servers=[] 


process_bar = tqdm(total=need_how_many_client)

for i in range(need_how_many_client):
    process_bar.update(1)

    # 服务器wg ip 地址  
    wg_ip_server_with_prefixlen =  str(wg_server_client_ips[i])

    wg_ip_client = wg_ip_server_with_prefixlen.split('/')[0]
    wg_table_client = f"{wg_ip_client.replace('.','_')}"
    wg_if_client =wg_table_client
    wg_conf_file_client = f"/etc/wireguard/{wg_table_client}.conf"
    wg_conf_file_client_sh = f"/etc/wireguard/{wg_table_client}.sh"

    client_pub_pri=get_公私钥(wg_ip_client)
    client_priv = client_pub_pri['private']
    cli_pub = client_pub_pri['public']


    # 生成配置文件
    client_conf = f"""
        [Interface]
        Address ={wg_ip_client}/{prefixlen}
        PrivateKey = {client_priv}
        Table = {wg_table_client}
        MTU = {MTU}
        DNS = 8.8.8.8

        [Peer]
        PublicKey = {srv_pub}
        Endpoint  = {wg_main_server_ip}:{ListenPort}
        AllowedIPs = {wg_ip_use_area}
        PersistentKeepalive = 25

    """

    client_conf_no_root = f"""
        [Interface]
        Address ={wg_ip_client}/{prefixlen}
        PrivateKey = {client_priv}
        # Table = {wg_table_client}
        MTU = {MTU}
        DNS = 8.8.8.8

        [Peer]
        PublicKey = {srv_pub}
        Endpoint  = {wg_main_server_ip}:{ListenPort}
        AllowedIPs = {wg_ip_use_area}
        PersistentKeepalive = 25

    """

    right_ips = '0.0.0.0/5,8.0.0.0/7,11.0.0.0/8,12.0.0.0/6,16.0.0.0/4,32.0.0.0/3,64.0.0.0/3,96.0.0.0/5,104.0.0.0/7,106.0.0.0/13,106.8.0.0/14,106.12.0.0/15,106.14.0.0/16,106.15.0.0/18,106.15.64.0/21,106.15.72.0/22,106.15.76.0/23,106.15.78.0/24,106.15.79.0/25,106.15.79.128/27,106.15.79.160/29,106.15.79.168/31,106.15.79.171/32,106.15.79.172/30,106.15.79.176/28,106.15.79.192/26,106.15.80.0/20,106.15.96.0/19,106.15.128.0/17,106.16.0.0/12,106.32.0.0/11,106.64.0.0/10,106.128.0.0/9,107.0.0.0/8,108.0.0.0/6,112.0.0.0/7,114.0.0.0/11,114.32.0.0/12,114.48.0.0/14,114.52.0.0/15,114.54.0.0/16,114.55.0.0/18,114.55.64.0/20,114.55.80.0/21,114.55.88.0/23,114.55.90.0/24,114.55.91.0/27,114.55.91.32/28,114.55.91.48/29,114.55.91.56/31,114.55.91.59/32,114.55.91.60/30,114.55.91.64/26,114.55.91.128/25,114.55.92.0/22,114.55.96.0/20,114.55.112.0/23,114.55.114.0/25,114.55.114.128/26,114.55.114.192/32,114.55.114.194/31,114.55.114.196/30,114.55.114.200/29,114.55.114.208/28,114.55.114.224/27,114.55.115.0/24,114.55.116.0/22,114.55.120.0/21,114.55.128.0/17,114.56.0.0/13,114.64.0.0/10,114.128.0.0/9,115.0.0.0/8,116.0.0.0/7,118.0.0.0/9,118.128.0.0/11,118.160.0.0/12,118.176.0.0/15,118.178.0.0/17,118.178.128.0/19,118.178.160.0/21,118.178.168.0/22,118.178.172.0/25,118.178.172.128/29,118.178.172.136/30,118.178.172.140/31,118.178.172.143/32,118.178.172.144/28,118.178.172.160/27,118.178.172.192/26,118.178.173.0/24,118.178.174.0/23,118.178.176.0/20,118.178.192.0/18,118.179.0.0/16,118.180.0.0/14,118.184.0.0/13,118.192.0.0/10,119.0.0.0/8,120.0.0.0/5,128.0.0.0/3,160.0.0.0/5,168.0.0.0/6,172.0.0.0/12,172.32.0.0/11,172.64.0.0/10,172.128.0.0/9,173.0.0.0/8,174.0.0.0/7,176.0.0.0/4,192.0.0.0/9,192.128.0.0/11,192.160.0.0/13,192.169.0.0/16,192.170.0.0/15,192.172.0.0/14,192.176.0.0/12,192.192.0.0/10,193.0.0.0/8,194.0.0.0/7,196.0.0.0/6,200.0.0.0/5,208.0.0.0/4,224.0.0.0/3'


    client_conf_no_root_with_allow_ips = f"""
        [Interface]
        Address ={wg_ip_client}/{prefixlen}
        PrivateKey = {client_priv}
        # Table = {wg_table_client}
        MTU = {MTU}
        DNS = 8.8.8.8

        [Peer]
        PublicKey = {srv_pub}
        Endpoint  = {wg_main_server_ip}:{ListenPort}
        AllowedIPs = {right_ips},{wg_ip_use_area}
        PersistentKeepalive = 25

    """

    client_script = f"""
        sysctl -w net.ipv4.ip_forward=1

        echo "{client_conf}" > {wg_conf_file_client}

        if ! cat /etc/iproute2/rt_tables | grep "{wg_table_client}"; then
            echo "{RT_table_ID}    {wg_table_client}" >> /etc/iproute2/rt_tables
        fi
        sysctl -w net.ipv4.ip_forward=1 2>/dev/null

        wg-quick down {wg_if_client}  2>/dev/null
        ip -4 route flush table {wg_table_client}
        ip -6 route flush table {wg_table_client}
        wg-quick up {wg_if_client} 2>/dev/null

        ip rule list   | grep {wg_ip_use_area} | awk '{{print $1}}' | tr -d ':' |xargs -r -I{{}} ip rule del pref {{}}
        ip rule add to {wg_ip_use_area} lookup {wg_table_client}

    """

    client_script_sh = f"""
        cat << EOF > {wg_conf_file_client_sh}
        {client_script}
        EOF

        bash {wg_conf_file_client_sh}
    """
    use_file_sh_client= f"./wg_client_sh/{wg_ip_use_area.replace('/','_').replace('.','_')}/{wg_table_client}.sh"
    use_file_conf_client= f"./wg_client_sh/{wg_ip_use_area.replace('/','_').replace('.','_')}/{wg_table_client}.conf"
    use_file_conf_phone_client= f"./wg_client_sh/{wg_ip_use_area.replace('/','_').replace('.','_')}/{wg_table_client}_phone.conf"
    use_file_conf_phone_client_二维码= f"./wg_client_sh/{wg_ip_use_area.replace('/','_').replace('.','_')}/{wg_table_client}_phone_二维码.png"
    use_file_conf_phone_allowips= f"./wg_client_sh/{wg_ip_use_area.replace('/','_').replace('.','_')}/{wg_table_client}_allow.conf"
    use_file_sh_client=os.path.abspath(use_file_sh_client)
    os.makedirs(os.path.dirname(use_file_sh_client), exist_ok=True)

    # 保存 client 的 sh
    with open(use_file_sh_client,'w') as ff:
        ff.write(client_script)


    # 保存 client 的 conf 具有 root
    with open(use_file_conf_client,'w') as ff:
        ff.write(client_conf)

    # 保存 client 的 conf 具有 手机分发 节点 那种没法创建路由表
    with open(use_file_conf_phone_client,'w') as ff:
        ff.write(client_conf_no_root)
        # 写回 conf 字段 sqlite
        cur.execute(f"UPDATE {TABLE_NAME} SET conf='{client_conf_no_root}' WHERE ip='{wg_ip_client}'")
        conn.commit()

    with open(use_file_conf_phone_allowips,'w') as ff:
        ff.write(client_conf_no_root_with_allow_ips)

    # pip install qrcode[pil]  
    import qrcode
    qrcode.make(client_conf_no_root).save(use_file_conf_phone_client_二维码)

    peer_templet = f"""
        [Peer]
        PublicKey = {cli_pub}
        AllowedIPs = {wg_ip_server_with_prefixlen}
        PersistentKeepalive = 25
        
    """

    # 修改路由表 只依赖wg-quick不行
    wg_server_ip_rule = f"""
                                       
        ip rule list   | grep {wg_ip_server_with_prefixlen} | awk '{{print $1}}' | tr -d ':' |xargs -r -I{{}} ip rule del pref {{}}
        ip rule add to {wg_ip_server_with_prefixlen} lookup {wg_table_server}

    """
    peer_templets.append(peer_templet)
    ip_rule_servers.append(wg_server_ip_rule)


server_conf = f"""
    [Interface]
    Address = {wg_ip_server}/{prefixlen}
    ListenPort = {ListenPort}
    PrivateKey = {srv_priv}
    Table = {wg_table_server}
    MTU = {MTU}

    {"".join(peer_templets)}

"""

# 服务端直接运行起来
cmd_lunch_wg_server = f"""
    sysctl -w net.ipv4.ip_forward=1
    
    WAN_IF=$(ip -o -4 route show default   | awk '{{print $5;exit}}')
    WAN_GW=$(ip -o -4 route show default   | awk '{{print $3;exit}}')

    iptables -t nat -D POSTROUTING -o $WAN_IF -j MASQUERADE
    iptables -t nat -A POSTROUTING -o $WAN_IF -j MASQUERADE

    iptables -t mangle -D FORWARD -o 10_+ -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
    iptables -t mangle -A FORWARD -o 10_+ -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
    iptables -t mangle -D FORWARD -i 10_+ -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu
    iptables -t mangle -A FORWARD -i 10_+ -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu

    echo "{server_conf}" > {wg_conf_file_server}

    if ! cat /etc/iproute2/rt_tables | grep "{wg_table_server}"; then
        echo "{RT_table_ID}    {wg_table_server}" >> /etc/iproute2/rt_tables
    fi

    wg-quick down {wg_conf_file_server}
    wg-quick up {wg_conf_file_server}

    {"".join(ip_rule_servers)}

"""


# 服务器生成下发脚本 一键运行 基于 cat eof + bash 
server_script = f"""

cat << EOF > {wg_conf_file_server_sh}
{cmd_lunch_wg_server}
EOF

bash {wg_conf_file_server_sh}

"""


with open(wg_conf_file_server_sh_this_dir,'w') as ff:
    ff.write(server_script)



os.system(f"""

chmod 777 {wg_conf_file_server_sh_this_dir}
bash {wg_conf_file_server_sh_this_dir}

""")


# 启动socks5进程
cmds_socks5 = """
    pip install asyncio-socks-server
    pkill -f asyncio_socks_server
    nohup python -m asyncio_socks_server --port 9898 >/dev/null 2>&1 & 
    curl -x socks5://127.0.0.1:9898 ipinfo.io

"""













