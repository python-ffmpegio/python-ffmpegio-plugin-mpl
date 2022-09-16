import numpy as np
# from matplotlib.animation import FFMpegWriter
from matplotlib import pyplot as plt
import ffmpegio

np.random.seed(0)
fig, ax = plt.subplots(figsize=(9, 4),dpi=300)
ln, = ax.plot([])
ax.set_xlim([0, 1000])
ax.set_ylim([-1, 1])
ax.grid(True)

# writer = FFMpegWriter(fps=1)
# with writer.saving(fig, "writer_test.mp4", 300):
with ffmpegio.open(
  "sandbox/writer_test.mp4", # output file name
  "wv", # open file in write-video mode
  1, # framerate in frames/second
  pix_fmt="yuv420p", # specify the pixel format (default is yuv444p)
  overwrite=True
) as writer:
    for i in range(20):
        x = np.arange(1000)
        t = np.random.randn(1000)
        y = np.sin(2 * np.pi * t)
        ln.set_data(x, y)
        writer.write(fig)
# plt.show()
