class CoordinateSystem:
    def __init__(self,width,height,scale=50):
        self.width=width
        self.height=height
        self.scale=scale
        self.origin_x=width/2
        self.origin_y=height/2

    def to_screen(self,x,y):
        screen_x=self.origin_x +x*self.scale
        screen_y=self.origin_y -y*self.scale
        return screen_x, screen_y

    def from_screen(self,screen_x,screen_y):
        x=(screen_x-self.origin_x)/self.scale
        y=(self.origin_y-screen_y)/self.scale
        return x,y