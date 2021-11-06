import pygame, sys, math
from pygame.draw import rect
from pygame.constants import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, RESIZABLE

Vadd = lambda a,b : (a[0]+b[0],a[1]+b[1])   #add/subtract/multiply/divide 2 tuples like numpy arrays
Vsub = lambda a,b : (a[0]-b[0],a[1]-b[1])
Vmul = lambda a,b : (a[0]*b[0],a[1]*b[1])
Vdiv = lambda a,b : (a[0]/b[0],a[1]/b[1])

def get_pixel_iters(constant, maxiter = 1000):  #in: complex, out: num of iterations
    lastpos = complex(0,0)              #start value
    counter = 0
    while counter < maxiter:
        nextpos = lastpos**2+constant   #calculating
        if abs(nextpos) > 3:            #if function explodes
            return counter
        counter += 1
        lastpos = nextpos
    return 0    #function bounces arround to much

def hanlde_input(event, mpressed, viewoffset, scale, res):
    if event.type == pygame.QUIT:   #pressing close button of the window
        pygame.quit()
        sys.exit()
    
    elif event.type == KEYDOWN:
        if event.key == K_ESCAPE:   #exit windows using 'Esc' button
            pygame.quit()
            sys.exit()

    elif event.type == MOUSEBUTTONDOWN: #when you press a button or scroll
        res = 50    #resets the resolution to 50 screen pixels per pixel
        mpos = pygame.mouse.get_pos()
        if event.button == 1: #left mousebutton
            mpressed = True
        elif event.button == 4: #zoom in
            viewoffset = Vmul(viewoffset,(2,2)) #idk how this works but it does
            viewoffset = Vsub(viewoffset,mpos)
            scale *= 2
        if event.button == 5: #zoom out
            viewoffset = Vadd(viewoffset,mpos)
            viewoffset = Vdiv(viewoffset,(2,2))
            scale /= 2
        
    elif event.type == MOUSEBUTTONUP: #when you 'unpress' a button
        if event.button == 1:
            mpressed = False

    elif event.type == MOUSEMOTION:   #when you move the mouse
        if mpressed:
            res = 20   #reset the resolution for the new frame
            viewoffset = Vadd(viewoffset,event.rel) #recalculate the window offset

    return (mpressed,list(viewoffset),scale, res)

def run():
    res = 10    #how big each pixel is (in actual pixel)
    scale = 200 #the zoom level, 1 unit is {scale} pixel
    winsize = (300,300)
    viewoffset = [winsize[0]/2,winsize[1]/2]
    mpressed = False

    pygame.init()           #pygame startup
    pygame.display.init()
    win = pygame.display.set_mode(winsize,RESIZABLE)
    clock = pygame.time.Clock()

    while True:
        for y in range(0,winsize[1],res):       #for every virtual pixel (resolution)
            for x in range(0,winsize[0],res):
                px = (x-viewoffset[0])/scale    #get complex value of pixel
                py = (y-viewoffset[1])/scale
                pixelpos = complex(px,py)       
                maxiter = math.log2(scale)**2     #"dynamic iterations" kinda works
                color = get_pixel_iters(pixelpos,maxiter+100)*2%255 #amount of iterations % 255 in greyscale
                rect(
                    surface=win,
                    color=[color]*3,
                    rect=pygame.Rect(x,y,res,res)
                )

            for event in pygame.event.get():    #yes i know this looks bad, but it works
                mpressed,viewoffset,scale,res = hanlde_input(event,mpressed,viewoffset,scale,res)
                winsize = win.get_size()
            pygame.display.flip()

        clock.tick(30)
        res -= res//2   #after every completed frame double the resolution
        if res < 1: res = 1

if __name__ == '__main__':
    run()