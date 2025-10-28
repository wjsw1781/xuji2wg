



# -*- coding: utf-8 -*-

from tqdm import tqdm
import subprocess, time,os,sys,json,random,ipaddress
from loguru import logger

from crud.utils import *

import re
_addr_re = re.compile(r'^\s*Address\s*=\s*([0-9A-Fa-f:./,]+)', re.M)
_priv_re = re.compile(r'^\s*PrivateKey\s*=\s*([\w+/=]+)',      re.M)

def extract_addr_priv(text: str):
    """
    从 WireGuard [Interface] 段配置中提取 Address 与 PrivateKey
    :param text: 整段配置字符串
    :return: (address:str | None, privkey:str | None)
    """
    addr  = _addr_re.search(text)
    priv  = _priv_re.search(text)
    return (addr.group(1) if addr else None,
            priv.group(1) if priv else None)

right_ips = '0.0.0.0/5,8.0.0.0/7,11.0.0.0/8,12.0.0.0/6,16.0.0.0/4,32.0.0.0/3,64.0.0.0/3,96.0.0.0/5,104.0.0.0/7,106.0.0.0/13,106.8.0.0/14,106.12.0.0/15,106.14.0.0/16,106.15.0.0/18,106.15.64.0/21,106.15.72.0/22,106.15.76.0/23,106.15.78.0/24,106.15.79.0/25,106.15.79.128/27,106.15.79.160/29,106.15.79.168/31,106.15.79.171/32,106.15.79.172/30,106.15.79.176/28,106.15.79.192/26,106.15.80.0/20,106.15.96.0/19,106.15.128.0/17,106.16.0.0/12,106.32.0.0/11,106.64.0.0/10,106.128.0.0/9,107.0.0.0/8,108.0.0.0/6,112.0.0.0/7,114.0.0.0/11,114.32.0.0/12,114.48.0.0/14,114.52.0.0/15,114.54.0.0/16,114.55.0.0/18,114.55.64.0/20,114.55.80.0/21,114.55.88.0/23,114.55.90.0/24,114.55.91.0/27,114.55.91.32/28,114.55.91.48/29,114.55.91.56/31,114.55.91.59/32,114.55.91.60/30,114.55.91.64/26,114.55.91.128/25,114.55.92.0/22,114.55.96.0/20,114.55.112.0/23,114.55.114.0/25,114.55.114.128/26,114.55.114.192/32,114.55.114.194/31,114.55.114.196/30,114.55.114.200/29,114.55.114.208/28,114.55.114.224/27,114.55.115.0/24,114.55.116.0/22,114.55.120.0/21,114.55.128.0/17,114.56.0.0/13,114.64.0.0/10,114.128.0.0/9,115.0.0.0/8,116.0.0.0/7,118.0.0.0/9,118.128.0.0/11,118.160.0.0/12,118.176.0.0/15,118.178.0.0/17,118.178.128.0/19,118.178.160.0/21,118.178.168.0/22,118.178.172.0/25,118.178.172.128/29,118.178.172.136/30,118.178.172.140/31,118.178.172.143/32,118.178.172.144/28,118.178.172.160/27,118.178.172.192/26,118.178.173.0/24,118.178.174.0/23,118.178.176.0/20,118.178.192.0/18,118.179.0.0/16,118.180.0.0/14,118.184.0.0/13,118.192.0.0/10,119.0.0.0/8,120.0.0.0/5,128.0.0.0/3,160.0.0.0/5,168.0.0.0/6,172.0.0.0/12,172.32.0.0/11,172.64.0.0/10,172.128.0.0/9,173.0.0.0/8,174.0.0.0/7,176.0.0.0/4,192.0.0.0/9,192.128.0.0/11,192.160.0.0/13,192.169.0.0/16,192.170.0.0/15,192.172.0.0/14,192.176.0.0/12,192.192.0.0/10,193.0.0.0/8,194.0.0.0/7,196.0.0.0/6,200.0.0.0/5,208.0.0.0/4,224.0.0.0/3'
MTU = 1380
prefixlen = 32
wg_ip_use_area = "10.96.0.0/16"
wg_main_server_ip_加速 = '47.99.89.181'
wg_main_server_ip = '47.99.89.181'
ListenPort = 58000


srv_pub = subprocess.check_output(f"""
        wg show 10_96_0_3 public-key
    """, shell=True).decode('utf-8').strip()

table = 'app_tables.wg_node_0000'


    # 表名: app_tables.wg_node_0000
    # 列名: [{'column_name': '_id'}, {'column_name': 'wg_conf'}, {'column_name': 'public_key'}, {'column_name': 'private_key'}, {'column_name': 'wg_conf_img'}, {'column_name': 'wg_client_ip_name'}]
import glob

all_wg_conf = glob.glob('/root/socks_ss_gfw_ss_socks/wg_one_2_many_peer/xuji2wg/crud/wg_client_sh/10_96_0_0_16/*allow.conf')
for wg_conf in all_wg_conf:
    peer_info= extract_addr_priv(open(wg_conf).read())
    peer_ip = peer_info[0]
    peer_pri = peer_info[1]
    peer_pub = subprocess.check_output(f"""
               wg show 10_96_0_3 dump | awk '$4=="{peer_ip}"{{print $1}}'
        """, shell=True).decode('utf-8').strip()
    print(peer_ip,peer_pri,peer_pub)

    client_conf_no_root_with_allow_ips = f"""
        [Interface]
        Address ={peer_ip}
        PrivateKey = {peer_pri}
        MTU = {MTU}
        DNS = 8.8.8.8

        [Peer]
        PublicKey = {srv_pub}
        Endpoint  = {wg_main_server_ip}:{ListenPort}
        AllowedIPs = {right_ips},{wg_ip_use_area}
        PersistentKeepalive = 25

    """
    import io,base64,qrcode
    buf = io.BytesIO()
    qrcode.make(client_conf_no_root_with_allow_ips).save(buf, format='PNG')
    b64_img = base64.b64encode(buf.getvalue()).decode('ascii')
    
    wg_client_ip_name = peer_ip.split('/')[0]

    cur.execute(f"SELECT * FROM {table} WHERE wg_client_ip_name='{wg_client_ip_name}'")
    have_exist = cur.fetchone()
    if have_exist:
        # 删除
        cur.execute(f"DELETE FROM {table} WHERE wg_client_ip_name='{wg_client_ip_name}'")

    cur.execute(f"SELECT * FROM {table} WHERE wg_client_ip_name='{peer_ip}'")
    have_exist = cur.fetchone()
    if have_exist:
        # 删除
        cur.execute(f"DELETE FROM {table} WHERE wg_client_ip_name='{peer_ip}'")


    cur.execute(f"INSERT INTO {table} (wg_client_ip_name, public_key, private_key,wg_conf, wg_conf_img) VALUES ('{wg_client_ip_name}', '{peer_pub}', '{peer_pri}','{client_conf_no_root_with_allow_ips}','{b64_img}');")
    conn.commit()

    # 打印总数
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(cur.fetchone())

