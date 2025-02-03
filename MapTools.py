import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter
import cv2

def make_diamond_mask(power):
    side = 2**power + 1
    mask = np.mod(np.reshape(range(side*side), (side, side))+1, 2).astype('bool')
    return mask

def center_crop(array, new_shape):
    # Crop a 2D array to the new shape symmetrically
    start = (np.array(array.shape) - new_shape) // 2
    end = start + new_shape
    return array[start[0]:end[0], start[1]:end[1]]

def riverify(map, min_value=0, length=20):
    idx = np.array(range(map.shape[0]*map.shape[1])).flatten()
    probs = map.flatten()
    probs -= probs.min()
    probs = probs / probs.sum()
    start_idx = np.random.choice(idx, p=probs)
    x, y = np.unravel_index(start_idx, map.shape)

    neighbor_offsets = [
        (0,  -1),
        (-1, 0),
        (+1, 0),
        (0,  +1)
    ]

    river_coords = [(x, y)]
    for k in range(length-1):
        neighbor_heights = []
        for offset in neighbor_offsets:
            nx = x + offset[0]
            ny = y + offset[1]
            try:
                neighbor_heights.append((nx, ny, map[nx, ny]))
            except IndexError:
                pass
        x, y, _ = min(neighbor_heights, key=lambda n:n[2])
        river_coords.append((x, y))

    for x, y in river_coords:
        map[x, y] = min_value
    return map





def islandify(map, sea_level, sea_width, min_value=None, max_value=None):
    """Alter an existing map to add a sea border around the perimeter

    Args:
        map (2D numpy array): The map to alter.
        sea_level (numerical): The map height level to consider to be "sea
            level".
        sea_width (int): Average desired width of the sea border.
        min_value (float): Min value to clamp output map to, or None for no
            clamping
        max_value (float): Max value to clamp output map to, or None for no
            clamping

    Returns:
        type: 2D numpy array, although the map is also altered in place.

    """
    # Store original data type so it can be restored later
    original_dtype = map.dtype
    # Get min and max height of map
    min_height = map.min()
    max_height = map.max()
    # Initialize a map of the sea alteration
    sea_map = np.zeros(map.shape, dtype='float')
    # Set up three bands of depth
    width1 = int(0.5*sea_width)
    width2 = int(1.0*sea_width)
    width3 = int(1.5*sea_width)
    height1 = sea_level - max_height*2
    height2 = sea_level - max_height
    height3 = 0
    # Set outer band to the deepest height
    sea_map[:] = height1
    # Set second band to the second height
    sea_map[width1:-width1, width1:-width1] = height2
    # Set third band to the third height
    sea_map[width2:-width2, width2:-width2] = height3
    # Smooth bands so they blend gradually
    sea_map = gaussian_filter(sea_map, (width1, width1), mode='wrap')
    # Add sea map to original map
    map = map.astype('float') + sea_map

    if min_value is not None:
        # Clamp map to the original minimum
        map[map < min_value] = min_value
    if max_value is not None:
        # Clamp map to the original maximum
        map[map > max_value] = max_value


    # Convert map back to original data type
    map = map.astype(original_dtype)
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

    # Create the two averaging kernels
    square_kernel = np.zeros((2, 2)) + 0.25
    diamond_kernel = np.zeros((3, 3))
    diamond_kernel[[1, 0, 2, 1], [0, 1, 1, 2]] = 0.25

    # Calculate some relevant values
    max_side = max(size)
    power = int(np.ceil(np.log2(max_side-1)))
    side = int(2**power + 1)
    # Initialize the map
    map = np.zeros((side, side), dtype='float')
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
    # Blur to remove artifacts
    map = gaussian_filter(map, (blur_size, blur_size), mode='wrap')
    # Center crop to get correct output size
    map = center_crop(map, size)
    # Rescale values to desired range
    map_max = map.max()
    map_min = map.min()
    mapRange = map_max-map_min
    new_range = max_value-min_value
    map = (map - map_min) * (new_range / mapRange) + min_value
    # Convert to integer, if desired
    if integer:
        return map.astype('int')
    else:
        return map

if __name__ == '__main__':
    # Demo

    # Create a map
    map = make_map((800, 600), blur_size=12, max_value=255, min_value=50, integer=True).astype('uint8')
    # Assign some nice terrain-ish colors
    map3 = np.zeros(map.shape+(3,), dtype='uint8')
    map3[:, :, 0] = (map < 150) * map
    map3[:, :, 1] = (map >= 150) * map
    map3[:, :, 0] += (map >= 220) * map
    map3[:, :, 2] += (map >= 220) * map
    # Show the map
    cv2.imshow('map', map3)
    cv2.waitKey(0)
    # Island-ify the map
    map = islandify(map, 150, 50, max_value=255, min_value=50)
    # Assign nice colors again
    map3 = np.zeros(map.shape+(3,), dtype='uint8')
    map3[:, :, 0] = (map < 150) * map
    map3[:, :, 1] = (map >= 150) * map
    map3[:, :, 0] += (map >= 220) * map
    map3[:, :, 2] += (map >= 220) * map
    # Show the island-ified map
    cv2.imshow('map', map3)
    cv2.waitKey(0)

    # River-ify the map
    map = riverify(map, length=100)
    # Assign nice colors again
    map3 = np.zeros(map.shape+(3,), dtype='uint8')
    map3[:, :, 0] = (map < 150) * map
    map3[:, :, 1] = (map >= 150) * map
    map3[:, :, 0] += (map >= 220) * map
    map3[:, :, 2] += (map >= 220) * map
        # Show the island-ified map
    cv2.imshow('map', map3)
    cv2.waitKey(0)

    # Quit
    cv2.destroyAllWindows()
