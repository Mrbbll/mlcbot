from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.plugin import on_startswith
from nonebot.adapters.onebot.v11 import MessageSegment as MS
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
import requests
from .config import Config
from . import status
from . import command
from . import bilibili
from . import kick
from datetime import datetime
import time
import mcstatus
import traceback
import psutil
from mcstatus import JavaServer
from base64 import b64decode
from io import BytesIO



__plugin_meta__ = PluginMetadata(
    name="mlc",
    description="",
    usage="",
    config=Config,
)
  
config = get_plugin_config(Config)


commandhelp = on_startswith("指令帮助", priority=10, block=True)
@commandhelp.handle()
async def handle_function():
    await commandhelp.finish("""/执行 <实例名字> <命令内容（可带空格）>
/<开启/停止/终止> <实例名字>
""")


hello = on_startswith("服务器地图", priority=10, block=True)
                             
@hello.handle()
async def handle_function():
    await hello.finish("你好，我是服务器机器人，(●'◡'●)\n生存服网页地图：43.248.188.28:19423,\n服务器文档：https://docs.qq.com/aio/DRnp3YU9sRmxWYnVB")


# 服务器配置 - 类型: [主服务器, 节点1, 节点2...]
SERVERS = {
    "生存服+小游戏服": [
        "127.0.0.1:25566",       # 主服务器(图标/人数)
        "43.248.188.28:41894"   # 节点服务器(ping)
    ],
    "冒险服": [
        "127.0.0.1:25565",       # 主服务器
        "103.205.253.104:57904"  # 节点服务器
    ],
    "科技服": [
      "127.0.0.1:25569",
      "103.205.253.104:32364"
    ],
    "VC查人端口": ["127.0.0.1:25565"]  # VC查人端口
}

async def get_status(addr):
    #获取服务器状态，带异常处理
    try:
        server = JavaServer.lookup(addr)
        return server.status()
    except Exception as e:
        # 打印错误日志
        print(f"获取服务器 {addr} 状态失败：{str(e)}")
        return None

def get_icon(status):
    #提取服务器图标
    if not status or not status.icon:
        return MS.text("<无图标>\n")
    try:
        aa, bb = status.icon.split("base64,")
        return MS.image(BytesIO(b64decode(bb))) + "\n"
    except:
        return MS.text("<无图标>\n")

def get_players(status):
    #获取玩家列表
    if not status:
        return "匿名/无人"
    try:
        return ", ".join(p.name for p in status.players.sample) if status.players.sample else "无人"
    except:
        return "匿名/无人"
      
def get_query(addr):
    try:
        server = JavaServer.lookup(addr)
        return server.query()
    except Exception as e:
        # 打印错误日志
        print(f"获取服务器 {addr} 状态失败：{str(e)}")
        return None

def get_players_vc(query):
    if not query:
      return "匿名/无人"
    try:
        return ', '.join(query.players.names) if query.players.names else "无人"
    except:
        return "匿名/无人"
    
list = on_startswith("list", priority=10, block=True)
@list.handle()
async def handle_function():
    msg = Message()
    msg.append(MS.text("查服结果如下：\n\n"))
    # 处理生存服+小游戏服
    main, node = SERVERS["生存服+小游戏服"]
    status_main = await get_status(main)
    status_node = await get_status(node)
    query_vc = get_query(SERVERS["VC查人端口"][0])
    
    if status_main:
        msg.append(f"{get_icon(status_main)}生存服+小游戏服\n"
                  f"在线: {status_main.players.online}\n"
                  f"节点({node})延迟: {status_node.latency:.2f}ms\n"
                  f"玩家: {get_players_vc(query_vc)}\n")
    
    # 处理整合包服1
    main_mod, node_mod = SERVERS["冒险服"]
    status_mod = await get_status(main_mod)
    status_mod_node = await get_status(node_mod)
    
    if status_mod:
        msg.append(f"{get_icon(status_mod)}冒险服\n"
                  f"在线: {status_mod.players.online}\n"
                  f"节点({node_mod})延迟: {status_mod_node.latency:.2f}ms\n"
                  f"玩家: {get_players(status_mod)}\n")
      
    # 处理整合包服2
    main_mod1, node_mod1 = SERVERS["科技服"]
    status_mod1 = await get_status(main_mod1)
    status_mod1_node = await get_status(node_mod1)
    
    if status_mod1:
        msg.append(f"{get_icon(status_mod1)}科技服\n"
                  f"在线: {status_mod1.players.online}\n"
                  f"节点({node_mod1})延迟: {status_mod1_node.latency:.2f}ms\n"
                  f"玩家: {get_players(status_mod1)}")
  
    await list.finish(msg)

shijian = on_startswith("视奸", priority=10, block=True)
@shijian.handle()
async def handle_function():
    msg = Message()
    msg.append(MS.text("在线群友\n"))
    # 处理生存服+小游戏服
    main, node = SERVERS["生存服+小游戏服"]
    status_main = await get_status(main)
    status_node = await get_status(node)
    query_vc = get_query(SERVERS["VC查人端口"][0])
    
    if status_main:
        msg.append(f"生存服+小游戏服\n"
                  f"在线: {status_main.players.online}\n"
                  f"玩家: {get_players_vc(query_vc)}\n")
    
    # 处理整合包服1
    main_mod, node_mod = SERVERS["冒险服"]
    status_mod = await get_status(main_mod)
    status_mod_node = await get_status(node_mod)
    
    if status_mod:
        msg.append(f"冒险服\n"
                  f"在线: {status_mod.players.online}\n"
                  f"玩家: {get_players(status_mod)}\n")
      
    # 处理整合包服2
    main_mod1, node_mod1 = SERVERS["科技服"]
    status_mod1 = await get_status(main_mod1)
    status_mod1_node = await get_status(node_mod1)

    
    if status_mod1:
        msg.append(f"科技服\n"
                  f"在线: {status_mod1.players.online}\n"
                  f"玩家: {get_players(status_mod1)}")
    await shijian.finish(msg)

ip = on_startswith("ip", priority=10, block=True)
@ip.handle()
async def handle_function():
    msg = Message()
    msg.append(MS.text("服务器列表：\n\n"))
    # 处理生存服+小游戏服
    main, node = SERVERS["生存服+小游戏服"]
    status_main = await get_status(main)
    status_node = await get_status(node)
    
    if status_main:
        msg.append(f"{get_icon(status_main)}生存服+小游戏服\n"
                  f"节点({node})延迟: {status_node.latency:.2f}ms\n")
    
    # 处理整合包服1
    main_mod, node_mod = SERVERS["冒险服"]
    status_mod = await get_status(main_mod)
    status_mod_node = await get_status(node_mod)
    
    if status_mod:
        msg.append(f"{get_icon(status_mod)}冒险服\n"
                  f"节点({node_mod})延迟: {status_mod_node.latency:.2f}ms\n")
      
    # 处理整合包服2
    main_mod1, node_mod1 = SERVERS["科技服"]
    status_mod1 = await get_status(main_mod1)
    status_mod1_node = await get_status(node_mod1)
    
    if status_mod1:
        msg.append(f"{get_icon(status_mod1)}科技服\n"
                  f"节点({node_mod1})延迟: {status_mod1_node.latency:.2f}ms\n")
  
    await ip.finish(msg)


