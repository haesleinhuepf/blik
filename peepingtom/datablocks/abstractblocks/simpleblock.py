from abc import abstractmethod
import logging

from xarray import DataArray

from .datablock import DataBlock


logger = logging.getLogger(__name__)


class SimpleBlock(DataBlock):
    """
    Base class for all simple DataBlock objects, data types which can be visualised by Depictors
    and are defined by a single xarray `data` attribute

    SimpleBlock objects must implement a data setter method as _data_setter which returns
    the appropriately formatted data

    Calling __getitem__ on a SimpleBlock will call __getitem__ on its data property and return a view
    """
    def __init__(self, *, data=None, lazy_loader=None, **kwargs):
        super().__init__(**kwargs)
        if (data is None and lazy_loader is None) or \
           (data is not None and lazy_loader is not None):
            raise ValueError('either one of data or lazy_loader must be provided')
        self._lazy_loader = lazy_loader
        self._loaded = lazy_loader is None
        self._data = None
        self.data = data

    @property
    def data(self):
        self.load()
        return self._data

    @data.setter
    def data(self, data):
        if isinstance(data, type(self)):
            self._data = data.data
        elif isinstance(data, DataArray) or data is None:
            self._data = data
        else:
            self._data = self._data_setter(data)
        self.update()

    def load(self):
        if not self._loaded and self._lazy_loader is not None:
            logger.debug(f'loading data for lazy datablock "{self.__short_repr__()}"')
            self.data = self._lazy_loader()
            self._loaded = True

    def unload(self):
        if self._loaded and self._lazy_loader is not None:
            self._data = ()
            self._loaded = False

    @property
    def nbytes(self):
        return self.data.nbytes

    @abstractmethod
    def _data_setter(self, data):
        """
        takes raw data and returns it properly formatted to the SimpleBlock subclass specification.
        """

    def __setitem__(self, key, value):
        self.data[key] = value
        self.update()

    def __getitem__(self, key):
        return self.__view__(data=self.data[key])

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        yield from self.data

    def __reversed__(self):
        yield from reversed(self.data)

    def __repr__(self):
        data_repr = ''
        if self._loaded:
            data_repr = f'\n{self.data}'
        return f'{self.__short_repr__()}{data_repr}'
