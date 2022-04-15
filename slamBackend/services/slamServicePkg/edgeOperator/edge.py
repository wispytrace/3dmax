import cv2 as cv
from scipy import signal
import numpy as np 
import math


class OpBase:


    def __init__(self):

        self.img = None

        self.edge = None
    

    def boundaryDeal(self, img):

        img = np.abs(img)
        img = np.round(img)
        img[img>255]=255
        img = img.astype(np.uint8)

        return img
    
    def normalize(self, img):

        img = np.abs(img)
        img = img/np.max(img)
        img = img * 255
        img = img.astype(np.uint8)

        return img


    def weightMean(self, img1, img2):

        img = 0.5 * img1 + 0.5 * img2

        return img


    def geometricMean(self, img1, img2):

        img = np.sqrt(np.power(img1, 2.0), np.power(img2, 2.0))

        return img


    def check(self, img):
        pass


    def showEdge(self):

        if self.edge is None:
            print("failed! please check frist!")
            return
        
        cv.imshow("img",self.img)
        cv.imshow("edge",self.edge)
        cv.waitKey(0)
        cv.destroyAllWindows()







# Roberts边缘检测算法是图像，分别与下面两个卷积核（锚点为1所在位置）进行卷积运算。
# 第一个为135度方向像素值差分，第二个为45度方向像素值差分，可以发现卷积后，图像内部由于相近像素值会变为0，成为黑色背景，而边缘处由于像素值相差大，相减的差分值作为新的像素值。
# 因此能够将图像边缘处的像素值识别出来，得到图像的轮廓
class Robert(OpBase):
    

    def check(self, img):

        self.img = img
        H1,W1 = self.img.shape[:2]
        r1 = np.array([[1,0],[0,-1]],np.float32)
        r2 = np.array([[0,1],[-1,0]],np.float32)
        H2,W2= 2, 2                                                                                #锚点位置


        kr1,kc1=0, 0
        con_r1 = signal.convolve2d(self.img, r1,mode="full", boundary="symm", fillvalue=0)
        con_r1 = con_r1[H2-kr1-1:H1+H2-kr1-1,W2-kc1-1:W1+W2-kc1-1]                                 #截取出same卷积
        edge_135 = self.boundaryDeal(con_r1)


        kr2,kc2=0,1
        con_r2 = signal.convolve2d(self.img, r2, mode="full", boundary="symm", fillvalue=0)
        con_r2 = con_r2[H2-kr2-1:H1+H2-kr2-1,W2-kc2-1:W1+W2-kc2-1]
        edge_45 = self.boundaryDeal(con_r2)
        

        edge = self.geometricMean(edge_135, edge_45)
        edge = self.boundaryDeal(edge)


        self.edge = edge

        return edge
        



# prewitt垂直算子，相当于先进行水平方向的均值平滑，再进行垂直方向的差分卷积[1,0,-1]。
# 所以相比于Robert算子，Prewitt算子多了一个平滑操作[1,1,1]，所以其受噪声干扰小。
class Prewitt(OpBase):              
    

    def check(self, img):

        self.img = img

        rx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]],np.float32)
        ry = np.array([[1,1,1],[0,0,0],[-1,-1,-1]],np.float32)


        con_x = signal.convolve2d(self.img, rx,mode="full", boundary="symm", fillvalue=0)      #也可以分别进行垂直均值平滑卷积，然后水平差分卷积，来加速运算
        edge_x = self.boundaryDeal(con_x)


        con_y = signal.convolve2d(self.img, ry, mode="full", boundary="symm", fillvalue=0)
        edge_y = self.boundaryDeal(con_y)
        

        edge = self.weightMean(edge_x, edge_y)
        edge = self.boundaryDeal(edge)


        self.edge = edge
        
        return edge


