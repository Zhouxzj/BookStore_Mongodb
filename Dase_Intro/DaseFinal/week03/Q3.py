import re


def validate_id_card(id_card):
    # 定义身份证号的正则表达式模式
    pattern = r'^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3}(\d|X|x)$'

    # 使用正则表达式匹配身份证号
    if re.match(pattern, id_card):
        return True
    else:
        return False


# 测试
id_card1 = "44030819990101123X"  # 合法身份证号，最后一位是X
id_card2 = "123456789012345678"  # 非法身份证号

print(f"身份证号 {id_card1} 是否合法: {validate_id_card(id_card1)}")
print(f"身份证号 {id_card2} 是否合法: {validate_id_card(id_card2)}")