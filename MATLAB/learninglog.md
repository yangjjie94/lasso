对于MATLAB谜一样的语言风格，最好还是把学到的及时记下来



## 2018-5-2 23:10:39

用在参数列表中获取xx的函数（虽然长得不像函数）

```matlab
%获取当前图形窗口中当前坐标轴的句柄值。
gca
%获取当前图形窗口的句柄值。
gcf
%获取当前图形窗口中当前对象的句柄值。
gco
%获取回调函数正在执行的对象所在窗口的句柄。
gcbf
%获取调函数正在执行的对象的句柄。
gcbo
```

### `imellipse`

[官网](https://ww2.mathworks.cn/help/images/ref/imellipse.html#bq_5ul3)

An `imellipse` object encapsulates an interactive ellipse
            over an image.

#### Syntax

`h = imellipse`

`h = imellipse(hparent)`

`h = imellipse(hparent,position)`

`h = imellipse(___,Name,Value)`

#### Object Functions

Each `imellipse` object supports a number of methods. Type                `methods imellipse` to see a complete list.

| [`addNewPositionCallback`](https://ww2.mathworks.cn/help/images/ref/imroi.addnewpositioncallback.html) | Add new-position callback to ROI object                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`createMask`](https://ww2.mathworks.cn/help/images/ref/imroi.createmask.html) | Create mask within image                                     |
| [`delete`](https://ww2.mathworks.cn/help/matlab/ref/handle.delete.html) | Delete handle object                                         |
| [`getColor`](https://ww2.mathworks.cn/help/images/ref/imroi.getcolor.html) | Get color used to draw ROI object                            |
| [`getPosition`](https://ww2.mathworks.cn/help/images/ref/imroi.getposition.html) | Return current position of ROI object                        |
| [`getPositionConstraintFcn`](https://ww2.mathworks.cn/help/images/ref/imroi.getpositionconstraintfcn.html) | Return function handle to current position constraint function |
| [`getVertices`](https://ww2.mathworks.cn/help/images/ref/imroi.getvertices.html) | Return vertices on perimeter of ellipse ROI object           |
| [`removeNewPositionCallback`](https://ww2.mathworks.cn/help/images/ref/imroi.removenewpositioncallback.html) | Remove new-position callback from ROI object                 |
| [`resume`](https://ww2.mathworks.cn/help/images/ref/imroi.resume.html) | Resume execution of MATLAB command line                      |
| [`setColor`](https://ww2.mathworks.cn/help/images/ref/imroi.setcolor.html) | Set color used to draw ROI object                            |
| [`setConstrainedPosition`](https://ww2.mathworks.cn/help/images/ref/imroi.setconstrainedposition.html) | Set ROI object to new position                               |
| [`setFixedAspectRatioMode`](https://ww2.mathworks.cn/help/images/ref/imrect.setfixedaspectratiomode.html) | Preserve aspect ratio when resizing ROI object               |
| [`setPosition`](https://ww2.mathworks.cn/help/images/ref/imroi.setposition.html) | Move ROI object to new position                              |
| [`setPositionConstraintFcn`](https://ww2.mathworks.cn/help/images/ref/imroi.setpositionconstraintfcn.html) | Set position constraint function of ROI object               |
| [`setResizable`](https://ww2.mathworks.cn/help/images/ref/imroi.setresizable.html) | Set resize behavior of ROI object                            |
| [`wait`](https://ww2.mathworks.cn/help/images/ref/imroi.wait.html) | Block MATLAB command line until ROI creation is finished     |

`wait`

[官网](https://ww2.mathworks.cn/help/images/ref/imroi.wait.html)

``pos = wait(h)`` blocks execution of the MATLAB® command line until you finish positioning the ROI object `h`. Indicate completion by double-clicking on the ROI object. The function returns the position, `pos`, of the ROI object.

#### e.g.

```matlab
imshow('pout.tif')
h = imrect;
position = wait(h)
```

```matlab
imshow('coins.png')
h = imellipse;
position = wait(h)
```

在上面的input arguments中

- h表示 ROI object

  ROI object, specified as an [`imfreehand`](https://ww2.mathworks.cn/help/images/ref/imfreehand.html), [`imline`](https://ww2.mathworks.cn/help/images/ref/imline.html), [`impoint`](https://ww2.mathworks.cn/help/images/ref/impoint.html), [`impoly`](https://ww2.mathworks.cn/help/images/ref/impoly.html), or [`imrect`](https://ww2.mathworks.cn/help/images/ref/imrect.html) object.

- he 表示 Ellipse ROI object

  llipse ROI object, specified as an [`imellipse`](https://ww2.mathworks.cn/help/images/ref/imellipse.html) object.

#### See Also

[`getPosition`](https://ww2.mathworks.cn/help/images/ref/imroi.getposition.html) | [`getVertices`](https://ww2.mathworks.cn/help/images/ref/imroi.getvertices.html) | [`imroi`](https://ww2.mathworks.cn/help/images/ref/imroi-class.html) | [`resume`](https://ww2.mathworks.cn/help/images/ref/imroi.resume.html)



## 2018-5-2 23:54:52

MATLAB的效率不可小觑，设计时候需要多利用其向量特点进行计算，因为向量的内存空间是在一块的，可以用C的库进行快速运算。



## 2018-5-3 01:59:35

识别圆圈的核心算法

### `imfindcircles`

[官网](https://ww2.mathworks.cn/help/images/ref/imfindcircles.html)

Find circles using circular Hough transform

这个算法非常鲁棒，可以克服噪点、封闭咬合occlusion和亮度变化varying illumination。

#### Syntax

`centers = imfindcircles(A,radius)`

`[centers,radii]= imfindcircles(A,radiusRange)`

`[centers,radii,metric]= imfindcircles(A,radiusRange)`

`[centers,radii,metric]= imfindcircles(___,Name,Value)`



**Strength** means the **number of votes** the circle gets in the Hough accumulator.



`imfindcircles`对图像的对比度contrast of the image敏感，我们有一些[tips](http://www.mathworks.com/help/images/ref/imfindcircles.html?#btdxntz-4)可以用于提高`imfindcircles`识别率：

- 如果图像对比度低，可以通过预处理步骤——对比度均化contrast equalization，函数为'histeq' or 'adapthisteq'
- 如果第一步放大amplify了噪声，那就要先于一步采取一些降噪de-noise方法
- 如果感兴趣的特征依然不显著the features of interest still don't stand out，可以用一些特征提取feature extraction或者特征增强feature enhancement。
- 在很多情况下，正确的检测需要tweak the ‘EdgeThreshold’, ‘Sensitivity’ and 'ObjectPolarity' parameters
- 进一步，如果高Sensitivity找到了过多的spurious circles，可以用‘metric’ output来过滤spurious circles。
- 可以切换'Method' parameter，有两种，可以都试试

另一个完全不同的探测圆圈的方法是`regionprops` 带上'eccentricity' property



#### graythresh

[官网](https://ww2.mathworks.cn/help/images/ref/graythresh.html)

Global image threshold using Otsu's method



## 2018-5-3 10:46:33

### `rgb2gray()`

converting to gray scale





### `regionprops`

[官网](https://www.mathworks.com/help/releases/R2017a/images/ref/regionprops.html)

带上'eccentricity' property。这是一个更灵活和鲁棒的方法，特别是当区域不是perfect circles，或者对比度很低的时候。例如，

操作二值图像，'BW'，可以用下面的命令 

```
stats = regionprops('table', BW, 'Centroid', 'Eccentricity', 'EquivDiameter');
```

会返回图像中每个 区域with it's eccentricity (a measure of how circular something is)、每个圆圈的约化半径approximate diameter和大致圆心approximate center。

更进一步，你可以过滤结果，只接受偏心率小于0.5和直径在80和100个像素之间的:

```
stats( stats.Eccentricity > .5 , : ) = []
stats( stats.EquivDiameter > 80 | stats.EquivDiameter < 100 , : ) = []
```

如果你接下来想画出这些圆，你可以用`viscircles` 函数，以centroids和 radii作为inputs.

### `viscircles`



```matlab
viscircles(centersStrong5, radiiStrong5,'EdgeColor','b');
```





### `imdistline`

交互式测量长度

```matlab
d = imdistline;
```

测量完后可以从交互式界面中删除

```matlab
delete(d)
```



### `imwrite` 



```
imwrite(A,'image_out_1.jpg');
```


2018-5-3 20:26:41

Sobel 和 Canny 边缘检测

```matlab
BW1 = edge(I,'sobel');
BW2 = edge(I,'canny');
figure;
imshowpair(BW1,BW2,'montage')
title('Sobel Filter                                   Canny Filter');
```

![](https://ww2.mathworks.cn/help/examples/images/win64/DetectEdgesInImagesExample_02.png)