# sobel算子的两个卷积核如下，也分为水平方向和垂直方向的卷积核（锚点为中心点），其卷积核也是可以差分，
# 相比于prewitt算子，只是其平滑卷积核由均值平滑变成了高斯平滑，差分卷积核还是一样的。差分卷积核一样为[1, 0, -1]
class Sobel(OpBase):              
    

    #n阶的二项展开式系数,构建一维高斯平滑矩阵
    def getsmooth(self, n=5):
        smooth = np.zeros([1,n],np.float32) 
        for i in range(n):
            smooth[0][i] = math.factorial(n-1)/(math.factorial(i)*math.factorial(n-i-1))
        return smooth


    def getdiff(self, n=5):
        diff = np.zeros([1,n],np.float32)
        smooth = self.getsmooth(n-1)
        for i in range(n):
            if i==0:
                diff[0][i]=smooth[0][i]  #恒等于1
            elif i==n-1:
                diff[0][i] = -smooth[0][i-1]  #恒等于-1
            else:
                diff[0][i] = smooth[0][i] - smooth[0][i-1]
        return diff
        


    def check(self, img):

        self.img = img

        smooth = self.getsmooth()
        diff = self.getdiff()


        print(smooth,diff)
        print(np.dot(smooth.transpose(),diff))
        print(np.dot(diff.transpose(),smooth))


        #水平方向的sobel算子：先进行垂直方向的高斯平滑，再进行水平方向的差分
        gaussian_y = signal.convolve2d(self.img, smooth.transpose(), mode="same", boundary="symm", fillvalue=0)
        sobel_x = signal.convolve2d(gaussian_y, diff, mode="same", boundary="symm", fillvalue=0)
        sobel_x = self.normalize(sobel_x)


        gaussian_x = signal.convolve2d(self.img,smooth, mode="same", boundary="symm", fillvalue=0)
        sobel_y = signal.convolve2d(gaussian_x,diff.transpose(), mode="same", boundary="symm", fillvalue=0)
        sobel_y = self.normalize(sobel_y)


        sobel_edge = self.geometricMean(sobel_x, sobel_y)
        sobel_edge = self.normalize(sobel_edge)


        self.edge = sobel_edge

        return sobel_edge

# scharr算子和3阶的Sobel边缘检测算子类似,换了个卷积核，里面的均值系数设的很大
# dst= cv2.Scharr(src,ddepth,dx,dy,scale,delta,borderType)
#         src: 输入图像对象矩阵,单通道或多通道
#         ddepth:输出图片的数据深度,注意此处最好设置为cv.CV_32F或cv.CV_64F
#         dx:dx不为0时，img与差分方向为水平方向的Sobel卷积核卷积
#         dy: dx=0,dy!=0时，img与差分方向为垂直方向的Sobel卷积核卷积
        
#             dx=1,dy=0: 与差分方向为水平方向的Sobel卷积核卷积
#             dx=0,dy=1: 与差分方向为垂直方向的Sobel卷积核卷积
# 　　　　　　　（注意必须满足： dx >= 0 && dy >= 0 && dx+dy == 1）
        
#         scale: 放大比例系数
#         delta: 平移系数
#         borderType:边界填充类型
class Scharr(OpBase):


    def check(self, img):

        self.img = img
        #注意此处的ddepth不要设为-1，要设为cv.CV_32F或cv.CV_64F，否则会丢失太多信息
        scharr_edge_x = cv.Scharr(self.img, ddepth=cv.CV_32F, dx=1, dy=0) 
        scharr_edge_x = self.normalize(scharr_edge_x)

        scharr_edge_y = cv.Scharr(self.img, ddepth=cv.CV_32F, dx=0, dy=1)
        scharr_edge_y = self.normalize(scharr_edge_y)

        scharr_edge = self.weightMean(scharr_edge_x, scharr_edge_y)

        self.edge = scharr_edge

        return scharr_edge
        
# Sobel，Scharr算子等边缘检测算法，只是对检测到的边缘进行了超阈值处理(超过255的像素点截断等)， 
# Canny边缘算法，是在sobel算法的基础上，对边缘像素进行更细致的后处理，过滤掉部分非边缘点，从而使得到便边缘更加细致准确。
# Canny边缘检测可以细分为三步：

# 采用Sobel卷积核进行卷积运算：分别采用水平方向和垂直方向的sobel算子，卷积计算出水平方向梯度和竖直方向梯度，然后我们可以计算图像中每个像素的梯度大小，梯度方向，梯度方向通常垂直于边缘方向。

# 基于边缘梯度方向的非极大值抑制: 在得到每个像素的梯度大小和方向后，我们遍历每个像素，判断该像素的梯度大小在该像素梯度方向上是否是其邻域中的局部最大值。按照这样的规则遍历每一个像素点，对于非极大值的像素点，需要将其梯度大小置为0

