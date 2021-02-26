import numpy as np

from peepingtom.io_.write.mrc import write_mrc
from peepingtom.datablocks import ImageBlock


def test_write_mrc(tmp_path):
    file_path = tmp_path / 'test.mrc'
    imageblock = ImageBlock(np.ones((3, 3, 3), dtype=np.float32))
    write_mrc(imageblock, str(file_path))
