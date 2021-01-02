# def reverselowhigh(data_in):
#     data_temp = []
#     for i in range(0, len(data_in), 4):
#         data_temp.append(data_in[i:i + 4])
#     datareversal = ''.join(data_temp[::-1])
#     return datareversal
#
# kk = '03040102'
# # kk = 'ff01'
# jj = reverselowhigh(kk)
# print(jj)
#
# kl = '01 03 08 03 04 01 02 03 04 01 02 95 d7 '
# kl = kl.strip().replace(' ','')
# code = kl[6:-4]
# codehuu = kl[4:6]
# print('code',codehuu)
# data_num = [code[i*8:(i+1)*8] for i in range(2)]
# print(data_num)
# result = []
# for i in range(2):
#     result.append(reverselowhigh(data_num[i]))
# print(result)

def reverselowhigh(data_in):
    """
    传入data = '0000 03e8'
    返回 e803 0000
    """
    data_temp = []
    for i in range(0, len(data_in), 2):
        data_temp.append(data_in[i:i + 2])
    datareversal = ''.join(data_temp[::-1])
    return datareversal

data = '000005dc'
print(reverselowhigh(data))

print(hex(1500))