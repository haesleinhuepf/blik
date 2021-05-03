from typing import Callable
import logging

import numpy as np
from xarray import DataArray

from .simpleblock import SimpleBlock
from ...depictors import ImageDepictor


logger = logging.getLogger(__name__)


class ImageBlock(SimpleBlock):
    """
    n-dimensional image block
    data can be interpreted as n-dimensional images
    """
    _depiction_modes = {'default': ImageDepictor}

    def __init__(self, data=(), pixel_size=None, mmap=False, lazy=True, **kwargs):
        # TODO this is a workaround until napari #2347 is fixed
        self.pixel_size = pixel_size  # no checking here, or we screw up lazy loading
        super().__init__(data, **kwargs)

    def _data_setter(self, data):
        data = np.asarray(data)  # asarray does not copy unless needed
        if data.ndim < 2:
            raise ValueError('images must have at least 2 dimensions')
        dims = ('z', 'y', 'x')
        data = DataArray(data, dims=dims[-data.ndim:])

        # set pixel_size if needed
        if self.pixel_size is None or np.all(self.pixel_size == 0):
            pixel_size = np.ones(data.ndim)
            pixel_size = np.broadcast_to(pixel_size, data.ndim)
            self.pixel_size = pixel_size

        return data

    @property
    def ndim(self):
        if isinstance(self._data, Callable):
            return None
        return self.data.ndim

    @property
    def dims(self):
        if isinstance(self._data, Callable):
            return None
        return self.data.dims

    def __shape_repr__(self):
        if isinstance(self._data, Callable):
            return f'(not-loaded)'
        return f'{self.data.shape}'
