from PIL import Image

class Steganography(object):

  @staticmethod
  def __int_to_bin(rgb):
    """Convert an integer tuple to a binary (string) tuple.
    
    :param rgb: An integer tuple (e.g. (220, 110, 96))
    :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
    """
    r, g, b = rgb
    return ('{0:08b}'.format(r),
            '{0:08b}'.format(g),
            '{0:08b}'.format(b))

  @staticmethod
  def __bin_to_int(rgb):
    """Convert a binary (string) tuple to an integer tuple.

    :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
    :return: Return an int tuple (e.g. (220, 110, 96))
    """
    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))

  @staticmethod
  def __merge_rgb(rgb1, rgb2):
    """Merge two RGB tuples.
    
    :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
    :param rgb2: Another string tuple (e.g. ("00101010", "11101011", "00010110"))
    :return: An integer tuple with the two RGB values merged.
    """
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    rgb = (r1[:4] + r2[:4],
          g1[:4] + g2[:4],
          b1[:4] + b2[:4])
    return rgb

  @staticmethod
  def encode(show_image, hide_image):
    """Merge two images. The second one will be merged into the first one.
    
    :param show_image: Image to be shown
    :param hide_image: Image to be hidden
    :return: A new encoded (merged) image.
    """
        
    show_image_width, show_image_height = show_image.size
    hide_image_width, hide_image_height = hide_image.size

    # Check the images dimensions
    if hide_image_width > show_image_width or hide_image_height > show_image_height:
      raise ValueError('Image Hide should not be larger than Image Show!')

    # Get the pixel map of the two images
    show_image_pixel = show_image.load()
    hide_image_pixel = hide_image.load()

    # Create a new image that will be outputted
    new_image = Image.new(show_image.mode, show_image.size)
    new_image_pixel = new_image.load()

    for i in range(show_image_width):
      for j in range(show_image_height):
        show_rgb = Steganography.__int_to_bin(show_image_pixel[i, j])

        # Use a black pixel as default
        hide_rgb = Steganography.__int_to_bin((0, 0, 0))

        # Check if the pixel map position is valid for the hide image
        if i < hide_image_width and j < hide_image_height:
          hide_rgb = Steganography.__int_to_bin(hide_image_pixel[i , j])

        # Merge the two pixels and convert it to a integer tuple
        rgb = Steganography.__merge_rgb(show_rgb, hide_rgb)

        new_image_pixel[i, j] = Steganography.__bin_to_int(rgb)

    return new_image

  @staticmethod
  def decode(image):
    """Decode an image.
    
    :param image: The input image.
    :return: The decoded (unmerged / extracted) image.
    """
    
    # Load the pixel map
    image_pixel = image.load()

    # Create the new image and load the pixel map
    new_image = Image.new(image.mode, image.size)
    new_image_pixel = new_image.load()

    # Tuple used to store the image original size
    original_size = image.size

    width, height = image.size
    for i in range(width):
      for j in range(height):
        # Get the RGB (as a string tuple) from the current pixel
        r, g, b = Steganography.__int_to_bin(image_pixel[i, j])

        # Extract the last 4 bits (corresponding to the hidden image)
        # Concatenate 4 zero bits because we are working with 8 bit
        rgb = (r[4:] + '0000',
              g[4:] + '0000',
              b[4:] + '0000')

        # Convert it to an integer tuple
        new_image_pixel[i, j] = Steganography.__bin_to_int(rgb)

        # If this is a 'valid' position, store it
        # as the last valid position
        if new_image_pixel[i, j] != (0, 0, 0):
          original_size = (i + 1, j + 1)

    # Crop the image based on the 'valid' pixels
    new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

    return new_image


if '__main__':
  show_image = Image.open('./samples/show.tiff')
  hide_image = Image.open('./samples/hide.tiff')

  encoded_image = Steganography.encode(show_image, hide_image)
  encoded_image.save('outputs/encoded_image.tiff')
  
  # encoded_image = Image.open('outputs/encoded_image.tiff')
  # decoded_image = Steganography.decode(encoded_image)
  # decoded_image.save('outputs/decoded_image.tiff')
        


