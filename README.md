# Visualization
use SMPL model by three.js

使用fbxLoader去加载smpl模型，并对模型的bones去进行操作，使其骨骼节点能根据四元数、欧拉角的数据变化进行旋转。



添加新脚本，直接将npz文件转换为json文件，读取骨骼旋转数据，忽略trans数据。

直接由web读取json文件对动作进行渲染
