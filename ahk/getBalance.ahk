Sleep, 300
MouseMove, 1445*0.876, 155, 5
Sleep, 300
Click Left
MouseMove, 1305*0.792, 229, 5
Sleep, 300
Click Left
Click Left
Send, ^c
FileDelete, bal.txt
FileAppend, % Clipboard, bal.txt, UTF-8
MouseMove, 419*0.372, 155, 5
Sleep, 300
Click Left

;cd S:\Program Files\AutoHotkey\Compiler & Ahk2Exe.exe /in C:\tg-bot\ahk\getBalance.ahk /out C:\tg-bot\exe\getBalance.exe