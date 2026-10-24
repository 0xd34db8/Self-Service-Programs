; ============================
;https://www.autohotkey.com/
;How to install:

;Press Win + R → type:

;shell:startup

;Copy your .ahk file into this folder
;now , it will start automatically at login
; ============================

; =========================================================
; VS Code–like text editing shortcuts (Global)
; AutoHotkey v1.x
; =========================================================
; This script mimics common VS Code shortcuts across Windows
; It automatically disables itself inside VS Code to avoid
; conflicts with native behavior.
; =========================================================

; ---------------------------------------------------------
; Master toggle key: ` (backtick) → suspends/resumes all hotkeys
; ---------------------------------------------------------
`::
Suspend, Permit  ; allow this hotkey to remain active
Suspend, Toggle
if A_IsSuspended
    ToolTip, Script is OFF (shortcuts disabled)
else
    ToolTip, Script is ON (shortcuts active)
SetTimer, RemoveToolTip, 1500
return

; ---------------------------------------------------------
; Label to remove tooltip after delay
; ---------------------------------------------------------
RemoveToolTip:
ToolTip
return

; ---------------------------------------------------------
; Do NOT apply these shortcuts when VS Code is active
; ---------------------------------------------------------
#IfWinNotActive ahk_exe Code.exe


; ---------------------------------------------------------
; Alt + Up  → Move current line up
; ---------------------------------------------------------
!Up::
Send, {Home}+{End}^x{Up}{Home}^v
return


; ---------------------------------------------------------
; Alt + Down → Move current line down
; ---------------------------------------------------------
!Down::
Send, {Home}+{End}^x{Down}{Home}^v
return


; ---------------------------------------------------------
; Shift + Alt + Up → Duplicate line upward
; ---------------------------------------------------------
+!Up::
Send, {Home}+{End}^c{Home}{Enter}^v{Up}
return


; ---------------------------------------------------------
; Shift + Alt + Down → Duplicate line downward
; ---------------------------------------------------------
+!Down::
Send, {Home}+{End}^c{End}{Enter}^v
return


; ---------------------------------------------------------
; Ctrl + L → Select current line
; ---------------------------------------------------------
^l::
Send, {Home}+{Shift down}{End}{Shift up}
return

; ---------------------------------------------------------
; Ctrl + / → Comment line (basic // comment)
; NOTE:
; - Works best in code editors / markdown
; - Assumes // comment style (JS, TS, C-like languages)
; ---------------------------------------------------------
^/::
Send, {Home}//{Space}
return


; ---------------------------------------------------------
; Ctrl + D → Approximate "select next occurrence"
; NOTE:
; - This is NOT true multi-cursor
; - Copies current selection/word
; - Finds next match and selects it
; ---------------------------------------------------------
^d::
Send, ^c
Sleep, 50
Send, ^f^v{Enter}{Esc}
Send, +^{Right}
return


; ---------------------------------------------------------
; End of conditional block
; ---------------------------------------------------------
#IfWinActive


; =========================================================
; End of file
; =========================================================
