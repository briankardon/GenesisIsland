import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter
import cv2

def make_diamond_mask(power):
    side = 2**power + 1
    mask = np.mod(np.reshape(range(side*side), (side, side))+1, 2).astype('bool')
    return mask

def make_map(size, blur_size=3, min_value=0, max_value=1, integer=False):
    # Generate a random heightmap using the diamond-square algorithm
    rng = np.random.default_rng()

    square_kernel = np.zeros((2, 2)) + 0.25
    diamond_kernel = np.zeros((3, 3))
    diamond_kernel[[1, 0, 2, 1], [0, 1, 1, 2]] = 0.25

    max_side = max(size)
    power = int(np.ceil(np.log2(max_side-1)))
    side = int(2**power + 1)
    map = np.zeros((side, side))
    # Initialize map corners
    map[::2**power, ::2**power] = rng.random((2,2))
    # map = np.reshape(range(side*side), (side, side))
    for pow in range(power, 0, -1):
        fullstep = 2**pow
        halfstep = 2**(pow-1)
        subpow = power-pow
        fullsize = 2**subpow
        halfsize = 2**(subpow+1)+1
        # Square step
        corners = map[::fullstep, ::fullstep]
        random_values = rng.random((fullsize, fullsize))
        map[halfstep::fullstep, halfstep::fullstep] = convolve2d(corners, square_kernel, mode='valid') + random_values
        # Diamond step
        random_values = rng.random((halfsize, halfsize))
        averages = convolve2d(map[::halfstep, ::halfstep], diamond_kernel, mode='same', boundary='wrap') + random_values
        mask = make_diamond_mask(subpow+1)
        averages[mask] = 0
        map[::halfstep, ::halfstep] += averages
    map_max = map.max()
    map_min = map.min()
    mapRange = map_max-map_min
    new_range = max_value-min_value
    map = gaussian_filter(map, (blur_size, blur_size), mode='wrap')
    map = (map - map_min) * (new_range / mapRange) + min_value
    if integer:
        return map.astype('uint8')
    else:
        return map

if __name__ == '__main__':
    map = make_map((1000, 1000), blur_size=12, max_value=255, integer=True)
    map3 = np.zeros(map.shape+(3,), dtype='uint8')
    map3[:, :, 0] = (map < 150) * map
    map3[:, :, 1] = (map >= 150) * map
    cv2.imshow('map', map3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
