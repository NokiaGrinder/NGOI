import time as t
from raylib import *
from pyray import *
from os.path import join

class Cell:
    def __init__(self, pos, cellcount, perm, wall, mover, direction, texture, color):
        self.pos = pos
        self.cellcount = cellcount
        self.perm = perm
        self.wall = wall
        self.mover = mover
        self.direction = direction
        self.texture = texture
        self.color = color
        
#normal
normalimage = load_image(join("NGOI", "Textures", "normalcell.png"))
normalimageicon = load_image(join("NGOI", "Textures", "normalcellicon.png"))
#permanent
permanentimage = load_image(join("NGOI", "Textures", "basepermanentcell.png"))
permanentimageicon = load_image(join("NGOI", "Textures", "basepermanentcellicon.png"))
#wall
wallimage = load_image(join("NGOI", "Textures", "basewall.png"))
wallimageicon = load_image(join("NGOI", "Textures", "basewallicon.png"))
#mover
moverimage = load_image(join("NGOI", "Textures", "basemovercell.png"))
moverimageicon = load_image(join("NGOI", "Textures", "basemovercellicon.png"))
        
spg = 1
#seconds per generation

currentg = 0
        
BuildMode = True

checkrement = 50
cellsize = [50, 50]

direction = [-1, 0]
directiondisplay = "left"

allcells = set([])

undo = []

#camera stuff
camerapos = [700, 425] #half of init_window size
camera = Camera2D()
camera.zoom = 1.1
camera.target = camerapos

normalchosen = True
permanentchosen = False
wallchosen = False
moverchosen = False

cellcolor = WHITE
displaycellcolor = "White"



init_window(1400, 850, "NokiaGrinder's Game Of Imagination")

#OK DO NOT MOVE INIT_WINDOW LOWER THAN THE FUNCTIONS FOR SOME REASON IDKY

def ECheckBorn(ecellpos):
    ADPass = True
    ALPass = True
    ecellcount = 0
    ecolor = []
    for l in allcells:
        if not l.wall:
            if [(ecellpos[0] + checkrement), ecellpos[1]] == l.pos:
                ecellcount += 1     
                ecolor.append(l.color)          
                # + _
            elif [ecellpos[0], (ecellpos[1] + checkrement)] == l.pos:
                ecellcount += 1
                ecolor.append(l.color)
                # _ +
            elif [(ecellpos[0] - checkrement), ecellpos[1]] == l.pos:
                ecellcount += 1
                ecolor.append(l.color)
                # - _
            elif [ecellpos[0], (ecellpos[1] - checkrement)] == l.pos: 
                ecellcount += 1
                ecolor.append(l.color)
                # _ -
            elif [(ecellpos[0] + checkrement), (ecellpos[1] + checkrement)] == l.pos:
                ecellcount += 1   
                ecolor.append(l.color) 
                # + +           
            elif [(ecellpos[0] - checkrement), (ecellpos[1] + checkrement)] == l.pos:
                ecellcount += 1
                ecolor.append(l.color)
                # - +
            elif [(ecellpos[0] + checkrement), (ecellpos[1] - checkrement)] == l.pos:
                ecellcount += 1
                ecolor.append(l.color)
                # + -
            elif [(ecellpos[0] - checkrement), (ecellpos[1] - checkrement)] == l.pos:
                ecellcount += 1
                ecolor.append(l.color)
                # - -
    if ecellcount == 3:
        ecolorR = int((ecolor[0][0] + ecolor[1][0] + ecolor[2][0])/3)
        ecolorG = int((ecolor[0][1] + ecolor[1][1] + ecolor[2][1])/3)
        ecolorB = int((ecolor[0][2] + ecolor[1][2] + ecolor[2][2])/3)
        ecell = Cell(ecellpos, 0, False, False, False, [0, 0], normaltexture, (ecolorR, ecolorG, ecolorB, 255))
        for l in allcells:
            if l.mover and ecellpos == [l.pos[0] + (l.direction[0] * checkrement), l.pos[1] + (l.direction[1] * checkrement)]:
                ALPass = False
            elif ecellpos == l.pos:
                ALPass = False
        for l in addthesecells:
            if ecellpos == l.pos:
                ADPass = False
        if ALPass and ADPass:
            addthesecells.add(ecell)
            
