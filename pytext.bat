@echo off

rem set the pytext main.py directory to yours. Feel free to change it.
rem the default directory is: (your user)\pytext\main.py
set pytext-main-dir="%UserProfile%\pytext\main.py"

python %pytext-main-dir% %*
