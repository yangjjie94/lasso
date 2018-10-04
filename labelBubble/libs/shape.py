# -*- coding: utf-8 -*-

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.lib import distance
import sys

DEFAULT_LINE_COLOR = QColor(0, 255, 0, 128)
DEFAULT_FILL_COLOR = QColor(255, 0, 0, 128)
DEFAULT_SELECT_LINE_COLOR = QColor(255, 255, 255)
DEFAULT_SELECT_FILL_COLOR = QColor(0, 128, 255, 155)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
DEFAULT_HVERTEX_FILL_COLOR = QColor(255, 0, 0)

class Line(object):
    P_SQUARE, P_ROUND = range(2)

    MOVE_VERTEX, NEAR_VERTEX = range(2)

    # The following class variables influence the drawing
    # of _all_ shape objects.
    line_color = DEFAULT_LINE_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR  # highlight vrtx
    point_type = P_ROUND
    point_size = 6
    scale = 1.0
    max_order = 0


    def __init__(self, line_color=None):
        self.points = []
        self.selected = False

        self._highlightIndex = None
        self._highlightMode = self.NEAR_VERTEX
        self._highlightSettings = {
            self.NEAR_VERTEX: (4, self.P_ROUND),
            self.MOVE_VERTEX: (1.5, self.P_SQUARE),
        }

        self.order = Line.max_order
        Line.max_order += 1

        self.length = None

        if line_color is not None:
            # Override the class line_color attribute
            # with an object attribute. Currently this
            # is used for drawing the pending line a different color.
            self.line_color = line_color


    def reachMaxPoints(self):
        if len(self.points) >= 2:
            return True
        return False

    def addPoint(self, point):
        if not self.reachMaxPoints():
            self.points.append(point)

    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None


    # def setOpen(self):
    #     self._closed = False

    def paint(self, painter):
        if self.points:
            color = self.select_line_color if self.selected else self.line_color
            pen = QPen(color)
            # Try using integer sizes for smoother drawing(?)
            pen.setWidth(max(1, int(round(2.0 / self.scale))))
            painter.setPen(pen)

            line_path = QPainterPath()
            vrtx_path = QPainterPath()

            line_path.moveTo(self.points[0])
            # Uncommenting the following line will draw 2 paths
            # for the 1st vertex, and make it non-filled, which
            # may be desirable.
            #self.drawVertex(vrtx_path, 0)

            for i, p in enumerate(self.points):
                line_path.lineTo(p)
                self.drawVertex(vrtx_path, i)

            painter.drawPath(line_path)
            painter.drawPath(vrtx_path)
            painter.fillPath(vrtx_path, self.vertex_fill_color)

    def makePath(self):
        path = QPainterPath(self.points[0])
        if len(self.points) > 1:
            for p in self.points[1:]:
                path.lineTo(p)
            return path
        else:
            return None

    def drawVertex(self, path, i):
        d = self.point_size / self.scale
        shape = self.point_type
        point = self.points[i]
        if i == self._highlightIndex:
            size, shape = self._highlightSettings[self._highlightMode]
            d *= size
        if self._highlightIndex is not None:
            self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = Line.vertex_fill_color
        if shape == self.P_SQUARE:
            path.addRect(point.x() - d / 2, point.y() - d / 2, d, d)
        elif shape == self.P_ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        else:
            assert False, "unsupported vertex shape"   

    def makePath(self):
        path = QPainterPath(self.points[0])
        for p in self.points[1:]:
            path.lineTo(p)
        return path

    def boundingRect(self):
        return self.makePath().boundingRect()

    def moveBy(self, offset):
        self.points = [p + offset for p in self.points]

    def moveVertexBy(self, i, offset):
        self.points[i] = self.points[i] + offset

    def highlightVertex(self, i, action):
        self._highlightIndex = i
        self._highlightMode = action

    def highlightClear(self):
        self._highlightIndex = None

    def copy(self):
        shape = Line("%s" % self.label)
        shape.points = [p for p in self.points]
        shape.fill = self.fill
        shape.selected = self.selected
        shape._closed = self._closed
        if self.line_color != Line.line_color:
            shape.line_color = self.line_color
        if self.fill_color != Line.fill_color:
            shape.fill_color = self.fill_color
        shape.difficult = self.difficult
        return shape

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __str__(self):
            return self.points.__str__()

    def __repr__(self):
            return (super().__repr__() + '\n' + 
                    self.points.__str__())



















print()
def isvalid(pts):
    # 如果pts是空的
    if len(pts) == 0:
        return False
    # 如果不满足 正好4个一组
    if np.mod(len(pts), 4) != 0:
        return False
    # 如果每组四个点两两之间的距离过大（大于250）
    for start, stop in zip(range(0, len(pts)-1, 4), range(4, len(pts)+1, 4)): 
        for a, b in itertools.combinations(pts[start: stop], 2): 
            if (abs(a[0] - b[0]) > 250 or abs(a[1] - b[1]) > 250):
                return False
    if False:# 如果没有按照对角线顺序选取
        return False
