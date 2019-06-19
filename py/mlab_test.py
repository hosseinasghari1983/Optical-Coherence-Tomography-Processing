import numpy as np
from mayavi import mlab
import time

x, y, z = np.ogrid[-10:10:50j, -10:10:50j, -10:10:20j]
s = np.sin(x * y * z) / (x * y * z)
# s = np.random.random((50, 50, 20))

print(f's with type {type(s)} \n'
      f'and size {s.shape}')

# mlab.show()

plane = mlab.pipeline.image_plane_widget(mlab.pipeline.scalar_field(s),
                                         plane_orientation='z_axes',
                                         slice_index=10,
                                         )

# mlab.volume_slice(s, plane_orientation='z_axes', slice_index=10)
mlab.outline()

vol = mlab.pipeline.volume(mlab.pipeline.scalar_field(s))


@mlab.animate(delay=100)
def anim():
    global s
    while True:
        s = s + np.random.random((50, 50, 20)) * .3
        plane.mlab_source.scalars = s
        vol.mlab_source.scalars = s
        yield

anim()
mlab.show()
