print(hex(140))
# jj = '0000008c'
jj = '000003e8'


def reverselowhigh(data_in, type):
    """
    传入data = '00059540'
    if type = 4 返回 95400005
    if type = 2 返回 40950500
    """
    data_temp = []
    for i in range(0, len(data_in), type):
        data_temp.append(data_in[i:i + type])
    datareversal = ''.join(data_temp[::-1])
    return datareversal
number = 5
command = hex(5)[2:]
command = "{0:0>{1}s}".format(command,number)

print(command)