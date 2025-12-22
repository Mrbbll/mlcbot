from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.plugin import on_startswith
from nonebot.adapters.onebot.v11 import (
    MessageSegment as MS,
)
from nonebot.adapters.onebot.v11 import Message

from .config import Config
from . import status
from datetime import datetime
import time
import mcstatus
import traceback
import psutil

from mcstatus import JavaServer
from base64 import b64decode
from io import BytesIO

#查服状态
status = on_startswith("status", priority=10, block=True)
@status.handle()
async def handle_function():
    msg = Message()
  
    logical_cores = psutil.cpu_count()
    msg.append(MS.text(f"CPU 核心：逻辑{logical_cores}核\n"))
      
    # CPU 频率（当前/最小/最大）
    cpu_freq = psutil.cpu_freq()
    msg.append(MS.text(
        f"CPU 频率：当前 {round(cpu_freq.current, 2)} MHz，"
        f"最小 {cpu_freq.min} MHz，最大 {cpu_freq.max} MHz\n"
    ))    
  
    cpu_percent = psutil.cpu_percent(interval=0.5)
    msg.append(MS.text(f"CPU占用：{cpu_percent}%\n"))
    #系统负载（1/5/15分钟平均负载）
    load_avg = psutil.getloadavg()  # 返回 (1分钟, 5分钟, 15分钟)
    msg.append(MS.text(
        f"系统负载：1分钟 {load_avg[0]:.2f}，"
        f"5分钟 {load_avg[1]:.2f}，15分钟 {load_avg[2]:.2f}\n"
    ))

    #硬盘占用
    disk_usage = psutil.disk_usage('/')
    disk_used = round(disk_usage.used / (1024** 3), 2)
    disk_free = round(disk_usage.free / (1024 **3), 2)
    msg.append(MS.text("磁盘占用：\n"))
    msg.append(MS.text(
        f"已用：{disk_used}GB（{disk_usage.percent}% ）"
        f"可用：{disk_free}GB\n"
    ))
  
    # 获取内存信息
    mem = psutil.virtual_memory()
    # 转换为GB
    total_mem = round(mem.total / (1024 **3), 2)
    used_mem = round(mem.used / (1024** 3), 2)
    mem_percent = mem.percent
    msg.append(MS.text(f"内存占用：{used_mem}GB / {total_mem}GB（{mem_percent}%）"))
        
    boot_ts = psutil.boot_time()  # 启动时间戳
    current_ts = time.time()      # 当前时间戳
    # 转换启动时间为本地时间（用time.strftime直接处理）
    boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(boot_ts))
    # 计算运行时长（只保留小时和分钟，简化除法）
    uptime = int(current_ts - boot_ts)
    uptime_str = f"{uptime//3600}小时{(uptime%3600)//60}分钟"
    msg.append(MS.text(f"\n运行时长：{uptime_str}"))
  
    await status.finish(msg)