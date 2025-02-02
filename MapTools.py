import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter
import cv2

def make_diamond_mask(power):
    side = 2**power + 1
    mask = np.mod(np.reshape(range(side*side), (side, side))+1, 2).astype('bool')
    return mask

def center_crop(array, new_shape):
    start = (np.array(array.shape) - new_shape) // 2
    end = start + new_shape
    return array[start[0]:end[0], start[1]:end[1]]

def islandify(map, sea_level, sea_width):
    """Alter an existing map to add a sea border around the perimeter

    Args:
        map (2D numpy array): The map to alter.
        sea_level (numerical): The map height level to consider to be "sea
            level".
        sea_width (int): Average desired width of the sea border.

    Returns:
        type: 2D numpy array, although the map is also altered in place.

    """
    original_dtype = map.dtype
    average_height = map.mean()
    max_height = map.max() + 1
    sea_map = np.zeros(map.shape, dtype='float')
    width1 = int(0.5*sea_width)
    width2 = int(1.0*sea_width)
    width3 = int(1.5*sea_width)
    height1 = sea_level - max_height
    height2 = min([2*(sea_level - average_height), height1])
    height3 = 0
    sea_map[:] = height1
    sea_map[width1:-width1, width1:-width1] = height2
    sea_map[width2:-width2, width2:-width2] = height3
    sea_map = gaussian_filter(sea_map, (width1, width1), mode='wrap')

    map = (map.astype('float') + sea_map).astype(original_dtype)
    return map


def make_map(size, blur_size=12, min_value=0, max_value=1, integer=False):
    """Create a randomized terrain height map as a numpy array.

    Args:
        size (2-tuple of ints): A 2-tuple specifying the (width, height) of the
            desired map.
        blur_size (float): How much blurring to apply after map generation, to
            remove diamond artifacts. Defaults to 12.
        min_value (float): Minimum map height. Defaults to 0.
        max_value (float): Maximum map height. Defaults to 1.
        integer (boolean): Convert map to integer values after generation.
            Defaults to False.

    Returns:
        type: 2D numpy array of either float or uint8 values

    """
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
    map = center_crop(map, size)
    if integer:
        return map.astype('uint8')
    else:
        return map

if __name__ == '__main__':
    map = make_map((800, 600), blur_size=12, max_value=255, integer=True)
    map3 = np.zeros(map.shape+(3,), dtype='uint8')
    map3[:, :, 0] = (map < 150) * map
    map3[:, :, 1] = (map >= 150) * map
    cv2.imshow('map', map3)
    cv2.waitKey(0)
    map = islandify(map, 150, 100)
    map3 = np.zeros(map.shape+(3,), dtype='uint8')
    map3[:, :, 0] = (map < 150) * map
    map3[:, :, 1] = (map >= 150) * map
    cv2.imshow('map', map3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
