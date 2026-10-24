#Requires AutoHotkey v2.0
#SingleInstance Force

; ==============================================================================
; CONFIGURATION
; ==============================================================================
global API_KEY := "[Google AI Studio API key]"
global API_URL := "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
global MODEL   := "gemini-2.5-flash"

; ==============================================================================
; HOTKEY: Ctrl + Alt + A
; ==============================================================================
^!a::
{
    ; 1. Copy selected text
    prevClipboard := ClipboardAll()
    A_Clipboard := ""
    Send("^c")
    if !ClipWait(1) {
        selectedText := ""
    } else {
        selectedText := A_Clipboard
    }

    ; 2. Ask what you want the AI to do
    ib := InputBox(
        "Enter instructions (e.g., 'Summarize', 'Fix grammar', 'Format as table', 'Make professional'):",
        "Notion AI Assistant",
        "w420 h130",
        "Improve writing and reformat as markdown"
    )
    if (ib.Result != "OK" || Trim(ib.Value) == "") {
        A_Clipboard := prevClipboard
        return
    }
    userInstruction := ib.Value

    ; 3. Visual feedback
    ToolTip("Processing...")

    ; 4. Call the LLM API
    try {
        result := CallLLM(selectedText, userInstruction)
        result := RegExReplace(result, "s)^```(?:markdown)?\R([\s\S]*?)\R```$", "$1")

        ; 5. Put the result into the clipboard
        A_Clipboard := result
        
        SoundBeep(750, 150)
        ToolTip("Notion AI finished! Output copied to clipboard.")
        SetTimer(() => ToolTip(), -2000) 
        
    } catch Error as err {
        MsgBox("Error: " . err.Message, "Notion AI Error", 16)
        ToolTip() 
    }
}

; ==============================================================================
; API HELPER FUNCTIONS
; ==============================================================================
CallLLM(selectedText, instruction) {
    http := ComObject("WinHttp.WinHttpRequest.5.1")
    http.Open("POST", API_URL, false)
    http.SetRequestHeader("Content-Type", "application/json")
    if (API_KEY != "")
        http.SetRequestHeader("Authorization", "Bearer " . API_KEY)

    systemPrompt := "You are a Notion workspace assistant. Modify or generate content strictly based on the user's instructions. "
        . "Return ONLY raw Markdown (using headers #, lists -, bold **, tables, callouts where helpful). "
        . "Do NOT wrap your final response in triple backticks (```markdown). Do NOT include conversational filler like 'Sure, here is...'."

    combinedUser := (selectedText != "")
        ? "INSTRUCTION: " . instruction . "`n`nCONTENT TO PROCESS:`n" . selectedText
        : "INSTRUCTION: " . instruction

    body := '{"model": "' . MODEL . '", "messages": ['
        . '{"role": "system", "content": "' . EscapeJSON(systemPrompt) . '"},'
        . '{"role": "user", "content": "' . EscapeJSON(combinedUser) . '"}'
        . ']}'

    http.Send(body)

    if (http.Status != 200)
        throw Error("HTTP " . http.Status . ": " . http.ResponseText)

    resp := http.ResponseText
    if RegExMatch(resp, 's)"content":\s*"((?:[^"\\]|\\.)*)"', &match) {
        return UnescapeJSON(match[1])
    } else {
        throw Error("Could not parse API response.")
    }
}

EscapeJSON(str) {
    str := StrReplace(str, "\", "\\")
    str := StrReplace(str, '"', '\"')
    str := StrReplace(str, "`r`n", "\n")
    str := StrReplace(str, "`n", "\n")
    str := StrReplace(str, "`r", "\n")
    str := StrReplace(str, "`t", "\t")
    return str
}

UnescapeJSON(str) {
    str := StrReplace(str, '\"', '"')
    str := StrReplace(str, '\n', "`n")
    str := StrReplace(str, '\r', "")
    str := StrReplace(str, '\t', "`t")
    str := StrReplace(str, '\\', '\')
    
    pos := 1
    while (pos := RegExMatch(str, "\\u([0-9a-fA-F]{4})", &m, pos)) {
        str := SubStr(str, 1, pos - 1) . Chr(Integer("0x" . m[1])) . SubStr(str, pos + 6)
        pos += 1 
    }
    return str
}
