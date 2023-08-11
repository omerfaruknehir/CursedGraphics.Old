class Rect:
    def __init__(self, height, width, y, x):
        self.height = height
        self.width = width
        self.y = y
        self.x = x
    
    def __str__(self):
        return "Rect"+str(((self.y, self.x), (self.width, self.height)))
    
    def contains(self, y, x):
        return (y >= self.y and y <= self.y + self.height -1 ) and (x >= self.x and x <= self.x + self.width - 1)