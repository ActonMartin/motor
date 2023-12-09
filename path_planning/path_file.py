
def preprocess():
    y_blank = 11.3
    # y_blank = 11.48
    x_blank = 12.063
    # x_blank = 12.175
    x_list = [x*(x_blank*1000)/1000 for x in range(0,9)]
    y_list = [y*(y_blank*100)/100 for y in range(6)]
    return x_list,y_list


def get_path_planning():
    # →→→→→→→→→→→→→→→→→
    # ←←←←←←←←←←←←←←←←←
    # →→→→→→→→→→→→→→→→→
    # ←←←←←←←←←←←←←←←←←
    # →→→→→→→→→→→→→→→→→
    # ←←←←←←←←←←←←←←←←←
    # →→→→→→→→→→→→→→→→→
    # ←←←←←←←←←←←←←←←←←
    # →→→→→→→→→→→→→→→→→
    x_list,y_list = preprocess()
    # print(x_list,y_list)
    coordinate_list = []
    for index,value in enumerate(x_list):
        if index % 2 == 0:
            for i in y_list:
                coordinate = (value,i)
                coordinate_list.append(coordinate)
        if index % 2 == 1:
            for j in y_list[::-1]:
                coordinate = (value,j)
                coordinate_list.append(coordinate)
    return coordinate_list


if __name__ == '__main__':
    a = get_path_planning()
    print(a)
    # a 是托盘上的相对坐标，然后在确定第一个物体位置的绝对坐标之后，对每一个坐标进行相加。