def CellAliveFilter(cell):
    if cell.perm or cell.wall:
        return False
    else:
        return True

def cameramovement():
    if is_key_down(KEY_UP): 
        camerapos[1] -= 50
    if is_key_down(KEY_DOWN):
        camerapos[1] += 50
    if is_key_down(KEY_RIGHT):
        camerapos[0] += 50
    if is_key_down(KEY_LEFT):
        camerapos[0] -= 50
    if is_key_down(KEY_E) and camera.zoom < 1.1:
        camera.zoom += 0.05
    if is_key_down(KEY_Q) and camera.zoom - 0.1 > 0.125: #idky -0.1 is needed but the max zoom out glitches without
        camera.zoom -= 0.05
    if is_key_pressed(KEY_Z):
        camera.zoom = 1.1
    
def gridlines(camerapos):
    offset = 25
    for i in range(int(18/camera.zoom)): #900/50
        #horizontal
        xs = camerapos[0]
        xe = int(1400/camera.zoom) + camerapos[0]
        y = (50*i) + camerapos[1] - offset
        draw_line(xs, y, xe, y, (100, 100, 100, 255)) #between gray and darkgray
    for i in range(int(28/camera.zoom)): #1400/50
        #vertical
        x = (50*i) + camerapos[0]
        ys = camerapos[1]
        ye = int(850/camera.zoom) + camerapos[1]
        draw_line(x, ys, x, ye, (100, 100, 100, 255))

def hotbar(camerapos, normalchosen, permanentchosen, wallchosen, moverchosen):
    draw_rectangle_lines_ex(Rectangle(int(574/camera.zoom) + camerapos[0], int(794.6/camera.zoom) + camerapos[1], int(258/camera.zoom), int(47/camera.zoom)), int(3/camera.zoom), (160, 160, 160, 255)) #same as below
    if normalchosen:
        draw_rectangle_lines_ex(Rectangle(577/camera.zoom + camerapos[0], 797/camera.zoom + camerapos[1], int(40/camera.zoom), int(40/camera.zoom)), int(4/camera.zoom), (150, 150, 150, 255)) #between lightgray and gray
    elif permanentchosen:
        draw_rectangle_lines_ex(Rectangle(646.3/camera.zoom + camerapos[0], 797/camera.zoom + camerapos[1], int(40/camera.zoom), int(40/camera.zoom)), int(4/camera.zoom), (150, 150, 150, 255))
    elif wallchosen:
        draw_rectangle_lines_ex(Rectangle(717.3/camera.zoom + camerapos[0], 797/camera.zoom + camerapos[1], int(40/camera.zoom), int(40/camera.zoom)), int(4/camera.zoom), (150, 150, 150, 255))
    elif moverchosen:
        draw_rectangle_lines_ex(Rectangle(787.3/camera.zoom + camerapos[0], 797/camera.zoom + camerapos[1], int(40/camera.zoom), int(40/camera.zoom)), int(4/camera.zoom), (150, 150, 150, 255))

generationtimer = t.time()

#normal
normaltexture = load_texture_from_image(normalimage)
normaltextureicon = load_texture_from_image(normalimageicon)
#permanent
permanenttexture = load_texture_from_image(permanentimage)
permanenttextureicon = load_texture_from_image(permanentimageicon)
#wall
walltexture = load_texture_from_image(wallimage)
walltextureicon = load_texture_from_image(wallimageicon)
#mover
movertexture = load_texture_from_image(moverimage)
movertextureicon = load_texture_from_image(moverimageicon)

