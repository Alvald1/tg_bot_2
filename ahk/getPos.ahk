
Loop{
    Sleep, 2000
    WinGetActiveStats, Title, Width, Height,x,y
    MouseGetPos, X, Y
    Width:=Width
    MsgBox, %Width% X %Height% `n%X% : %Y% 
}

;cd S:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe /in C:\tg-bot\ahk\getPos.ahk /out C:\tg-bot\exe\getPos.exe