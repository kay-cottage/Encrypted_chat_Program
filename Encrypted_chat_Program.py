from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex 
from socket import *
import getpass
from threading import Thread
import hashlib


#接受消息
def rec_data():
  while True:
    rec_info = udpsocket.recv(1024).decode()
    ip_ad = udpsocket.recvfrom(1024)[1]
    d = decrypt(rec_info,key)
    print("\r>>%s:%s" % (ip_ad, d))
    print(" ", end="")

#发送消息
def send_date():
  while True:
    text = input("<<")
    e = encrypt(text,key)
    st =  str(e.decode())
    udpsocket.sendto(st.encode(), (desip, desport))
udpsocket = None
desip = ""
desport = 0

#消息取段处理
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text,key):
    mode = AES.MODE_ECB
    text = add_to_16(text)
    cryptos = AES.new(key, mode)
    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(rec_info,key):
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(rec_info))
    return bytes.decode(plain_text).rstrip('\0')

def main():
  global udpsocket
  global desip
  global desport
  global key
  print('本程序为加密聊天程序')
  print('<<为可发送状态')
  print(' ')
  locport = int(input('请绑定本地端口（默认33333）：'))
  desip = input("远程IP：")
  desport = int(input("对方端口（默认33333）："))
  print('以下请正确输入与好友约定的密钥')
  print('该密钥可以是几乎任意定长的字符串！')
   #两次SHA生成密钥。此部分可自定义修改，例如可以使用RSA生成密钥key，或者推荐使用D-H密钥交换算法
  a = input('请输入该密钥：').encode("utf8")
  b = hashlib.sha256(a).hexdigest()
  c = hashlib.sha256(b.encode("utf8")).hexdigest()
  key = c[6:38].encode('utf8')
  udpsocket = socket(AF_INET, SOCK_DGRAM)
  udpsocket.bind(("", locport))
  print('######################已经成功创建socket#####################')
  for i in range(60):
                print('                          >>>>>>><<<<<<<<                                     ')
  print('***********************可以开始会话***************************')           
  tr = Thread(target=rec_data)
  ts = Thread(target=send_date)
  tr.start()
  ts.start()
  tr.join()
  ts.join()

  
if __name__ == '__main__':
  main()
