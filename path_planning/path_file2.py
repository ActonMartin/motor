import numpy as np


class PathPlanning:
    def __init__(self,x_blank=12.063, y_blank=11.3, width=6,height=9,flag=2):
        self.x_blank = x_blank
        self.y_blank = y_blank
        self.width = width
        self.height = height
        self.flag = flag
        self.x_list,self.y_list = self.pre_process()

    def pre_process(self):
        if self.flag == 1:
            x_list = [x*(self.x_blank*1000)/1000 for x in range(self.height)]
            y_list = [y*(self.y_blank*100)/100 for y in range(self.width)]
        elif self.flag == 2:
            # 每一个坐标进行了二等分，也就是在步长为0.5切分一次
            x_list = [x * (self.x_blank * 1000) / 10000 for x in range(0, self.height * 10, 5)]
            y_list = [y * (self.y_blank * 100) / 1000 for y in range(0, self.width * 10, 5)]
        return x_list, y_list

    def get_path_planning(self):
        if self.flag == 1:
            coordinate_list = self.get_path_planning_single()
        elif self.flag == 2:
            coordinate_list = []
            for index, value in enumerate(self.x_list):
                for i in self.y_list:
                    coordinate = (value, i)
                    coordinate_list.append(coordinate)
            x_list, y_list = [], []
            for k, v in coordinate_list:
                x_list.append(k)
                y_list.append(v)
            x_numpy = np.array(x_list).reshape((-1, self.width*2))
            y_numpy = np.array(y_list).reshape((-1, self.width*2))
            # print(x_numpy.shape)#18行12列
            x_list, y_list = [], []
            if self.flag == None:
                for i in range(0, self.height*2, 2):
                    for j in range(0, self.width*2, 2):
                        if i in [2,6,10,14]:
                            cell_y = y_numpy[i:i + 2, ::-1]
                            ###
                            # cell_y = cell_y[:, j:j + 2].flatten().tolist() #不写cell_y[:, ::-1].flatten().tolist()是另外一种情况
                            cell_y = cell_y[:, j:j + 2]
                            cell_y = cell_y[:, ::-1].flatten().tolist()
                        else:
                            cell_y = y_numpy[i:i + 2, j:j + 2].flatten().tolist()
                            temp = cell_y[2]
                            cell_y[2] = cell_y[3]
                            cell_y[3] = temp
                        cell_x = x_numpy[i:i + 2, j:j + 2].flatten().tolist()
                        print('cell_x',cell_x)
                        print('cell_y_origin', cell_y)
                        # cell_y = y_numpy[i:i + 2, j:j + 2].flatten().tolist()
                        temp = cell_y[2]
                        cell_y[2] = cell_y[3]
                        cell_y[3] = temp
                        print('cell_y', cell_y)
                        x_list.append(cell_x)
                        y_list.append(cell_y)
            elif self.flag == 2:
                for i in range(0, self.height*2, 2):
                    for j in range(0, self.width*2, 2):
                        # print('i',i)
                        if i in [2,6,10,14,18]:
                            cell_x = x_numpy[i:i + 2, j:j + 2].flatten().tolist()
                            temp = cell_x[1]
                            cell_x[1] = cell_x[3]
                            cell_x[3] = temp
                            # print(cell_x)
                            cell_y = y_numpy[i:i + 2, ::-1]
                            cell_y = cell_y[:, j:j + 2]
                            cell_y = cell_y[:, ::-1].flatten().tolist()
                            temp = cell_y[0]
                            cell_y[0] = cell_y[3]
                            cell_y[3] = temp
                            # print(cell_y)
                        else:
                            cell_x = x_numpy[i:i + 2, j:j + 2].flatten().tolist()
                            temp = cell_x[1]
                            cell_x[1] = cell_x[3]
                            cell_x[3] = temp

                            cell_y = y_numpy[i:i + 2, j:j + 2].flatten().tolist()
                            temp = cell_y[1]
                            cell_y[1] = cell_y[2]
                            cell_y[2] = temp
                        x_list.append(cell_x)
                        y_list.append(cell_y)
            x_list = np.array(x_list).flatten().tolist()
            x_list = [round(x,3) for x in x_list]
            y_list = np.array(y_list).flatten().tolist()
            coordinate_list = list(zip(x_list, y_list))
        return coordinate_list

    def get_path_planning_single(self):
        # →→→→→→→→→→→→→→→→→
        # ←←←←←←←←←←←←←←←←←
        # →→→→→→→→→→→→→→→→→
        # ←←←←←←←←←←←←←←←←←
        # →→→→→→→→→→→→→→→→→
        # ←←←←←←←←←←←←←←←←←
        # →→→→→→→→→→→→→→→→→
        # ←←←←←←←←←←←←←←←←←
        # →→→→→→→→→→→→→→→→→
        # x_list,y_list = preprocess()
        # print(x_list,y_list)
        coordinate_list = []
        for index,value in enumerate(self.x_list):
            if index % 2 == 0:
                for i in self.y_list:
                    coordinate = (value,i)
                    coordinate_list.append(coordinate)
            if index % 2 == 1:
                for j in self.y_list[::-1]:
                    coordinate = (value,j)
                    coordinate_list.append(coordinate)
        return coordinate_list



def preprocess():
    x_blank = 12.063
    y_blank = 11.3
    # x_blank = 12.175
    # y_blank = 11.48
    width,height = 6,9
    x_list = [x*(x_blank*1000)/10000 for x in range(0,height*10,5)]
    y_list = [y*(y_blank*100)/1000 for y in range(0,width*10,5)]
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
    # # print(x_list,y_list)
    coordinate_list = []
    for index,value in enumerate(x_list):
        for i in y_list:
            coordinate = (value, i)
            coordinate_list.append(coordinate)
    x_list,y_list = [],[]
    for k,v in coordinate_list:
        x_list.append(k)
        y_list.append(v)
    x_numpy = np.array(x_list).reshape((-1,12))
    y_numpy = np.array(y_list).reshape((-1,12))
    # print(x_numpy.shape)#18行12列
    x_list,y_list = [],[]
    for i in range(0,18,2):
        for j in range(0,12,2):
            cell_x = x_numpy[i:i+2,j:j+2].flatten().tolist()
            cell_y = y_numpy[i:i+2,j:j+2].flatten().tolist()
            temp = cell_y[2]
            cell_y[2] = cell_y[3]
            cell_y[3] = temp
            x_list.append(cell_x)
            y_list.append(cell_y)
    x_list = np.array(x_list).flatten().tolist()
    y_list = np.array(y_list).flatten().tolist()
    coordinate_list = list(zip(x_list,y_list))
    return coordinate_list


if __name__ == '__main__':
    # a = get_path_planning()
    a = PathPlanning(x_blank=10,y_blank=10,width=10,height=10,flag=2).get_path_planning()
    print(a)
    # print(len(a))
    # a 是托盘上的相对坐标，然后在确定第一个物体位置的绝对坐标之后，对每一个坐标进行相加。
