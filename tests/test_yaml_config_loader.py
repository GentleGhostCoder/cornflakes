# import os
# from typing import Any
# from skimage import io
# from cornflakes.decorator.dataclasses import config
# import numpy as np
# from cornflakes.types import Loader
# def rgb2gray(rgb):
#     return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])[..., None]
#
# @config(
#     files="predict.yaml",
#     sections="dataset",
#     is_list=True,
#     default_loader=Loader.YAML,
# )
# class PredictDataSet:
#     """Dataset for prediction."""
#
#     path_sketch: str = ""
#     num_workers: int = 1
#     batch_size: int = 1
#
#     def __post_init__(self):
#         for file in os.listdir(self.path_sketch):
#             if file.endswith(".png"):
#                 # append full path
#                 self.pkl_list.append(file)
#
#         self.pkl_list = sorted(self.pkl_list)
#
#     def __len__(
#             self,
#     ) -> int:
#         return len(self.pkl_list)
#
#     def __getitem__(
#             self, idx
#     ) -> Any:
#         sketch_path = self.pkl_list[idx]
#         sketch = io.imread(sketch_path)
#         sketch[np.where(sketch[:, :, 3] == 0)] = 255
#         sketch = sketch.astype('float32') / 255
#         sketch = ((np.transpose(rgb2gray(sketch[:, :, :3]), (2, 0, 1)) - .5) * 2).astype('float32')
#         return sketch
#
#     def __repr__(self) -> str:
#         return f"Dataset(name={self.name!r}"
#
