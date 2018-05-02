对于MATLAB谜一样的语言风格，最好还是把学到的及时记下来



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

2018-5-2 23:10:39

`imellipse`

[官网](https://ww2.mathworks.cn/help/images/ref/imellipse.html#bq_5ul3)

An `imellipse` object encapsulates an interactive ellipse
            over an image.

### Syntax

`h = imellipse`

`h = imellipse(hparent)`

`h = imellipse(hparent,position)`

`h = imellipse(___,Name,Value)`

## Object Functions

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

e.g.

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

See Also

[`getPosition`](https://ww2.mathworks.cn/help/images/ref/imroi.getposition.html) | [`getVertices`](https://ww2.mathworks.cn/help/images/ref/imroi.getvertices.html) | [`imroi`](https://ww2.mathworks.cn/help/images/ref/imroi-class.html) | [`resume`](https://ww2.mathworks.cn/help/images/ref/imroi.resume.html)



2018-5-2 23:54:52

MATLAB的效率不可小觑，设计时候需要多利用其向量特点进行计算，因为向量的内存空间是在一块的，可以用C的库进行快速运算。


