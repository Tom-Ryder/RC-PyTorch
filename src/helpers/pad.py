"""
Copyright 2020, ETH Zurich

This file is part of RC-PyTorch.

RC-PyTorch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

RC-PyTorch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RC-PyTorch.  If not, see <https://www.gnu.org/licenses/>.
"""
from fjcommon import functools_ext as ft
from torch.nn import functional as F


def pad(img, fac, mode='replicate'):
    """
    pad img such that height and width are divisible by fac
    """
    _, _, h, w = img.shape
    padH = fac - (h % fac)
    padW = fac - (w % fac)
    if padH == fac and padW == fac:
        return img, ft.identity
    if padH == fac:
        padTop = 0
        padBottom = 0
    else:
        padTop = padH // 2
        padBottom = padH - padTop
    if padW == fac:
        padLeft = 0
        padRight = 0
    else:
        padLeft = padW // 2
        padRight = padW - padLeft
    assert (padTop + padBottom + h) % fac == 0
    assert (padLeft + padRight + w) % fac == 0

    def _undo_pad(img_):
        # the or None makes sure that we don't get 0:0
        img_out = img_[..., padTop:(-padBottom or None), padLeft:(-padRight or None)]
        assert img_out.shape[-2:] == (h, w), (img_out.shape[-2:], (h, w), img_.shape,
                                              (padLeft, padRight, padTop, padBottom))
        return img_out

    return F.pad(img, (padLeft, padRight, padTop, padBottom), mode), _undo_pad