#     if s=input("Sure to sumbit?") # 用户确认功能
    else:
        return True

# 如果每组四个点对应的两条线段相交
def isintersected(pts):
    assert(len(pts) == 4)
    def isseperated(pts):
        """如果p1,p2在P3,p4直线的两边，则返回True，否则返回False"""
        p1,p2,p3,p4 = pts
        # 先求斜率a，注意x1-x2!=0时，直接用x坐标进行比较
        if abs(p1[0]-p2[0]) < 1e-6:
            if abs(p1[1]-p2[1]) < 1e-6:
                return False
            elif (p3[0]-p1[0]) * (p4[0]-p1[0]) < 0:
                return True
            else:
                return False
        elif abs(p1[1]-p2[1]) < 1e-6:
            if (p3[0]-p1[0]) * (p4[0]-p1[0]) < 0:
                return True
            else:
                return False
        else:
            a = (p1[1]-p2[1])/(p1[0]-p2[0])
            b = p1[1] - a * p1[0]
            if not ((p3[1] > a * p3[1] + b) and (p4[1] > a * p4[1] + b)):
                return True
            return False
        
    return (isseperated(pts) and isseperated(reversed(pts)))

#iimg 为图片的编号，如果你想从0005号图片开始标注，请输入4，可以理解为跳过前4张图片
def mark_image(idir, isubdir, iimg=0, stop=3767, step = 1, sample = None):
    img_paths = glob.glob(PATH+"\\"+dirs[idir]+"\\"+subdirs[dirs[idir]][isubdir]+"\\*.jpg")
    # 如果输入参数没有什么错误，就进行切片
    if ((idir in range(len(dirs))) 
        and (isubdir in range(len(subdirs[dirs[idir]]))) 
        and (iimg not in range(3767))
        and (stop not in range(3767))):
        print("Invalid input: \n(index of image must range between 0 - 3766)\n")
        return
    img_paths = img_paths[iimg:stop:step]
    if img_paths == []:
        return
    
    print("开始标注%s中的图片" % dirs[idir]+subdirs[dirs[idir]][isubdir])
    
    if(os.path.exists(os.getcwd()+"\\data_" + str(subdirs[dirs[idir]][isubdir]) + ".csv")):
        print("Note that there already exist data, please check whether to remove")
    
    for img_index, img_path in zip(range(iimg,stop,step), img_paths):
        name_experiment = img_path.split(".")[0].split("\\")[-1].split("_")[0]
        name_pic = img_path.split(".")[0].split(" / ")[-1].split("_")[-1]
        print("正在标注%s:" % name_pic)
        im = Image.open(img_path)
        plt.imshow(im)
        grid_X,grid_Y =  zip(*[(200,100),(200,600), (200,100),(1000,100),
                               (200,350),(1000,350),(400,100),(400,600),
                               (600,100),(600,600), (800,100),(800,600)])
        for n_grid in range(min(len(grid_X),len(grid_Y)) // 2):
            plt.plot(grid_X[2*n_grid: 2*n_grid+2], grid_Y[2*n_grid: 2*n_grid+2],'k--',lw=1)
        grid_X,grid_Y =  zip(*[(1000,100),(1000,600),(200,600),(1000,600)])
        for n_grid in range(min(len(grid_X),len(grid_Y)) // 2):
            plt.plot(grid_X[2*n_grid: 2*n_grid+2], grid_Y[2*n_grid: 2*n_grid+2],'k-',lw=1)
        
        plt.title(name_experiment + ": " + str(idir) + " / " + str(isubdir) + " / " + name_pic)

        pts = []
        pts = plt.ginput(n=-1, timeout=0, show_clicks=True)

        
        # 如果数据不合格就重新标注一遍
        if not isvalid(pts):
            print("重新标注%s" % name_pic)
            pts = []
            mark_image(idir, isubdir, iimg=img_index, stop=img_index+1)
            continue
        
        print("完成标注 %s:" %name_pic)
        # 保存数据
        n_circle = int(len(pts)/4)
        circle = []
        for i in range(n_circle):
            circle += [i] * 4
        df_circle = pd.DataFrame(circle, columns=['circle'])
        df_dir = pd.DataFrame({'dir':[dirs[idir]]*len(pts),
                               'subdir': [subdirs[dirs[idir]][isubdir]]*len(pts), 
                               "timestamp":[time.asctime()]*len(pts),
                               "pic":name_pic})
        df_pts = pd.DataFrame(pts, columns=list("xy"), copy=True)
        df_data = pd.concat([df_pts, df_circle,df_dir], axis=1)
        print(df_data)
        if not os.path.exists("NDD"):
            os.mkdir('NDD')
#         if 'NDD' not in os.path.dirname(os.getcwd()):
#             os.mkdir('NDD')    
        df_data.to_csv(os.getcwd()+"\\NDD\\data_" + str(subdirs[dirs[idir]][isubdir]) + ".csv",mode='a', header=False)
        print("数据保存完毕")
    print("所有数据保存完毕，程序退出")
    plt.close()
    return None