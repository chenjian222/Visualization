import json
import os

import numpy as np
import torch


def format_pose_npz_to_pt(npz_path):
    # 读取npz文件
    data = np.load(npz_path)
    data = data['poses']
    # smpl-h的数据
    data = torch.Tensor(data.reshape(data.shape[0], -1, 3))
    data[:, 23] = data[:, 37]  # right hand
    pose = data[:, :24].clone()
    quaternion_pose = axis_angle_to_quaternion(pose).reshape(-1, 4).tolist()
    quaternion_pose_str = str(quaternion_pose).replace("[[", "[").replace("],", "]").replace("]]", "]").replace(" ","")
    quaternion_pose_dict = {'data': quaternion_pose_str}

    json_data = json.dumps(quaternion_pose_dict)
    f2 = open('quaternion.json', 'w')
    f2.write(json_data)
    f2.close()



def normalize_tensor(x: torch.Tensor, dim=-1, return_norm=False):
    r"""
    Normalize a tensor in a specific dimension to unit norm. (torch)

    :param x: Tensor in any shape.
    :param dim: The dimension to be normalized.
    :param return_norm: If True, norm(length) tensor will also be returned.
    :return: Tensor in the same shape. If return_norm is True, norm tensor in shape [*, 1, *] (1 at dim)
             will also be returned (keepdim=True).
    """
    norm = x.norm(dim=dim, keepdim=True)
    normalized_x = x / norm
    return normalized_x if not return_norm else (normalized_x, norm)


def axis_angle_to_quaternion(a: torch.Tensor):
    r"""
    Turn axis-angles into quaternions. (torch, batch)

    :param a: Axis-angle tensor that can reshape to [batch_size, 3].
    :return: Quaternion wxyz tensor of shape [batch_size, 4].
    """
    axes, angles = normalize_tensor(a.view(-1, 3), return_norm=True)
    axes[torch.isnan(axes)] = 0
    q = torch.cat(((angles / 2).cos(), (angles / 2).sin() * axes), dim=1)
    return q






if __name__ == '__main__':
    format_pose_npz_to_pt("poses.npz")