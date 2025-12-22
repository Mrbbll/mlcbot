from nonebot.plugin import on_command
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11 import MessageSegment as MS
from nonebot.adapters.onebot.v11 import Message
from nonebot import get_bots, get_driver
from bilibili_api import live
import asyncio


uids = {
    31531145,30646779
}
group_id = 821656882

status = {}

danmaku_tasks = []

async def send_notification(message: str):
    try:
        bots = get_bots()
        if bots:
            bot = next(iter(bots.values()))
            await bot.send_group_msg(
                group_id=group_id,
                message=Message(message)
            )
    except:
        pass

async def check_live(room_id: int):
    try:
        room = live.LiveRoom(room_id)
        
        #获取直播间信息
        room_info = await room.get_room_info()

        live_status = room_info.get('room_info', {}).get('live_status', 0)
        is_live = live_status == 1
        
        # 标题
        room_detail = room_info.get('room_info', {})
        title = room_detail.get('title', '')
        
        # 主播名
        anchor_info = room_info.get('anchor_info', {})
        base_info = anchor_info.get('base_info', {})
        uname = base_info.get('uname', '主播')
        
        # 状态变化检测
        if room_id not in status:
            status[room_id] = is_live
            print(f"初始化: 直播间 {room_id} ({uname}) 状态: {'直播中' if is_live else '未开播'}")
            return
        
        if status[room_id] != is_live:
            if is_live:
                # 开播通知
                message = f"{uname} 开播啦！\n标题：{title}\n链接：https://live.bilibili.com/{room_id}"
                await send_notification(message)
                print(f"检测到开播并已通知: {uname} - {title}")
            else:
                # 下播通知
                await send_notification(f"{uname} 的直播间已下播！")
                print(f"检测到下播并已通知: {uname}")
            
            status[room_id] = is_live
            
    except Exception as e:
        print(f"使用库检查直播间 {room_id} 失败: {e}")
        import traceback
        traceback.print_exc()

async def check_all():
    tasks = [check_live(room_id) for room_id in uids]
    await asyncio.gather(*tasks)


@scheduler.scheduled_job("interval", seconds=5, id="bilibili_live_check")
async def scheduled_check():
    await check_all()

driver = get_driver()

@driver.on_startup
async def init():
    await check_all()

@driver.on_shutdown
async def cleanup():
    status.clear()