# 双阈值的滞后阈值处理：
# 这一步我们设置两个阈值，遍历所有像素：
# 梯度大小大于tmax的像素点被归为“确定边缘”像素，被保留；
# 梯度大小小于tmin的像素点被认为一定不属于边缘，被丢弃。
# 梯度大小介于tmax 和 tmin之间的像素点，如果它们连接到“确定边缘”像素，则它们被视为边缘的一部分。否则，它们也会被丢弃。　

# edges=cv.Canny(image, threshold1, threshold2, apertureSize=3, L2gradient=False)
#     image:输入图像对象矩阵,单通道或多通道
#     threshold1: 代表双阈值中的低阈值
#     threshold2: 代表双阈值中的高阈值
#     apertureSize: spbel核的窗口大小，默认为3*3
#     L2gradient: 代表计算边缘梯度大小时使用的方式，True代表使用平方和开方的方式，False代表采用绝对值和的方式，默认为False    

class Canny(OpBase):

    def check(self, img):

        self.img = img

        canny_edg = cv.Canny(self.img, threshold1=180, threshold2=230, apertureSize=5, L2gradient=True)

        self.edge = canny_edg

        return self.edge


# Laplacian算子采用二阶导数，其计算公式如下：(分别对x方向和y方向求二阶导数，并求和),个人认为噪声影响可能会很大，因为求导会放大噪声
# 对应的卷积核为，三阶方阵，中间为-4，上下左右为1
# dst = cv2.Laplacian(src, ddepth, ksize, scale, delta, borderType)
#     src: 输入图像对象矩阵,单通道或多通道
#     ddepth:输出图片的数据深度,注意此处最好设置为cv.CV_32F或cv.CV_64F
#     ksize: Laplacian核的尺寸，默认为1，采用上面3*3的卷积核
#     scale: 放大比例系数
#     delta: 平移系数
#     borderType: 边界填充类型
# Laplacina算子进行边缘提取后，可以采用不同的后处理方法: 取绝对值后归一化、边界处理、高斯平滑处理。
class Laplacian(OpBase):
    
    def check(self, img):

        self.img = img

        laplacian_edge = cv.Laplacian(self.img, cv.CV_32F)
        laplacian_edge = self.normalize(laplacian_edge)

        self.edge = laplacian_edge

        return laplacian_edge


# 拉普拉斯算子没有对图像做平滑处理，会对噪声产生明显的响应，所以一般先对图片进行高斯平滑处理，再采用拉普拉斯算子进行处理，但这样要进行两次卷积处理。
# 高斯拉普拉斯(LoG)边缘检测，是将两者结合成一个卷积核，只进行一次卷积运算。

class LoG(OpBase):

    def check(self, img):

        self.img = img

        sigma = 1
        H, W = (11, 11)

        r, c = np.mgrid[0:H:1.0, 0:W:1.0]
        r -= (H-1)/2
        c -= (W-1)/2

        sigma2 = np.power(sigma, 2.0)
        norm2 = np.power(r, 2.0) + np.power(c, 2.0)

        LoGKernel = (norm2/sigma2 -2)*np.exp(-norm2/(2*sigma2))  # 省略掉了常数系数 1\2πσ4

        print(norm2)
        print(LoGKernel)

        LoG_edge = signal.convolve2d(self.img, LoGKernel, 'same', boundary='symm')
        LoG_edge = self.boundaryDeal(LoG_edge)

        self.edge = LoG_edge

        return LoG_edge


# 高斯差分(Difference of Gaussian, DoG), 是高斯拉普拉斯(LoG)的一种近似，两者之间的关系推导如下：
# 当k趋向于1时候（取k=0.95）, sigma * Laplace^2 = dG/dsigma , 其实就是把求二阶导数变成了求一阶导数?
# 构建窗口大小为HxW，标准差为的DoG卷积核(H, W一般为奇数，且相等)
# 图像与两个高斯核卷积，卷积结果计算差分
# 边缘后处理

