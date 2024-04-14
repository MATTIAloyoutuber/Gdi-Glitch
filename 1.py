from win32api import *
from win32con import *
from win32gui import *
import numpy as np
import numba

# Get screen dimensions
w, h = GetSystemMetrics(SM_CXSCREEN), GetSystemMetrics(SM_CYSCREEN)

# Get device context
hdc = GetDC(0)

# Bitblt Effect
for i in range(100):
    BitBlt(hdc, 1, 1, w, h, hdc, 0, 0, SRCCOPY)

# Stretchblt Effect
for i in range(100):
    StretchBlt(hdc, 180, 180, w - 100, h - 100, hdc, 0, 0, w, h, SRCCOPY)

# Patblt Effect
for i in range(100):
    brush = CreateSolidBrush(RGB(randrange(280), randrange(280), randrange(280)))
    SelectObject(hdc, brush)
    PatBlt(hdc, randrange(w), randrange(h), randrange(w), randrange(h), PATINVERT)

# Plgblt Effect
points = ((100, 100), (w, -99), (60, h))
for i in range(100):
    PlgBlt(hdc, points, hdc, 0, 0, w, h, None, 0, 0)

# Pie Effect
for i in range(200000):
    brush = CreateSolidBrush(RGB(randrange(280), randrange(280), randrange(280)))
    SelectObject(hdc, brush)
    Pie(hdc, randrange(1, w), randrange(1, h), randrange(1, w), randrange(1, h),
        randrange(1, w), randrange(1, h), randrange(1, w), randrange(1, h))

# Shaders Effect (customize as needed)
@numba.njit(parallel=True)
def shader(arr, w, h, i):
    for x in numba.prange(w):
        for y in range(h):
            arr[x, y, 0] = x ^ y + i * 100
    return arr

# Apply shader
dcMem = CreateCompatibleDC(hdc)
bmp = CreateCompatibleBitmap(hdc, w, h)
SelectObject(dcMem, bmp)

for i in range(100):
    BitBlt(dcMem, 0, 0, w, h, hdc, 0, 0, SRCINVERT)
    buf = GetBitmapBits(bmp, True)
    arr_f = np.frombuffer(buf, dtype=np.uint8)
    arr = np.array(arr_f)
    bs = arr.shape
    arr.shape = (h, w, 4)
    shader(arr, h, w, i)
    arr.shape = bs
    SetBitmapBits(bmp, arr.tobytes())
    BitBlt(hdc, 0, 0, w, h, dcMem, 0, 0, SRCCOPY)
