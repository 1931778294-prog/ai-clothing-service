# -*- coding: utf-8 -*-
"""
自动化测试：8 个核心场景（含多轮对话记忆、金额计算）
用法：先启动服务 python main.py，再运行 python test_api.py
结果打印到控制台，同时写入 test_result.txt（UTF-8）
"""
import json
import urllib.request

URL = "http://127.0.0.1:8000/chat"


def ask(message, history=None):
    payload = json.dumps({"message": message, "history": history or []}).encode("utf-8")
    req = urllib.request.Request(
        URL, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))["reply"]


out = []


def case(title, user_msg, history=None):
    out.append(f"\n{'='*60}\n【{title}】用户：{user_msg}\n{'-'*60}")
    reply = ask(user_msg, history)
    out.append(f"AI：{reply}")
    print(f"[完成] {title}")
    return reply


# 1. 商品查询
case("场景1 商品查询", "纯棉T恤多少钱？有哪些颜色？")

# 2-3. 尺码推荐多轮对话（验证上下文记忆 + 尺码表推理）
r2 = case("场景2 尺码引导-第1轮", "我想买那件纯棉基础T恤，不知道选什么尺码")
case("场景3 尺码推荐-第2轮(多轮记忆)", "身高175cm，体重70kg", [
    {"role": "user", "content": "我想买那件纯棉基础T恤，不知道选什么尺码"},
    {"role": "assistant", "content": r2},
])

# 4. 售后政策
case("场景4 售后政策", "退货规则是什么？")

# 5. 超纲问题（应拒答并引导人工，验证防幻觉约束）
case("场景5 超纲拒答", "这个衣服能防水吗？")

# 6. 负面情绪/投诉（应安抚 + 转人工 + 生成工单要点）
case("场景6 投诉转人工", "衣服收到是破的，我非常生气，我要投诉！")

# 7. 满减金额计算
case("场景7 优惠计算", "我买一件T恤加一件羽绒服，一共多少钱，能叠加满减吗？")

# 8. 物流咨询
case("场景8 物流咨询", "下单后多久发货？发什么快递？")

with open("test_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("\n全部测试完成，结果已写入 test_result.txt")
