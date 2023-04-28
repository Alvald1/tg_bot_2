Sleep, 300
WinGetActiveStats, Title, Width, Height,x,y
MouseMove, % Width / 2, 395, 5
Sleep, 300
Click Left
Sleep, 300
MouseMove, 24, 981*0.7, 5
Sleep, 300
Click Left
Sleep, 300
MouseMove, % Width / 2, 355, 5
Sleep, 300
Click Left
Send, ^c
FileDelete, tmp.txt
FileAppend, % Clipboard, tmp.txt, UTF-8

;cd S:\Program Files\AutoHotkey\Compiler & Ahk2Exe.exe /in C:\tg-bot\ahk\getHistory.ahk /out C:\tg-bot\exe\getHistory.exe