import cv2

def resize_if_small(image_to_resize, size=100):
    height, width = image_to_resize.shape[:2]

    dim = (width, height)
    if height < size:
        dim = (int(size*width/height), size)

    if width < height:
        if width < size:
            dim = (size, int(size*height/width))
    if dim == (width, height):
        return image_to_resize
    resized = cv2.resize(image_to_resize, dim, interpolation=cv2.INTER_AREA)
    return resized

def main():
    print('test')

if __name__ == "__main__":
    main()