import numpy as np
import matplotlib.pyplot as plt

"""
只是一个验证用的py文件
"""
#定义x、y散点坐标
x = [0.284271247461902,4.30228320103704,7.82945715469326,10.9991987097171,13.8927201313068,16.5638586749397,
               19.0505047794389,21.3805376641446,23.5751878329105,25.6510717507116,27.6214886532175,29.497282544482,
               31.2874354311266,32.9994877027668,34.6398435502516,36.2139976952066,37.7267069006199,39.1821218777734,
               40.5838902367021,41.9352378990735,43.239034243875,44.4978447955524,45.7139742518337,46.8895019345168,
               48.0263112349928,49.1261142545117,50.1904725653963,51.2208148152996,52.2184517427256,53.18458905482,
               54.1203385282842,55.0267276243018,55.9047078536121,56.7551620846778,57.5789109535755,58.3767185067828,
               59.1492971859211,59.8973122455971,60.621385680884]
x = np.array(x)
print('x is :\n',x)
num = [i for i in range(len(x))]
y = np.array(num)
print('y is :\n',y)
#用7次多项式拟合
f1 = np.polyfit(x, y, 8)
print('f1 is :\n',f1)
p1 = np.poly1d(f1)
print('p1 is :\n',p1)
yvals = p1(x)
plot1 = plt.plot(x, y, 'b',label='original values')
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=4) #指定legend的位置右下角
plt.title('polyfitting')
plt.show()

w = 36.214
print("w={}, value={}".format(w,p1(w)))


# print(np.max(abs(y-yvals)))
print(y-yvals)
y_fit = []
for i in x:
    y_fit.append(p1(i))
res = list(zip(y_fit,y))
print(res)
