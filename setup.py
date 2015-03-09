from distutils.core import setup
import py2exe
from ocempgui import *
import os
import sys

sys.path.append("C:")
pygame_files = ["C:\Python27\Lib\site-packages\pygame\SDL_ttf.dll", "C:\Python27\lib\site-packages\pygame\libogg-0.dll"]

dungeon_data_files = ["C:\Users\Robert\Documents\platformer\Platformer\LevelEditor\dungeon_map_files\dungeon0"]
my_data_files = [("pygame_files", pygame_files), ("dungeon_map_files", dungeon_data_files)]
level_editor_dir = "C:\Users\Robert\Documents\platformer\Platformer\LevelEditor\\"

for files in os.listdir(level_editor_dir):
   f1 = level_editor_dir + files
   if os.path.isfile(f1): # skip directories
      f2 = '', [f1]
      my_data_files.append(f2)

def all_files_in_dir(new_dir_name, file_dir):
   all_files = []
   for files in os.listdir(file_dir):
      f1 = file_dir + files
      if os.path.isfile(f1): # skip directories
         f2 = new_dir_name, [f1]
         all_files.append(f2)
      else:
         next_files = all_files_in_dir(new_dir_name, f1 + "\\")
         for i in next_files:
            all_files.append(i)
   return all_files

#TODO: if I repeat more sections of code like those below, make a special method to save time.
main_images_dir = "C:\Users\Robert\Documents\platformer\Platformer\LevelEditor\images\\"
image_files = all_files_in_dir("images", main_images_dir)
for i in image_files:
   my_data_files.append(i)

main_animations_dir = "C:\Users\Robert\Documents\platformer\Platformer\LevelEditor\\animations\\"
animation_files = all_files_in_dir("animations", main_animations_dir)
for a in animation_files:
   my_data_files.append(a)

main_data_dir = "C:\Users\Robert\Documents\platformer\Platformer\data\\"
data_files = all_files_in_dir("data", main_data_dir)
for d in data_files:
   my_data_files.append(d)

setup(
   data_files = my_data_files,
   options = {
      "numpy" : {
         "includes" : ["_umath_linalg.pyd", "fftpack_lite.pyd"],
         },
      "dialog" : {
         "includes" : ["pygame.font"],
         },
      #"filemanagercontainer" : {
      #   "includes" : ["ocempgui.widgets"],
      #}
      #"ocempgui" : {
      #   "includes" : ["access", "draw", "events", "objects", "widgets"],
      #   "packages" : ["access", "draw", "events", "objects", "widgets"],
      #   }
      },
   windows = ['gamelauncher.py']
)

"""
   OLEAUT32.dll - C:\WINDOWS\system32\OLEAUT32.dll
   USER32.dll - C:\WINDOWS\system32\USER32.dll
   IMM32.dll - C:\WINDOWS\system32\IMM32.dll
   SHELL32.dll - C:\WINDOWS\system32\SHELL32.dll
   ole32.dll - C:\WINDOWS\system32\ole32.dll
   COMDLG32.dll - C:\WINDOWS\system32\COMDLG32.dll
   
   COMCTL32.dll - C:\WINDOWS\system32\COMCTL32.dll
   ADVAPI32.DLL - C:\WINDOWS\system32\ADVAPI32.DLL
   
   msvcrt.dll - C:\WINDOWS\system32\msvcrt.dll
   WS2_32.dll - C:\WINDOWS\system32\WS2_32.dll
   GDI32.dll - C:\WINDOWS\system32\GDI32.dll
   WINMM.DLL - C:\WINDOWS\system32\WINMM.DLL
   KERNEL32.dll - C:\WINDOWS\system32\KERNEL32.dll

   _umath_linalg.pyd - c:\Python27\lib\site-packages\numpy\linalg\_umath_linalg.pyd
   fftpack_lite.pyd - c:\Python27\lib\site-packages\numpy\fft\fftpack_lite.pyd   
   SDL_ttf.dll - c:\Python27\lib\site-packages\pygame\SDL_ttf.dll
   libogg-0.dll - c:\Python27\lib\site-packages\pygame\libogg-0.dll
"""
