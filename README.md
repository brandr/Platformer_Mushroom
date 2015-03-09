Platformer
==========

A currently unnamed platformer which will be sort of like super metroid and based around exploration.
We need more programmers, sprite artists, and pretty much every type of game making person (even idea guys).

HOW TO INSTALL THE PLATFORMER (as a developer): 

NOTE: These steps are currently Windows-only. I will add instructions for other operating systems if I meet developers who use them.

1. Install python 2.7: https://www.python.org/download/releases/2.7.8/ (on windows, you want the "Windows x86 MSI Installer (2.7.8)")

2. Install pygame: http://www.pygame.org/download.shtml (on windows, you want "pygame-1.9.1.win32-py2.7.msi")

3. Search for "IDLE" on your computer and open the IDLE (python gui). Type in "import pygame" and press enter. If you get an error message, pygame
   was installed incorrectly. If nothing happens, everything went perfectly.

4. Install numpy:(not yet sure if this works)
	a. Go to http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy. 
	b. If you have a 64-bit machine, click the link that says “numpy‑MKL‑1.9.0.win-amd64‑py2.7.exe”. If you have a 32-bit machine, click 	the link that says “numpy‑MKL‑1.9.0.win32‑py2.7.exe”
	b. Run this exe to install numpy.

5. Install git bash: http://git-scm.com/downloads

6. Add python to your computer's system variables. (This is where it gets a bit tricky.)  On windows 7, the process should go something like this:
	
	a. Right click on "my computer" and click "properties".

	b. On the left pane, click "advanced system settings".

	c. In the window that appears, click "environment variables".

	d. (DO NOT MESS THIS PART UP) In the "system variables" pane: 

		i. scroll down until you find a variable called PATH.

		ii. select PATH and click "edit".

		iii. Click on the "variable value" field but do NOT delete anything from it. Scroll all the way to the right.

		iv. Add the python system variable at the end, separated by a semicolon. (You might want to check where python was saved to your computer, just to be safe.)
			For instance, if you see "...;C:\Program Files (x86)\Windows Live\Shared" at the end, add to it so it says
			"...;C:\Program Files (x86)\Windows Live\Shared;C:\Python27\".

		v. Click "Ok", then "Ok" again in the "enviorment variables" windows, then "apply" (or "ok" if "apply" is greyed out.)

7. Install Ocempgui. 

	a. http://sourceforge.net/projects/ocemp/files/ocempgui/0.2.9/
   	   (You want OcempGUI-0.2.9.tar.gz, not the tar.gz.asc.)

   	b. Unzip the file and save it somewhere on your computer.

   	c. Open git bash and navigate to the file you just saved. To navigate, enter the following commands into the git bash terminal:

   		i. ls: shows all the files in the current directory

   		ii. cd (directory) : go into whatever directory used. (Do not actually include parens when typing the directory.)

   		iii. cd .. : go up, out of the current directory.

   		iv. (press tab): Autocomplete whatever you are currently typing. This is VERY useful when typing long filenames and you should get used to using it.

   	d. Once you navigate to the directory containing setup.py (inside the ocempGUI folder), enter the command "python setup.py install". This will install ocempgui

8. Actually install the game.

	a. Create a folder on your computer where the game will be stored.

	b. Navigate to this folder in git bash, the same way you did in step 7.

	c. Enter the command "git clone https://github.com/brandr/Platformer.git" 

	d. Navigate inside the cloned repo (I think by entering "cd Platformer").

	e. play the game by entering "python gamelaucher.py". If everything went well it should run fine.

	f. To open the level editor, cancel the game (either by closing it or with ctrl-c in git bash) and then enter "cd LevelEditor" followed by "python dungeoneditorlauncher.py".
