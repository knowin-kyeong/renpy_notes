define persistent.snake_high_score = 0

init python:
    import random

    class SnakeDisplayable(renpy.Displayable):
        def __init__(self):
            renpy.Displayable.__init__(self)

            # Set game values
            self.SNAKE_SIZE = 60
            self.score = 0

            # Some displayables we use
            self.snake = Solid("#009933", xsize=self.SNAKE_SIZE, ysize=self.SNAKE_SIZE)
            self.snake_body = Solid("#004d1a", xsize=self.SNAKE_SIZE, ysize=self.SNAKE_SIZE)
            self.apple = Solid("#cc0000", xsize=self.SNAKE_SIZE, ysize=self.SNAKE_SIZE)

            # The positions of the displayables
            self.shx = 1920/2
            self.shy = 1080/2
            self.shdx = 0
            self.shdy = 0
            self.shxmin = 0
            self.shxmax = 1920
            self.shymin = 0
            self.shymax = 1080
            self.key_pressed = None

            self.sbxy = []

            self.ax = random.randint(0, 1920 - self.SNAKE_SIZE)
            self.ay = random.randint(0, 1080 - self.SNAKE_SIZE)

            # The time of the past render-frame
            self.oldst = None
            self.lose = False
            return

        # Draws the screen
        def render(self, width, height, st, at):

            # The Render object we'll be drawing into
            r = renpy.Render(width, height)

            # Figure out the time elapsed since the previous frame.
            if self.oldst is None:
                self.oldst = st
            dtime = st - self.oldst
            self.oldst = st

            # This draws the snake
            def snake(shx, shy):

                # Render the snake image
                snake = renpy.render(self.snake, width, height, st, at)
                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                r.blit(snake, (int(shx), int(shy)))
            
            # This draws the snakebody
            def snake_body(sbxy):

                # Render the snake body image
                snake_body = renpy.render(self.snake_body, width, height, st, at)
                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                for body in sbxy:
                    r.blit(snake_body, (int(body[0]), int(body[1])))

            # This draws the apple
            def apple(ax, ay):

                # Render the apple image
                apple = renpy.render(self.apple, width, height, st, at)

                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                r.blit(apple, (int(ax), int(ay)))

            snake(self.shx, self.shy)
            snake_body(self.sbxy)
            apple(self.ax, self.ay)

            # Recalculate pos.of snake
            if self.key_pressed == "up":
                self.shdx = 0
                self.shdy = -1 * self.SNAKE_SIZE
            elif self.key_pressed == "down":
                self.shdx = 0
                self.shdy = self.SNAKE_SIZE
            elif self.key_pressed == "left":
                self.shdx = -1 * self.SNAKE_SIZE
                self.shdy = 0
            elif self.key_pressed == "right":
                self.shdx = self.SNAKE_SIZE
                self.shdy = 0

            # Add a segment onto the snake's body
            self.sbxy.insert(0, (self.shx, self.shy))
            self.sbxy.pop()

            # Update the x, y position of the snake's head
            self.shx += self.shdx
            self.shy += self.shdy

            if self.shx < self.shxmin or self.shx + self.SNAKE_SIZE > self.shxmax :
                self.lose = True
                renpy.timeout(0)

            if self.shy < self.shymin or self.shy + self.SNAKE_SIZE > self.shymax:
                self.lose = True
                renpy.timeout(0)
            
            if (self.shx, self.shy) in self.sbxy:
                self.lose = True
                renpy.timeout(0)

            # Check for collisions
            def is_colliding():
                return (
                    self.shx <= self.ax + self.SNAKE_SIZE and
                    self.shx + self.SNAKE_SIZE >= self.ax and
                    self.shy <= self.ay + self.SNAKE_SIZE and
                    self.shy + self.SNAKE_SIZE >= self.ay
                )
            
            if is_colliding():
                self.score += 1
                #renpy.sound.play("audio/minigames/s_pick_up_sound.wav")
                self.ax = random.randint(0, 1920 - self.SNAKE_SIZE)
                self.ay = random.randint(0, 1080 - self.SNAKE_SIZE)
                self.sbxy.append((self.shx, self.shy))

            # Ask that we be re-rendered so we can show the next frame
            renpy.redraw(self, 0.04)

            # Return the Render object
            return r

        # Handles events
        def event(self, ev, x, y, st):
            
            import pygame

            if renpy.map_event(ev, "focus_up") and (self.key_pressed != "down" or self.sbxy == []):
                self.key_pressed = "up"
            elif renpy.map_event(ev, "focus_down") and (self.key_pressed != "up" or self.sbxy == []):
                self.key_pressed = "down"
            elif renpy.map_event(ev, "focus_left") and (self.key_pressed != "right" or self.sbxy == []):
                self.key_pressed = "left"
            elif renpy.map_event(ev, "focus_right") and (self.key_pressed != "left" or self.sbxy == []):
                self.key_pressed = "right"
            elif renpy.map_event(ev, "pad_lefty_zero") or renpy.map_event(ev, "pad_righty_zero") or ev.type == pygame.KEYUP:
                self.key_pressed = None

            # Ensure the screen updates
            renpy.restart_interaction()

            # If the player loses, return it
            if self.lose:
                return self.lose
            else:
                raise renpy.IgnoreEvent()

    def display_s_score(st, at):
        return Text(_("Score: ") + "%d" % snake.score, size=90, color="#cc0000", outlines=[ (4, "#800000", 0, 0) ]), None #font="gui/font/Gallagher.ttf"), .1

default snake = SnakeDisplayable()

screen snake():

    #add "minigames/s_background.jpg"

    text _("Snake"):
        xpos 240
        xanchor 0.5
        ypos 25
        size 90
        color "#cc0000"
        outlines [ (4, "#800000", 0, 0) ]
        #font "gui/font/Gallagher.ttf"

    add DynamicDisplayable(display_s_score) xpos (1920 - 240) xanchor 0.5 ypos 25

    add snake

label play_snake:

    window hide  # Hide the window and quick menu while in Feed the Dragon
    $ quick_menu = False
    hide screen buttons_ui

    #play music s_background_music

    $ snake.lose = False
    $ snake.key_pressed = None
    $ snake.score = 0
    $ snake.shx = 1920/2
    $ snake.shy = 1080/2
    $ snake.shdx = 0
    $ snake.shdy = 0
    $ snake.sbxy = []

    call screen snake

    #play music amusement

    #show screen buttons_ui(dt)
    $ quick_menu = True
    window auto

label snake_done:

    if persistent.snake_high_score >= snake.score:
        pass
    else:
        $ persistent.snake_high_score = snake.score

    e "Score: [snake.score]\n\nHigh Score: [persistent.snake_high_score]"

    menu:
        e "다시 한 번 시도하시겠습니까?"

        "네":
            jump play_snake

        "아니요":
            return
