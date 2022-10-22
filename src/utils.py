from subprocess import Popen, PIPE

def paste_text(txt: str):
    scpt = '''
        on run {x}
            tell app "System Events" to keystroke x
        end run'''
    args = [txt]

    p = Popen(['/usr/bin/osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    _, stderr = p.communicate(scpt.encode())
    
    if stderr:
        print (stderr.decode())

def word_size_bytes(word: str) -> int:
        return len(word.encode("utf-8"))