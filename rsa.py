#RSA加密算法

import random
# p,q是两个不同的素数n=pq,按理说应该随机产生，这里我用p=101,q=103为例

P = 101
Q = 113
N = P * Q
global _E  # 把逆元定义为全局变量，才能在解密模块调用
_E = 0     #初始为0

#欧拉公式:如果n是质数，则 φ(n)=n-1 。因为质数与小于它的每一个数，都构成互质关系
F = (P-1) * (Q-1)


#求最大公约数，若最大公约数是1，且m,n>1,m与n不等，则说明m,n互质
def comm_div(m, n):      #m>n
    temp = m % n
    while(temp != 0):
        m = n
        n = temp
        temp = m % n
    if n == 1:         #说明互质，返回True
        return True


# 在1-9999之间随机选择一个整数e，条件是1< e < F，且e与F 互质
# 互质即说明e,F的公因子有且仅有1
def e_product():
    while True:
        rand = random.randrange(2, F)
        if comm_div(F, rand):
            e = rand
            return e


#用辗转相除法求质数e关于欧拉公式F的逆元
def _e_product(e, F):
    a_list = []
    m = F
    n = e
    temp = m % n

    while (temp != 0):
        a = (m - temp) / n
        a_list.append(a)
        m = n
        n = temp
        temp = m % n
    print("a_list:", a_list)
    a_list.reverse()    #逆序
    print("a_list_reverse:", a_list)
    b_list = []
    b_list.append(1)
    b_list.append(a_list[0])
    print("(最初插入的两个1及a_list[0])b_list:", b_list)
    for i in range(len(a_list)-1):
        b = b_list[-1] * a_list[i+1] + b_list[-2]
        b_list.append(b)

    print("b_list", b_list)
    #a_list存放的是商数，如果商数个数是偶数 b_list[-1]即为所求逆元
    #若为奇数，F-b_list[-1]为所求的逆元
    if len(a_list) % 2 == 0:   #偶数
        return b_list[-1]
    else:
        return F - b_list[-1]


#传入明文(数字)和公钥，进行加密,返回密文
def core_encryption(clear_text, e, N):
    clear = clear_text
    for i in range(e-1):
        clear_text = clear_text  * clear
    cipher_text = clear_text % N
    return cipher_text


def encryption(clear_text):
    clear_text = int(clear_text)
    e = e_product()
    print("随机产生的e:%s" % e)
    global _E       #对全局变量进行重新赋值，需要global
    _E = _e_product(e, F)
    # print("逆元_e:", _E)
    # print("逆元类型:",type(_E))
    print("公钥KU:%d,%d\n私钥KR:%d,%d" % (e,N, _E,N))
    cipher_text = core_encryption(clear_text,e,N)
    return cipher_text


#根据之前加密生成的私钥进行解密，所以必须先有加密才行的
def decryption(cipher_text, _e, N):
    cipher_text = int(cipher_text)
    cipher = cipher_text
    # print(_e)
    # print("逆元_e类型:",type(_e))
    for i in range(int(_e-1)):
        cipher_text = cipher_text * cipher
    clear_text = cipher_text % N
    return clear_text


if __name__ == "__main__":
    while True:
        print("必须先加密后解密！".center(50, "-"))
        choice = input("Input E for encryption or D for decryption:")
        if choice == "E":
            clear_text = input("请输入明文(只允许数字):")
            if clear_text.strip().isalnum():
                print("加密成功！密文为:%d" % encryption(clear_text))
        if choice == "D":
            cipher_text = input("请输入密文:")
            if cipher_text.strip().isalnum():
                print("解密成功！明文为:%d" % decryption(cipher_text, _E, N))