from PIL import Image

# predefine image size, circle size, circle color, ..., etc
ROWS, COLS = 300, 300
RADIUS = 100
COLOR = (0, 255, 0)
BLURRED = (0, 128, 0)
BLACK = (0, 0, 0)


def makeCircle(pixels):
    def circlePoint(x, y):
        # shift the circle
        x += cx
        y += cy

        # fill the pixel at (x, y) and seven others (symmetrical points)
        pixels[x, y] = COLOR
        pixels[y, x] = COLOR
        pixels[y, -x] = COLOR
        pixels[x, -y] = COLOR
        pixels[-x, -y] = COLOR
        pixels[-y, -x] = COLOR
        pixels[-y, x] = COLOR
        pixels[-x, y] = COLOR

    cx, cy = COLS // 2, ROWS // 2
    x, y = 0, RADIUS
    d = 1 - RADIUS

    # fill the pixel at (x, y) and its symmetrical points of (x, y)
    circlePoint(x, y)

    while y > x:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        circlePoint(x, y)


def fillCircle(pixels):
    def fillLine(r):
        # find out the min and max x coordinate on this line then fill it
        minX, maxX = ROWS - 1, 0
        for c in range(COLS):
            if pixels[r, c] != BLACK:
                minX = min(minX, c)
                maxX = max(maxX, c)

        for c in range(minX, maxX + 1):
            pixels[r, c] = COLOR

    for row in range(ROWS):
        fillLine(row)


def antiAliasing(pixels):
    def circlePoint(x, y):
        # shift the circle
        x += cx
        y += cy

        # fill the pixel at (x, y) and seven others (symmetrical points)
        pixels[x, y] = BLURRED
        pixels[y, x] = BLURRED
        pixels[y, -x] = BLURRED
        pixels[x, -y] = BLURRED
        pixels[-x, -y] = BLURRED
        pixels[-y, -x] = BLURRED
        pixels[-y, x] = BLURRED
        pixels[-x, y] = BLURRED

    cx, cy = COLS // 2, ROWS // 2
    x, y = 0, RADIUS
    d = 1 - RADIUS

    while y > x:
        x += 1
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            circlePoint(x, y)
            y -= 1


# Q1
image = Image.new('RGB', (ROWS, COLS))
makeCircle(image.load())
image.save('Q1.png')

# Q2
fillCircle(image.load())
image.save('Q2.png')

# Q3
antiAliasing(image.load())
image.save('Q3.png')
