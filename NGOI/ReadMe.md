# NGOI

Hotkeys:
-Holding down X activates Builder Mode
-Holding down S activates Simulation Mode
-Pressing Z resets Zoom (Build Mode)
-Pressing Q decreases Zoom (Build Mode)
-Pressing E increases Zoom (Build Mode)
-Pressing W rotates Direction Clockwise (Build Mode)
-Pressing . resets Board (Build Mode)
-Arrow Keys = Movement across the Board (Build Mode)

Left Clicking creates a Cell (Build Mode)
(1) selects normal cell
(2) selects permanent cell
(3) selects wall cell
(4) selects mover cell

Game Rules:

SPG means Seconds Per Generation (how many generations are executed per second)

Normal Cells (Conway's GOL Cells)
-Conway's GOL cell logic

Permanent Cells
-Can never die from overpopulation and isolation
-Can help create cells

Walls Cells
-Can never die from overpopulation and isolation
-Can not help create cells

Mover Cells
-Can never die from overpopulation and isolation (may change to can only die from overpopulation)
-Can help create cells
-Moves by 1 cell at the END of a generation (previous position is considered in the program)

To select colors it is the letter at the start of each color which chooses them.
Except black and white which are N and M.

Newly borned cells are the color of the RGB average of its parents ((p1+p2+p3)/3) for each color).

RUN FILE RunGame.py TO RUN THE GAME LOLLLLLL.

MAKE SURE TO DOWNLOAD ALL FILES AND KEEP THEM IN THEIR RESPECTIVE FOLDER.


INSTALLATION

1. Install pyray
2. Install raylib
4. Install os
5. Install time

All the libraries needed.
