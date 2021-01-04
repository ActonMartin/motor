import time



number = 1024
start = time.time()
for i in range(number):
    x = '%04x'%i
    print(x)
mid = time.time()
for i in range(number):
    x = hex(i)[2:]
    x = (4-len(x))*'0'+x
end = time.time()

print(mid-start,(mid-start)/number)
print(end-mid,(end-mid)/number)