
% I = im2double(imread('S001_0001.tif'));
% subplot(1,2,1),imshow(I)
% mask = createMask(imellipse(gca));
% subplot(1,2,2),imshow(I.*mask)
% 
% I = imread('cameraman.tif');
% subplot(1,2,1),imshow(I)
% A = imcrop(I,getrect);
% subplot(1,2,2),imshow(A)

% imshow('coins.png')
% h = imellipse(gca,[10 10 100 100]);
% addNewPositionCallback(h,@(p) title(mat2str(p,3)));
% fcn = makeConstrainToRectFcn('imellipse',get(gca,'XLim'),get(gca,'YLim'));
% setPositionConstraintFcn(h,fcn);

% imshow('pout.tif')
% h = imrect;
% position = wait(h)

openExample('images/DetectCirclesExample')