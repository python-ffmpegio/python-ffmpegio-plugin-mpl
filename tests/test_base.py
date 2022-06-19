try:
    from math import prod
except:
    from functools import reduce
    from operator import mul

    prod = lambda seq: reduce(mul, seq, 1)
import tempfile
from os import path
import numpy as np
from matplotlib import pyplot as plt
from ffmpegio import plugins, open as ffopen
import pytest


@pytest.fixture(scope="module")
def x():
    yield np.arange(0, 2 * np.pi, 0.01)


@pytest.fixture(scope="module")
def plot_figure(x):

    h = 1080
    w = 1920
    dpi = 120

    fig, ax = plt.subplots(figsize=(w / dpi, h / dpi), dpi=dpi)

    (line,) = ax.plot(x, np.sin(x))

    yield (h, w, 4), fig, line

    plt.close(fig)


def test_hooks(plot_figure):

    figsize, fig, _ = plot_figure
    hook = plugins.get_hook()
    assert hook.video_info(obj=fig) == (figsize, "|u1")
    assert len(hook.video_bytes(obj=fig)) == prod(figsize)


def test_video(x, plot_figure):

    _, fig, line = plot_figure

    interval = 20  # delay in milliseconds
    save_count = 50  # number of frames

    def animate(i):
        line.set_ydata(np.sin(x + i / 50))  # update the data.
        return line

    with tempfile.TemporaryDirectory() as tmpdir, ffopen(
        path.join(tmpdir, "output.mp4"), "wv", 1e3 / interval
    ) as f:
        for n in range(save_count):
            animate(n)  # update figure
            f.write(fig)  # write new frame


if __name__ == "__main__":
    test_video()
