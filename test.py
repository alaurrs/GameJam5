# import pygame module in this program
import pygame

# activate the pygame library.
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()
# create the display surface object
# of specific dimension..e(500, 500).
win_ing = pygame.display.set_mode((500, 500))
# set the pygame window name
pygame.display.set_caption("Jump Game")
# object current co-ordinates
x_new = 200
y_new = 200
# dimensions of the object
wdth = 30
hght = 40
# Indicates if the player is jumping or not.
is_jump = False
# mass m and force (v) up
v_new = 5
m_new = 1
# pygame is now active.
run_new = True
# endless loop
while run_new:
# Completely cover the thing
# with black paint.
win_ing.fill((0, 0, 0))
# sketching a rectangle-shaped object on the screen
pygame.draw.rect(win_ing, (255, 0, 0), (x_new, y_new, wdth, hght))

# cycle through the Event object list
# that the pygame.event.get() method returned
for vnt in pygame.event.get():

    # If the event object type is QUIT
    # both the pygame
    # and the application will be terminated..
    if vnt.type == pygame.QUIT:
        # It will cause the while loop to end.
        run_new = False
# keystrokes are saved
kys = pygame.key.get_pressed()

if is_jump == False:
    # if space bar is pressed
    if kys[pygame.K_SPACE]:
        # make isjump equal to True
        is_jump = True

if is_jump:
    # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
    F_orce = (1 / 2) * mass * (vel ** 2)

    # change in the y co-ordinate
    y -= F_orce

    # decreasing velocity while going up and become negative while coming down
    vel = vel - 1

    # object reached its maximum height
    if vel < 0:
        # negative sign is added to counter negative velocity
        mass = -1
    # objected reaches its original state
    if vel == -6:
        # making isjump equal to false
        is_jump = False

        # setting original values to v and m
        vel = 5
        mass = 1

# creates time delay of 10ms
pygame.time.delay(10)
# it refreshes the window
pygame.display.update()
# closes the pygame window
pygame.quit()