import numpy as np
from scipy.signal import convolve2d
import cv2

def make_diamond_mask(power):
    side = 2**power + 1
    mask = np.mod(np.reshape(range(side*side), (side, side))+1, 2).astype('bool')
    return mask

def make_map(size):
    # Generate a random heightmap using the diamond-square algorithm
    rng = np.random.default_rng()

    square_kernel = np.zeros((2, 2)) + 0.25
    diamond_kernel = np.zeros((3, 3))
    diamond_kernel[[1, 0, 2, 1], [0, 1, 1, 2]] = 0.25
    print('square_kernel:')
    print(square_kernel)
    print('diamond_kernel:')
    print(diamond_kernel)

    max_side = max(size)
    power = int(np.ceil(np.log2(max_side-1)))
    side = int(2**power + 1)
    map = np.zeros((side, side))
    # Initialize map corners
    map[::2**power, ::2**power] = rng.random((2,2))
    # map = np.reshape(range(side*side), (side, side))
    for pow in range(power, 0, -1):
        print('pow=', pow)
        fullstep = 2**pow
        halfstep = 2**(pow-1)
        subpow = power-pow
        fullsize = 2**subpow
        halfsize = 2**(subpow+1)+1
        # Square step
        corners = map[::fullstep, ::fullstep]
        random_values = rng.random((fullsize, fullsize))
        map[halfstep::fullstep, halfstep::fullstep] = convolve2d(corners, square_kernel, mode='valid') + random_values
        print((map*100).astype('int'))
        # Diamond step
        random_values = rng.random((halfsize, halfsize))
        averages = convolve2d(map[::halfstep, ::halfstep], diamond_kernel, mode='same', boundary='wrap') + random_values
        mask = make_diamond_mask(subpow+1)
        averages[mask] = 0
        map[::halfstep, ::halfstep] += averages
        print((map*100).astype('int'))
        print()
    # mapMax = map.max()
    # mapMin = map.min()
    # mapRange = mapMax-mapMin
    # map = (map - mapMin) / mapRange
    return map


# print(make_diamond_mask(3))

map = make_map((8, 8))
print(map)

cv2.imshow('map', np.kron(map,np.ones((8, 8))))
cv2.waitKey(0)
cv2.destroyAllWindows()