class DoG(OpBase):

    # 二维高斯卷积核拆分为水平核垂直一维卷积核，分别进行卷积
    def gaussConv(self, image, size, sigma):

        H, W = size
        # 先水平一维高斯核卷积
        xr, xc = np.mgrid[0:1, 0:W]
        xc = xc.astype(np.float32)
        xc -= (W-1.0)/2.0
        xk = np.exp(-np.power(xc, 2.0)/(2*sigma*sigma))
        image_xk = signal.convolve2d(image, xk, 'same', 'symm')

        # 垂直一维高斯核卷积
        yr, yc = np.mgrid[0:H, 0:1]
        yr = yr.astype(np.float32)
        yr -= (H-1.0)/2.0
        yk = np.exp(-np.power(yr, 2.0)/(2*sigma*sigma))
        image_yk = signal.convolve2d(image_xk, yk, 'same','symm')
        image_conv = image_yk/(2*np.pi*np.power(sigma, 2.0))

        return image_conv


    #直接采用二维高斯卷积核，进行卷积
    def gaussConv2(self, image, size, sigma):
        H, W = size
        r, c = np.mgrid[0:H:1.0, 0:W:1.0]
        c -= (W - 1.0) / 2.0
        r -= (H - 1.0) / 2.0
        sigma2 = np.power(sigma, 2.0)
        norm2 = np.power(r, 2.0) + np.power(c, 2.0)
        LoGKernel = (1 / (2*np.pi*sigma2)) * np.exp(-norm2 / (2 * sigma2))
        image_conv = signal.convolve2d(image, LoGKernel, 'same','symm')

        return image_conv


    def deviate(self, sigma, k, size):



        Is = self.gaussConv(self.img, size, sigma)
        Isk = self.gaussConv(self.img, size, sigma*k)

        doG = Isk - Is
        doG /= (np.power(sigma, 2.0)*(k-1))
        
        return doG
    
    def check(self, img):

        self.img = img

        sigma = 1
        k = 1.1
        size = (7, 7)

        dog_edg = self.deviate(sigma, k, size)
        dog_edg = self.normalize(dog_edg)

        self.edge = dog_edg

        return dog_edg

# Marri-Hildreth边缘检测算法
# 高斯拉普拉斯和高斯差分边缘检测，得到边缘后，只进行了简单的阈值处理，Marr-Hildreth则对其边缘进行了进一步的细化，使边缘更加精确细致，就像Canny对sobel算子的边缘细化一样。

# Marr-Hildreth边缘检测可以细分为三步：

# 构建窗口大小为H*W的高斯拉普拉斯卷积核(LoG)或高斯差分卷积核(DoG)

# 图形矩阵与LoG核或DoG核卷积

# 在第二步得到的结果中，寻找过零点的位置，过零点的位置即为边缘位置

# 　　第三步可以这么理解，LoG核或DoG核卷积后表示的是二阶导数，二阶导数为0表示的是一阶导数的极值，而一阶导数为极值表示的是变化最剧烈的地方，因此对应到图像边缘提取中，二阶导数为0，表示该位置像素点变化最明显，即最有可能是边缘交接位置。

# 　　对于连续函数g(x), 如果g(x1)*g(x2) < 0，即 g(x1) 和g(x2) 异号，那么在x1，x2之间一定存在x 使得g(x)=0， 则x为g(x)的过零点。在图像中，Marr-Hildreth将像素点分为下面四种情况，分别判断其领域点之间是否异号：

class Marri(DoG):
    

    def isCross(self, x1, x2):

        return (int(x1) ^ int(x2)) < 0



    def zero_cross_default(self, doG):

        zero_cross = np.zeros(doG.shape, np.uint8)
        rows, cols = doG.shape
        for r in range(1, rows-1):
            for c in range(1, cols-1):
                if self.isCross(doG[r][c-1], doG[r][c+1]):
                    zero_cross[r][c] = 255
                    continue
                if self.isCross(doG[r-1][c], doG[r+1][c]):
                    zero_cross[r][c] = 255
                    continue
                if self.isCross(doG[r-1][c-1], doG[r+1][c+1]):
                    zero_cross[r][c] = 255
                    continue
                if self.isCross(doG[r-1][c+1], doG[r+1][c-1]):
                    zero_cross[r][c] = 255
                    continue
        return zero_cross


    def check(self, img):

        self.img = img

        sigma = 1
        k = 1.1
        size = (7, 7)

        doG = super().deviate(sigma, k, size)

        self.edge = self.zero_cross_default(doG)

        return self.edge


if __name__ == '__main__':
    img = cv.imread('/home/wispy/imageSegment/edgeOperator/render.jpg', 0)

    myop = Marri(img)

    myop.check()

    myop.showEdge()