# DES 算法实现，使用完整的 S 盒，所有步骤封装成函数

# 定义置换表和 S-盒
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

IP_INV_TABLE = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

EXPANSION_TABLE = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

P_TABLE = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# DES 密钥生成

# 定义 PC-1 和 PC-2 置换表
PC1_TABLE = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2_TABLE = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

# 每轮的左移次数
LEFT_SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

key = [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0,
       0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0
]




def permute(block, table):

    return [block[i - 1] for i in table]

def left_shift(block, num_shifts):
    """对密钥块进行左移操作"""
    return block[num_shifts:] + block[:num_shifts]

def generate_subkeys(key):

    # 1. PC-1 置换：从 64 位密钥中选出 56 位
    key56 = permute(key, PC1_TABLE)

    # 2. 将 56 位密钥分为两个 28 位部分
    left_half, right_half = key56[:28], key56[28:]

    # 3. 生成 16 轮子密钥
    subkeys = []
    for i in range(16):
        # 左移
        left_half = left_shift(left_half, LEFT_SHIFTS[i])
        right_half = left_shift(right_half, LEFT_SHIFTS[i])

        # 合并左右两部分
        combined_key = left_half + right_half

        # PC-2 置换，生成 48 位子密钥
        subkey = permute(combined_key, PC2_TABLE)
        subkeys.append(subkey)

    return subkeys

subkeys = generate_subkeys(key)
# 打印生成的子密钥
# for round_number, subkey in enumerate(subkeys, 1):
#     print(f"子密钥 {round_number}: {''.join(map(str, subkey))}")


def xor(block1, block2):
    """按位异或"""
    return [b1 ^ b2 for b1, b2 in zip(block1, block2)]


# def split_block(block):
#     """将 64 位块分为左右两个 32 位块"""
#     return block[:len(block) // 2], block[len(block) // 2:]

def split_block(block):
    return block[:32], block[32:]


def expand(block):
    """扩展置换，将 32 位扩展为 48 位"""
    return permute(block, EXPANSION_TABLE)


def s_box_substitution(expanded_block):
    """S 盒替代操作"""
    result = []
    for i in range(8):  # 8 个 S 盒，每个处理 6 位输入
        chunk = expanded_block[i * 6:(i + 1) * 6]
        row = int(f"{chunk[0]}{chunk[5]}", 2)  # 首尾两位作为行号
        col = int("".join(map(str, chunk[1:5])), 2)  # 中间 4 位作为列号
        s_value = S_BOXES[i][row][col]  # 从 S 盒中查找值
        result.extend([int(bit) for bit in f"{s_value:04b}"])  # 转为 4 位二进制
    return result


def feistel(right, key):
    expanded = expand(right)
    xored = xor(expanded, key)
    substituted = s_box_substitution(xored)
    return permute(substituted, P_TABLE)


def des_encrypt(plaintext, keys):
    plaintext = permute(plaintext, IP_TABLE)
    left, right = split_block(plaintext)

    for i in range(16):  # 16 轮 Feistel 操作
        new_right = xor(left, feistel(right, keys[i]))
        left = right
        right = new_right

    ciphertext = permute(right + left, IP_INV_TABLE)
    return ciphertext



def test():

    print(S_BOXES[0][0][0])
    print(S_BOXES[0][1][8])
    print(S_BOXES[0][1][12])
    print(S_BOXES[0][1][10])
    print(S_BOXES[0][1][14])



plaintext = [0, 1, 0, 1] * 16  # 示例 64 位明文
# key = [0, 1, 1, 0] * 16
# keys = generate_subkeys(key)
ciphertext = des_encrypt(plaintext, subkeys)
print("明文:", plaintext)
print("密文:", ciphertext)
with open("subkeys.txt", "w") as file:
    for subkey in subkeys:
        subkey_str = ''.join(map(str, subkey))  # 将子密钥转换为字符串
        file.write(subkey_str + "\n")
# print(subkeys)
# test()
