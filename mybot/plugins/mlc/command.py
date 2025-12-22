import requests
from nonebot.plugin import on_startswith
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment as MS
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

MCSM_PANEL_URL = "http://127.0.0.1:23333" 
MCSM_API_SECRET = "d91738751a9447ccaca2086ea01574e5" #用户密钥
# DEFAULT_DAEMON_ID = "b7118149e42d4cf86415cd5e6854297a2e7866ea423e3b8" #守护进程id
DEFAULT_DAEMON_ID = "48118c0a53ec4818b285251b35a9825d"

def send_mcsm_command(uuid, daemon_id, command):
    url = f"{MCSM_PANEL_URL}/api/protected_instance/command"
    params = {
        "apikey": MCSM_API_SECRET,
        "uuid": uuid,
        "daemonId": daemon_id,
        "command": command
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(
        url=url,
        params=params,
        headers=headers
    )
    return response

def send_mcsm_open(uuid, daemon_id):
    url = f"{MCSM_PANEL_URL}/api/protected_instance/open"
    params = {
        "apikey": MCSM_API_SECRET,
        "uuid": uuid,
        "daemonId": daemon_id
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(
        url=url,
        params=params,
        headers=headers
    )
    return response

def send_mcsm_stop(uuid, daemon_id):
    url = f"{MCSM_PANEL_URL}/api/protected_instance/stop"
    params = {
        "apikey": MCSM_API_SECRET,
        "uuid": uuid,
        "daemonId": daemon_id
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(
        url=url,
        params=params,
        headers=headers
    )
    return response

def send_mcsm_kill(uuid, daemon_id):
    url = f"{MCSM_PANEL_URL}/api/protected_instance/kill"
    params = {
        "apikey": MCSM_API_SECRET,
        "uuid": uuid,
        "daemonId": daemon_id
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(
        url=url,
        params=params,
        headers=headers
    )
    return response

def getinstanceid(str):
    if str == "mod":
        return "27ea20d72183463bb4cf090873793cc1"
    elif str == "lobby":
        return "78d271683ebc4ae79c0110016c2f08c3"
    elif str == "scf":
        return "ab1618cf3a484ebd9a8d1bc8e15222b7"
    elif str == "minigames":
        return "63da3dc840434753b0abd2e62a08746c"
    elif str == "vc":
        return "25d18f7748b94aeb9949857a270bc468"
    elif str == "vc1":
        return "49af27ad838c481fbd0e2c093662905d"
    elif str == "mod1":
        return "8ab80a3c099641f592f16164b6fb620a"
    else:
        return "null"

def getreason(response):
    if response.status_code == 200:
        return "命令请求成功 [200]"
    else:
        if response.status_code == 400:
            return "参数错误（UUID/守护进程ID无效）"
        elif response.status_code == 403:
            return "无权限（API密钥错误或未授权）"
        elif response.status_code == 404:
            return "接口不存在（面板地址或API路径错误）"
        elif response.status_code == 500:
            return "面板服务器内部异常"
        else:
            return "未知错误"

command = on_command("执行", priority=10, block=True, permission=SUPERUSER)

@command.handle()
async def handle_function(args: Message = CommandArg()):
    input_text = args.extract_plain_text()
    if not input_text:
        await command.finish("格式错误1！\n用法：执行 <实例名字> <命令内容（可带空格）>")

    parts = input_text.split(' ', 1)  # 只分割一次
    if len(parts) < 2:
        await command.finish("格式错误2！\n用法：执行 <实例名字> <命令内容（可带空格）>")
    
    instanceid = parts[0]  # 第一个片段：实例ID
    instance_uuid = getinstanceid(instanceid)
    if(instance_uuid == "null"):
        await command.finish("无效id")
    
    command_content = parts[1]  # 剩余命令
    
    # 发送命令
    response = send_mcsm_command(
        uuid=instance_uuid,
        daemon_id=DEFAULT_DAEMON_ID,
        command=command_content
    )
    
    reason = getreason(response)
    
    # 回复已发送
    await command.finish(
        f"已向实例发送命令：\n"
        f"实例：{instanceid}\n"
        f"命令内容：{command_content}\n"
        f"结果：{reason}"
    )

start = on_command("开启", priority=10, block=True, permission=SUPERUSER)

@start.handle()
async def handle_function(args: Message = CommandArg()):
    input_text = args.extract_plain_text()
    instance_uuid = getinstanceid(input_text)
    if(instance_uuid == "null"):
        await start.finish("无效id")
      
    # 发送命令
    response = send_mcsm_open(
        uuid=instance_uuid,
        daemon_id=DEFAULT_DAEMON_ID
    )
    
    reason = getreason(response)
  
    # 回复已发送
    await start.finish(
        f"已向实例发送开启命令：\n"
        f"实例：{input_text}\n"
        f"结果：{reason}"
    )

stop = on_command("停止", priority=10, block=True, permission=SUPERUSER)

@stop.handle()
async def handle_function(args: Message = CommandArg()):
    input_text = args.extract_plain_text()
    instance_uuid = getinstanceid(input_text)
    if(instance_uuid == "null"):
        await start.finish("无效id")
      
    # 发送命令
    response = send_mcsm_stop(
        uuid=instance_uuid,
        daemon_id=DEFAULT_DAEMON_ID
    )
    
    reason = getreason(response)
  
    # 回复已发送
    await stop.finish(
        f"已向实例发送停止命令：\n"
        f"实例：{input_text}\n"
        f"结果：{reason}"
    )

kill = on_command("终止", priority=10, block=True, permission=SUPERUSER)

@kill.handle()
async def handle_function(args: Message = CommandArg()):
    input_text = args.extract_plain_text()
    instance_uuid = getinstanceid(input_text)
    if(instance_uuid == "null"):
        await kill.finish("无效id")
      
    # 发送命令
    response = send_mcsm_kill(
        uuid=instance_uuid,
        daemon_id=DEFAULT_DAEMON_ID
    )
    
    reason = getreason(response)
  
    # 回复已发送
    await kill.finish(
        f"已向实例发送终止命令：\n"
        f"实例：{input_text}\n"
        f"结果：{reason}"
    )
