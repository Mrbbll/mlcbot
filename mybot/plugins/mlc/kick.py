from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment, Message
from nonebot.permission import SUPERUSER
import re


check_id = on_command("check", permission=SUPERUSER, priority=10, block=True)

while_list = ["机器人","测试机器人（记得修改群昵称为游戏id", "阿罗娜小助手","苦力怕娘","Q群管家","伊蕾娜","蓝猫猫猫猫猫猫猫猫猫猫猫猫猫猫猫猫猫猫猫"]

@check_id.handle()
async def handle_check_id(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id

    #获取本群所有成员
    try:
        member_list = await bot.get_group_member_list(group_id=group_id)
    except Exception as e:
        await check_id.finish(f"获取成员列表失败：{e}")
        return


    #规则定义
    mc_name_pattern = re.compile(r'^\s*[a-zA-Z0-9_]{3,16}\s*([（\(].*)?$')

    illegal_members = []  # 存储非法ID成员的信息

    #遍历检查
    for member in member_list:
        user_id = member['user_id']
        # 优先使用“群名片”(card)，如果没有则使用“昵称”(nickname)
        card_name = member.get('card') or member.get('nickname', '')
        # 跳过机器人和测试机器人
        if card_name in while_list:
            continue

        #判断是否合法
        if not mc_name_pattern.match(card_name):
            # 4. 记录不合规的成员
            illegal_members.append({
                'user_id': user_id,
                'card_name': card_name
            })

    total_count = len(member_list)
    illegal_count = len(illegal_members)

    if illegal_count == 0:
        await check_id.finish(f"检查完成。共检查 {total_count} 名成员，所有成员ID均通过")
        return

    # 构造提醒消息
    message = Message(f"检查完成。共检查 {total_count} 名成员，发现 {illegal_count} 名成员ID未修改：\n")
    for mem in illegal_members:
        #构造@消息
        at_segment = MessageSegment.at(mem['user_id'])
        # message.append(f" {at_segment} ")
        message.append(f"{at_segment}")

    message.append("\n群昵称须为3-16位英文、数字或下划线，可后接括号自定义后缀（如：Steve_123（彩笔）。")

    # 发送合并后的提醒消息
    await check_id.finish(message)