while not window_should_close():
    set_trace_log_level(LOG_ERROR)
    set_target_fps(70)

    if BuildMode:   
        cameramovement()
        #camera
            
        if is_key_down(KEY_S):
            BuildMode = False
        #simulation mode
        if is_key_pressed(KEY_A):
            spg += 0.25
        if is_key_pressed(KEY_D) and spg - 0.25 > 0:
            spg -= 0.25
        #gps changers
        
        if is_key_pressed(KEY_W):
            image_rotate(moverimage, 90)
            movertexture = load_texture_from_image(moverimage)
            image_rotate(moverimageicon, 90)
            movertextureicon = load_texture_from_image(moverimageicon)
            if direction == [-1, 0]: #left
                direction = [0, -1]
                directiondisplay = "up"
            elif direction == [0, -1]: #up
                direction = [1, 0]
                directiondisplay = "right"
            elif direction == [1, 0]: #right
                direction = [0, 1]
                directiondisplay = "down"
            elif direction == [0, 1]: #left
                direction = [-1, 0]
                directiondisplay = "left"
        #mover cell rotation
        
        if is_key_down(KEY_PERIOD):
            allcells = set([])
            currentg = 0
        #clear
        
        if is_key_pressed(KEY_ONE):
            normalchosen = True
            permanentchosen = False
            wallchosen = False
            moverchosen = False
        elif is_key_pressed(KEY_TWO):
            normalchosen = False
            permanentchosen = True
            wallchosen = False
            moverchosen = False
        elif is_key_pressed(KEY_THREE):
            normalchosen = False
            permanentchosen = False
            wallchosen = True
            moverchosen = False
        elif is_key_pressed(KEY_FOUR):
            normalchosen = False
            permanentchosen = False
            wallchosen = False
            moverchosen = True
        #cellselection
            
        if is_key_pressed(KEY_R):
            cellcolor = RED
            displaycellcolor = "Red"
        elif is_key_pressed(KEY_O):
            cellcolor = ORANGE
            displaycellcolor = "Orange"
        elif is_key_pressed(KEY_Y):
            cellcolor = YELLOW
            displaycellcolor = "Yellow"
        elif is_key_pressed(KEY_G):
            cellcolor = GREEN
            displaycellcolor = "Green"
        elif is_key_pressed(KEY_B):
            cellcolor = BLUE
            displaycellcolor = "Blue"
        elif is_key_pressed(KEY_P):
            cellcolor = VIOLET
            displaycellcolor = "Purple"
        elif is_key_pressed(KEY_V):
            cellcolor = PURPLE
            displaycellcolor = "Violet"
        elif is_key_pressed(KEY_N):
            cellcolor = (45, 45, 45, 255) #black
            displaycellcolor = "Black"
        elif is_key_pressed(KEY_M):
            cellcolor = WHITE
            displaycellcolor = "White"
        #colorselection

        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            CellChange = True
            mposx = (get_mouse_x()/camera.zoom) + camerapos[0]
            mposy = (get_mouse_y()/camera.zoom) + camerapos[1]
            mposx = mposx - (mposx % 50)
            mposy = mposy - (mposy % 50)
            
            if permanentchosen: #permanent
                cell = Cell([mposx, mposy], 0, True, False, False, [0, 0], permanenttexture, cellcolor)
            elif wallchosen: #wall
                cell = Cell([mposx, mposy], 0, False, True, False, [0, 0], walltexture, WHITE)
            elif moverchosen: #mover
                cell = Cell([mposx , mposy], 0, False, False, True, direction, movertexture, cellcolor)
            elif normalchosen: #normal
                cell = Cell([mposx, mposy], 0, False, False, False, [0, 0], normaltexture, cellcolor)
            for i in allcells.copy():
                if i.pos == cell.pos:
                    allcells.remove(i)
                    CellChange = False
                    undo.append(i)
                    #cells remove and add
            if CellChange:
                undo.append(cell)
                allcells.add(cell)
                
        #CELL CREATION IN BUILDER MODE
            
        if is_key_pressed(KEY_C):
            CellChange = True
            if undo != []:
                for i in allcells.copy():
                    if i.pos == undo[-1].pos:
                        allcells.discard(undo[-1])
                        undo.pop()
                        break
                        #cells remove and add
                if CellChange and len(undo) > 0:
                    allcells.add(undo[-1])
                
                if len(undo) > 10: #depth
                    undo.pop(0)
                   
        #UNDO
        
        camera.target = camerapos
        
        cellcount = len(allcells)
        
        begin_drawing()
        begin_mode_2d(camera)
        clear_background((20, 20, 20)) #background - black but a bit lighter
        
        gridlines(camerapos)

        for i in allcells:
            draw_texture_v(i.texture, i.pos, i.color)
        #DRAWS 
        
        draw_rectangle_v([camerapos[0], camerapos[1]], [int(450/camera.zoom), int(150/camera.zoom)], (20, 20, 20, 255)) 
        draw_line_ex([camerapos[0] + int(450/camera.zoom), camerapos[1]], [camerapos[0] + int(450/camera.zoom), camerapos[1] + int(151/camera.zoom)], 2/camera.zoom, DARKGRAY)
        draw_line_ex([camerapos[0], camerapos[1] + int(150/camera.zoom)], [camerapos[0] + int(450/camera.zoom), camerapos[1] + int(150/camera.zoom)], 2/camera.zoom, DARKGRAY)
        #background of info
        
        draw_text("Build-Mode (S)", camerapos[0], camerapos[1], int(30/camera.zoom), SKYBLUE)
        draw_text(f"SPG (A/D): {round(spg, 2)}s", camerapos[0], camerapos[1] + int(30/camera.zoom), int(30/camera.zoom), GREEN)
        draw_text(f"Cells #: {cellcount} | Generation: {currentg}", camerapos[0], camerapos[1] + int(60/camera.zoom), int(30/camera.zoom), LIGHTGRAY)
        draw_text(f"Direction (W): {directiondisplay}", camerapos[0], camerapos[1] + int(90/camera.zoom), int(30/camera.zoom), GOLD)
        draw_text(f"Color (ROYGBPVMN): {displaycellcolor}", camerapos[0], camerapos[1] + int(120/camera.zoom), int(30/camera.zoom), cellcolor)
        #info
        
        #normal
        image_resize(normalimageicon, int(35/camera.zoom), int(35/camera.zoom))
        normaltextureicon = load_texture_from_image(normalimageicon)
        draw_texture_v(normaltextureicon, Vector2(int(580/camera.zoom) + camerapos[0], int(800/camera.zoom) + camerapos[1]), cellcolor)
        #permanent
        image_resize(permanentimageicon, int(35/camera.zoom), int(35/camera.zoom))
        permanenttextureicon = load_texture_from_image(permanentimageicon)
        draw_texture_v(permanenttextureicon, Vector2(int(650/camera.zoom) + camerapos[0], int(800/camera.zoom) + camerapos[1]), cellcolor)
        #wall
        image_resize(wallimageicon, int(35/camera.zoom), int(35/camera.zoom))
        walltextureicon = load_texture_from_image(wallimageicon)
        draw_texture_v(walltextureicon, Vector2(int(720/camera.zoom) + camerapos[0], int(800/camera.zoom) + camerapos[1]), WHITE)
        #mover
        image_resize(moverimageicon, int(35/camera.zoom), int(35/camera.zoom))
        movertextureicon = load_texture_from_image(moverimageicon)
        draw_texture_v(movertextureicon, Vector2(int(790/camera.zoom) + camerapos[0], int(800/camera.zoom) + camerapos[1]), cellcolor)
        
        hotbar(camerapos, normalchosen, permanentchosen, wallchosen, moverchosen)
        
        end_mode_2d()
        end_drawing()
    
    if not BuildMode:
        if is_key_down(KEY_X):
            BuildMode = True
        #build mode
        
        elapsed = round(t.time() - generationtimer, 6)
        
        if round(elapsed % spg, 6) == 0:
            addthesecells = set([])
            remove = set([])
            
            cellcount = len(allcells)

            for i in allcells:
                for j in allcells:
                    ecellpos = None
                    if not i.wall:
                        if [(i.pos[0] + checkrement), i.pos[1]] != j.pos:
                            ecellpos = [(i.pos[0] + checkrement), i.pos[1]]
                            ECheckBorn(ecellpos)
                            # + _
                        if [i.pos[0], (i.pos[1] + checkrement)] != j.pos:
                            ecellpos = [i.pos[0], (i.pos[1] + checkrement)]
                            ECheckBorn(ecellpos)
                            # _ +
                        if [(i.pos[0] - checkrement), i.pos[1]] != j.pos:
                            ecellpos = [(i.pos[0] - checkrement), i.pos[1]]
                            ECheckBorn(ecellpos)
                            # - _
                        if [i.pos[0], (i.pos[1] - checkrement)] != j.pos:
                            ecellpos = [i.pos[0], (i.pos[1] - checkrement)]
                            ECheckBorn(ecellpos)
                            # _ -
                        if [(i.pos[0] + checkrement), (i.pos[1] + checkrement)] != j.pos:
                            ecellpos = [(i.pos[0] + checkrement), (i.pos[1] + checkrement)]
                            ECheckBorn(ecellpos)
                            # + +           
                        if [(i.pos[0] - checkrement), (i.pos[1] + checkrement)] != j.pos:
                            ecellpos = [(i.pos[0] - checkrement), (i.pos[1] + checkrement)]
                            ECheckBorn(ecellpos)
                            # - +
                        if [(i.pos[0] + checkrement), (i.pos[1] - checkrement)] != j.pos:
                            ecellpos = [(i.pos[0] + checkrement), (i.pos[1] - checkrement)]
                            ECheckBorn(ecellpos)
                            # + -
                        if [(i.pos[0] - checkrement), (i.pos[1] - checkrement)] != j.pos:
                            ecellpos = [(i.pos[0] - checkrement), (i.pos[1] - checkrement)]
                            ECheckBorn(ecellpos)
                            # - -
                #Cell Borned Check

            cellsmaydie = filter(CellAliveFilter, allcells)
            for i in cellsmaydie:
                for j in allcells:
                    if i.pos != j.pos and not j.wall:
                        if [(i.pos[0] + checkrement), i.pos[1]] == j.pos:
                            i.cellcount += 1               
                            # + _
                        elif [i.pos[0], (i.pos[1] + checkrement)] == j.pos:
                            i.cellcount += 1
                            # _ +
                        elif [(i.pos[0] - checkrement), i.pos[1]] == j.pos:
                            i.cellcount += 1
                            # - _
                        elif [i.pos[0], (i.pos[1] - checkrement)] == j.pos:
                            i.cellcount += 1
                            # _ -
                        elif [(i.pos[0] + checkrement), (i.pos[1] + checkrement)] == j.pos:
                            i.cellcount += 1    
                            # + +           
                        elif [(i.pos[0] - checkrement), (i.pos[1] + checkrement)] == j.pos:
                            i.cellcount += 1
                            # - +
                        elif [(i.pos[0] + checkrement), (i.pos[1] - checkrement)] == j.pos:
                            i.cellcount += 1
                            # + -
                        elif [(i.pos[0] - checkrement), (i.pos[1] - checkrement)] == j.pos:
                            i.cellcount += 1
                            # - -
                if i.cellcount > 3 and not i.perm and not i.wall: #overpopulation
                    remove.add(i)
                elif i.cellcount < 2 and not i.perm and not i.wall and not i.mover: #isolation
                    remove.add(i)
                else:
                    i.cellcount = 0
                #Death/Alive Cell Check
            
            for i in allcells:
                if i.mover:
                    i.pos = [i.pos[0] + checkrement * i.direction[0], i.pos[1] + checkrement * i.direction[1]]

            begin_drawing()
            begin_mode_2d(camera)
            clear_background((20, 20, 20)) #background - black but a bit lighter
            
            gridlines(camerapos)

            for i in allcells:
                draw_texture_v(i.texture, i.pos, i.color)
            #DRAWS
            
            draw_rectangle_v([camerapos[0], camerapos[1]], (400/camera.zoom, 95/camera.zoom), (20, 20, 20, 255)) #black
            draw_line_ex([camerapos[0] + int(400/camera.zoom), camerapos[1]], [camerapos[0] + int(400/camera.zoom), camerapos[1] + int(96/camera.zoom)], 2/camera.zoom, DARKGRAY)
            draw_line_ex([camerapos[0], camerapos[1] + int(95/camera.zoom)], [camerapos[0] + int(400/camera.zoom), camerapos[1] + int(95/camera.zoom)], 2/camera.zoom, DARKGRAY)
            #background of info
               
            draw_text("Simulation-Mode (X)", camerapos[0], camerapos[1], int(30/camera.zoom), SKYBLUE)
            draw_text(f"SPG: {round(spg, 2)}s", camerapos[0], camerapos[1] + int(30/camera.zoom), int(30/camera.zoom), GREEN)
            draw_text(f"Cells #: {cellcount} | Generation: {currentg}", camerapos[0], camerapos[1]  + int(60/camera.zoom), int(30/camera.zoom), LIGHTGRAY)
            #info

            end_mode_2d()
            end_drawing()
            
            for k in remove:
                allcells.discard(k)
            for k in addthesecells:
                allcells.add(k)
            
            currentg += 1

close_window()