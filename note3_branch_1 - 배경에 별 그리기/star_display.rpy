init -1 python:
    import random, pygame

    TOTAL_STARS = 500
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    class Star(object):
        color = (0,0,0)
        position = [0,0]
        speed = 1

        def __init__(self):
            self.generateStartPosition(xrandom=True)

        def generateStartPosition(self, xrandom=False):
            # start at right of screen, scroll left
            if xrandom:
                xpos = random.randint(1, SCREEN_WIDTH - 1)
            else:
                xpos = SCREEN_WIDTH - 1
            self.position = [xpos, random.randint(1, SCREEN_HEIGHT - 1)]
            brightness = random.randint(1, 255)
            self.color = (brightness, brightness, brightness)
            self.speed = float(brightness / 400.0)

        def update(self):
            #self.position[0] -= self.speed
            if(self.position[0] < 0):
                # generate new star
                self.generateStartPosition()

        def draw(self, canvas):
            xpos = int(self.position[0])
            ypos = int(self.position[1])
            canvas.rect(self.color, pygame.Rect(xpos, ypos, 0, 0))

    # Displayable 설계하기
    class StarDisplay(renpy.Displayable):
        def __init__(self, *args, **kwargs):
            super(StarDisplay, self).__init__(*args, **kwargs)
            self.stars = [Star() for x in range(TOTAL_STARS)]

        def render(self, width, height, st, at):
            """Called when renpy needs to get the image to display"""

            screen = renpy.Render(SCREEN_WIDTH, SCREEN_HEIGHT)
            canvas = screen.canvas()
            canvas.rect((0,0,0), pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            for star in self.stars:
                star.draw(canvas)
                star.update()
            # just drawing once if not good enough. Tell Renpy to call this function again as soon as possible.
            renpy.redraw(self, 0)
            return screen

        def visit(self):
            """This function needs to return all the child displayables.
            We have none, so just return the empty list."""
            return []