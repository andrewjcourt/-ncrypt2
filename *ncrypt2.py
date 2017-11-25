'''                 ________________________________

                               *ncrypt2
                            by Andrew Court
                            
                    ________________________________

'''

# BUGS
# When text is encryted, new typing should also be encrypted - or blocked until de_code.

from Tkinter import *
import tkMessageBox
from tkFileDialog import *
import time
import random
import os

status = 'OFF'
pin = '2008'
entry_str = keyentry_str = key = deleted_entry = filepath = ''
entry_length = deleted_length = 0
scramble_status = key_in_progress = encode_flag = False


def on_off():                   # turn machine on or off

    global status, keyentry_str, key

    if status== 'ON' and entry_str == '': 
        status= 'OFF'
        buttons('off')
        screen_Live.config(state = DISABLED)
        display_Key.config(fg = bkgd)
        display_Filepath.config(fg = bkgd)
        counter.config(fg = bkgd)
        display_PowerState.config(text = 'Power OFF')
        update_display()
        
    elif status== 'OFF':

        tkMessageBox.showinfo('Key required', 'Enter unlock key.')
        set_key()
        if keyentry_str != pin:
            keyentry_str = ''
            key = ''
            update_display()
            tkMessageBox.showwarning('Access Denied', 'Incorrect Key - Access Denied.')
            nums('off')
            buttons('off')
            button_StartMachine.config(state = NORMAL)
            return
        keyentry_str = ''
        key=''
        status= 'ON'
        buttons('on')
        display_Key.config(fg = 'yellow')
        display_Filepath.config(fg = 'yellow')
        counter.config(fg = 'yellow')
        display_PowerState.config(text = 'Power ON')

        if deleted_entry == '':
            button_UndoReset.config(state = DISABLED)

        else:
            button_UndoReset.config(state = NORMAL)
        
        update_display()

    return


def read_keys(event):           # process keyboard input

    if status == 'OFF' or scramble_status or key_in_progress: return
    
    global entry_str, entry_length, deleted_entry

    button_UndoReset.config(state = DISABLED)
    button_ClearText.config(state = NORMAL)

    k = event.keysym
    no_keys = ('BackSpace', 'Return', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R',
               'Super_L', 'Meta_L', 'Alt_L', 'Alt_R', 'Caps_Lock', 'Tab', 'Clear',
               'Pause', 'Scroll_Lock', 'Escape', 'Home', 'Up', 'Down', 'Left', 'Right',
               'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
               'F12', 'space')

    if k not in no_keys and entry_length < 1000:
        entry_str += event.char
        entry_length += 1
        deleted_entry = ''

    if k == 'space' and entry_str[-1:] != ' ' and entry_length < 1000:  
        entry_str += event.char                              
        entry_length += 1
        deleted_entry = ''                                                                                                                                                                 
                                            
    if k == 'BackSpace' and len(entry_str):
        entry_str = entry_str[:-1]
        entry_length = 0
        for x in entry_str:         #NOT: for x in range (0, len(entry_str)):
            if x == '\n':           #NOT: if entry_str[x:x+1] == '\n':
                entry_length += (70-(entry_length%70))
            else:
                entry_length +=1
        deleted_entry = ''
        
    if k == 'Return' and entry_length < 910:
        if entry_str[-1:] == ' ': entry_str = entry_str[:-1]
        entry_str += '\n'
        entry_length += (70-(entry_length%70))
        deleted_entry = ''

    screen_Live.config(text = (entry_str + '_'))
    counter.config(text = str(1000-entry_length))
        
    return


def update_display():           # refresh on-screen information & force focus on text input screen

    if status== 'ON':
        fgcolour = 'yellow'
    else:
        fgcolour = bkgd

    display_Key.config(text = 'Key: %s' %key, font = CounterFont, bg = frgd, fg = fgcolour)
    display_Filepath.config(text = 'File: %s' %filepath, font = CounterFont, bg = frgd, fg = fgcolour)
    display_PowerState.config(text = 'Power %s' %status, fg = fgcolour)

    screen_Live.focus_force()

    return


def buttons(x):                 # turn GUI function buttons on or off

    if x == 'on': st = 'normal'
    else:
        st = 'disabled'

    button_Scramble.config(state = st)
    button_ClearText.config(state = st)
    button_UndoReset.config(state = st)
    button_SaveText.config(state = st)
    button_Setkey.config(state = st)
    button_Encode.config(state = st)
    button_Decode.config(state = st)
    button_OpenFile.config(state = st)

    return


def nums(x):                    # turn GUI numeric keypad on or off

    if x == 'on': st = 'normal'
    else:
        st = 'disabled'

    button1.config(state = st)
    button2.config(state = st)
    button3.config(state = st)
    button4.config(state = st)
    button5.config(state = st)
    button6.config(state = st)
    button7.config(state = st)
    button8.config(state = st)
    button9.config(state = st)
    button0.config(state = st)
    buttonX.config(state = st)
    
    return


def set_key():                  # accept 4-digit key 

    global key, key_in_progress, keyentry_str

    if encode_flag:
        tkMessageBox.showinfo('Encrypted message',
                              'Can\'t set a new key while message remains encrypted.')
        return

    key_in_progress = True
    keyentry_str = key

    display_Key.place_forget()
    display_KeyEntry.place(x = 600, y = 330)

    nums('on')
    buttons('off')
    button_StartMachine.config(state = DISABLED)

    button_Phantom.config(state = NORMAL)
    button_Phantom.bind('<Key>', key_entry)
    button_Phantom.focus_force()
    
    while key_in_progress:
        
        button_Phantom.update()
        display_KeyEntry.config(text = 'Key: %s_' %keyentry_str)

    key = keyentry_str

    display_Key.config(state = NORMAL)
    display_Key.place(x = 600, y = 330)

    nums('off')
    buttons('on')
    button_UndoReset.config(state = DISABLED)
    button_StartMachine.config(state = NORMAL)
    button_Phantom.config(state = DISABLED)
    display_KeyEntry.place_forget()
    update_display()

    return


def key_entry(event):           # process keyboard input for key entry

    global keyentry_str, key_in_progress

    num_keys = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

    if event.char in num_keys and len(keyentry_str) < 4:
        flash_num(event.char)
        keyentry_str += event.char
        return
    if event.keysym == 'BackSpace' and len(keyentry_str):
        keyentry_str = keyentry_str[:-1]
        return
    if event.keysym == 'Return' and len(keyentry_str) == 4:
        key_in_progress = False
        return

    return


def flash_num(num):             # numeric keypad effect

    button = int(num)

    if button == 1:
        button1.config(fg = flash)
        root.after(1000, lambda: button1.config(fg = frgd))
    if button == 2:
        button2.config(fg = flash)
        root.after(1000, lambda: button2.config(fg = frgd))
    if button == 3:
        button3.config(fg = flash)
        root.after(1000, lambda: button3.config(fg = frgd))
    if button == 4:
        button4.config(fg = flash)
        root.after(1000, lambda: button4.config(fg = frgd))
    if button == 5:
        button5.config(fg = flash)
        root.after(1000, lambda: button5.config(fg = frgd))
    if button == 6:
        button6.config(fg = flash)
        root.after(1000, lambda: button6.config(fg = frgd))
    if button == 7:
        button7.config(fg = flash)
        root.after(1000, lambda: button7.config(fg = frgd))
    if button == 8:
        button8.config(fg = flash)
        root.after(1000, lambda: button8.config(fg = frgd))
    if button == 9:
        button9.config(fg = flash)
        root.after(1000, lambda: button9.config(fg = frgd))
    if button == 0:
        button0.config(fg = flash)
        root.after(1000, lambda: button0.config(fg = frgd))

    return


def reset_text():               # clear entered text

    global entry_str, entry_length, deleted_entry, deleted_length, scramble_status

    if scramble_status or entry_length == 0: return

    encode_flag = False
    deleted_entry = entry_str
    entry_str = ''
    deleted_length = entry_length
    entry_length = 0
    scramble_status = False
    screen_Live.config(text = entry_str + '_')
    counter.config(text = '1000')
    button_ClearText.config(state = DISABLED)
    button_UndoReset.config(state = NORMAL)
        
    return


def undo_reset():               # undo text reset

    global entry_str, deleted_entry, entry_length, deleted_length, scramble_status

    if scramble_status: return

    if deleted_length:
        entry_str = deleted_entry
        deleted_entry = ''
        entry_length = deleted_length
        deleted_length = 0
        scramble_status = False
        screen_Live.config(text = entry_str + '_')
        counter.config(text = str(1000-entry_length))
        button_UndoReset.config(state = DISABLED)
        button_ClearText.config(state = NORMAL)
    
    return


def en_code():                  # encode text using 4-digit key

    global encode_flag, entry_str

    if not entry_str:
        tkMessageBox.showwarning('No message', 'Nothing to encode.')
        screen_Live.focus_force()
        return

    if not key:
        tkMessageBox.showwarning('No key', 'Enter encode-decode key.')
        set_key()
        en_code()
        screen_Live.focus_force()
        return

    if encode_flag:
        tkMessageBox.showwarning('Can\'t encode', 'Message is already encrypted.')
        screen_Live.focus_force()
        return

    encode_flag = True

    convert_lst = [None] * len(entry_str)

    for x in range (0, 4):
        for y in range (x, len(entry_str), 4):
            val = ord(entry_str[y:y+1])
            
            if 65 <= val <= 90:
                val = val + int(key[x:x+1])
                if val > 90: val -= 26
                convert_lst[y:y+1] = chr(val)
                
            if 97 <= val <= 122:
                val = val + int(key[x:x+1])
                if val > 122: val -= 26
                convert_lst[y:y+1] = chr(val)

            if val < 65 or (90 < val < 97) or val > 122:
                convert_lst[y:y+1] = chr(val)

    entry_str = ''.join(convert_lst)
    screen_Live.config(text = (entry_str + '_'))

    root.update()

    tkMessageBox.showinfo('Encode.', 'Done.')

    update_display()
    
    return


def de_code():                  # decode text using 4-digit key

    global encode_flag, entry_str

    if not entry_str:
        tkMessageBox.showwarning('No message', 'Nothing to decode.')
        screen_Live.focus_force()
        return

    if not key:
        tkMessageBox.showwarning('No key', 'Enter encode-decode key.')
        set_key()
        de_code()
        screen_Live.focus_force()
        return

    if not encode_flag:
        tkMessageBox.showwarning('Can\'t decode', 'Message is already decrypted.')
        screen_Live.focus_force()
        return

    encode_flag = False

    convert_lst = [None] * len(entry_str)

    for x in range (0, 4):
        for y in range (x, len(entry_str), 4):
            val = ord(entry_str[y:y+1])
            
            if 65 <= val <= 90:
                val = val - int(key[x:x+1])
                if val < 65: val += 26
                convert_lst[y:y+1] = chr(val)
                
            if 97 <= val <= 122:
                val = val - int(key[x:x+1])
                if val < 97: val += 26
                convert_lst[y:y+1] = chr(val)

            if val < 65 or (90 < val < 97) or val > 122:
                convert_lst[y:y+1] = chr(val)

    entry_str = ''.join(convert_lst)
    screen_Live.config(text = (entry_str + '_'))

    root.update()

    tkMessageBox.showinfo('Decode.', 'Done.')

    update_display()

    return


def scramble_text():            # randomly scramble the text or unscramble it

    global scramble_status, entry_length

    if scramble_status == False and entry_length:

        scramble_status = True
        scrambled_str = ''
        random_number = 0

        for x in entry_str:     # NOT: for x in range (0, len(entry_str)):
            random_number = random.randint(1, 10)
            val = ord(x)        # NOT: val = ord(entry_str[x:x+1])

            if 97 <= val <= 122:
                new_val = val + random_number
                if new_val > 122:
                    new_val = val - random_number
                scrambled_str += chr(new_val)

            elif 65 <= val <= 90:
                new_val = val - random_number
                if new_val < 65:
                    new_val = val + random_number
                scrambled_str += chr(new_val)

            else:
                scrambled_str += chr(val)
        
            screen_Live.config(text = scrambled_str + '_')
            display_ScrambleState.config(text = 'Scramble ON')
            display_ScrambleState.place(x = 120, y = 330)

    else:

        scramble_status = False
        screen_Live.config(text = entry_str + '_')
        display_ScrambleState.place_forget()

    return


def save_text():                # save text and key to file

    global filepath

    if key == '':
        tkMessageBox.showinfo('No key', 'Enter encode-decode key before saving.')
        set_key()
        save_text()

    if encode_flag:
        flag = '<+>'
    else:
        flag = '<->'

    filename = asksaveasfilename(initialdir = '/Users/Shared/', title = 'Select File',
                                 filetypes = (('Text files', '*.txt'), ('All files','*.*')))
    if filename:
        filepath = filename
        filename = ''

        textfile = open(filepath, 'w', 0)
        textfile.write(entry_str + '<?>' + flag + key)

        tkMessageBox.showinfo('Saved', 'File saved.')

    update_display()

    return


def open_file():                # open saved file

    global filepath, entry_length, entry_str, key, deleted_entry, deleted_length, encode_flag

    filename = askopenfilename(initialdir = '/Users/Shared/', title = 'Select File',
                               filetypes = (('Text files', '*.txt'),('All files','*.*')))
    if filename:
        deleted_entry = entry_str
        entry_str = ''
        deleted_length = entry_length
        entry_length = 0
        encode_flag = False

        button_ClearText.config(state = DISABLED)
        button_UndoReset.config(state = NORMAL)
        
        filepath = filename
        filename = ''
        textfile = open(filepath, 'r')
        entry_str = (textfile.read())

        entry_length = 0
        
        for x in entry_str:     # NOT: for x in range (0, len(entry_str)):
            if x == '\n':       # NOT: if entry_str[x:x+1] == '\n':
                entry_length += (70 - (entry_length%70))
            else:
                entry_length +=1

        if entry_str[-7:-4] == '<+>':
            encode_flag = True

        if entry_str[-10:len(entry_str)-4] == '<?><+>' or entry_str[-10:len(entry_str)-4] == '<?><->':
            key = entry_str[-4:]
            entry_str = entry_str[:-10].rstrip()

        buttons('on')
        button_UndoReset.config(state = DISABLED)
        display_Key.config(text = 'Key: %s' %key)
        counter.config(text = (1000-entry_length))
        screen_Live.config(text = entry_str + '_')
        root.update()

        if encode_flag:
            q = tkMessageBox.askquestion('Encrypted File', 'Encrypted file.\n\nDecode?')
            if q == 'yes':
                de_code()
                root.update()
                q = tkMessageBox.askquestion('Done', 'Delete encrypted file?')
                if q == 'yes':
                    os.remove(filepath)
                    tkMessageBox.showinfo('Deleted', 'Encrypted file deleted.')
                screen_Live.focus_force()
                return

        if not encode_flag:
            tkMessageBox.showinfo('Unencrypted File', 'File is not encrypted.')

    update_display()
    
    return


def quit_destroy():             # quit application
    
    quit_str = tkMessageBox.askquestion('Quit', 'Are you sure you\'d like to quit?')
    if quit_str == 'yes':
        root.destroy()
        exit()
        
    return


# GUI WIDGETS

#fonts & colours
TextFont1 = ('Menlo', 17)
ButtonFont1 = ('Helvetica Neue', 18)
CounterFont = ('Helvetica Neue', 14, 'bold')
Statusfont = ('Helvetica Neue', 14)
LogoFont = ('Helvetica Neue', 42, 'bold', 'italic')
bkgd = 'gainsboro'
frgd = 'black'
flash = 'red'

#window
root = Tk()
root.title('*NCRYPT2_ Encode-Decode Machine')
root.geometry('770x600+250+100')
root.resizable(0,0)
root.config(background=bkgd)

#button & key master coordinates
bcx = 515 
bcy = 380 
ncx = 302 
ncy = 378 

#buttons    
button_StartMachine = Button(root, font = ButtonFont1, text = 'Power', bg = bkgd, fg = frgd, command = on_off)
button_StartMachine.place(x = 10, y = bcy, width = 120, height = 45)
button_Scramble=Button(root, font = ButtonFont1, text = 'Scramble', bg = bkgd, fg = frgd, command = scramble_text)
button_Scramble.place(x = 10, y = bcy + 51, width = 120, height = 45)
button_ClearText=Button(root, font=ButtonFont1, text='Reset', bg=bkgd, fg=frgd, command=reset_text)
button_ClearText.place(x = bcx, y = bcy, width = 120, height = 45)
button_UndoReset = Button(root, font = ButtonFont1, text = 'Undo', bg = bkgd, fg = frgd, command=undo_reset)
button_UndoReset.place(x = bcx + 125, y = bcy, width = 120, height = 45)
button_Setkey = Button(root, font = ButtonFont1, text = 'Key', bg = bkgd, fg = frgd, command=set_key)
button_Setkey.place(x = bcx, y = bcy + 51, width = 120, height = 45)
button_Encode = Button(root, font = ButtonFont1, text = 'Encode', bg = bkgd, fg = frgd, command=en_code)
button_Encode.place(x = bcx + 125, y = bcy + 51, width = 120, height = 45)
button_OpenFile = Button(root, font = ButtonFont1, text = 'Open', bg = bkgd, fg = frgd, command=open_file)
button_OpenFile.place(x = bcx, y = bcy + 102, width = 120, height = 45)
button_Decode = Button(root, font = ButtonFont1, text = 'Decode', bg = bkgd, fg = frgd, command=de_code)
button_Decode.place(x = bcx + 125, y = bcy + 102, width = 120, height = 45)
button_SaveText = Button(root, font = ButtonFont1, text = 'Save', bg = bkgd, fg = frgd, command=save_text)
button_SaveText.place(x = bcx, y = bcy + 153, width = 120, height = 45)
button_Quit=Button(root, font = ButtonFont1, text = 'Quit', bg = bkgd, fg = frgd, command=quit_destroy)
button_Quit.place(x = bcx + 125, y = bcy + 153, width = 120, height = 45)
buttons('off')

#numeric keypad
button1=Button(root, font = ButtonFont1, text = '1', bg = bkgd, fg = frgd)
button1.place(x =  ncx, y = ncy, width = 66, height = 50)
button2=Button(root, font = ButtonFont1, text = '2', bg = bkgd, fg = frgd)
button2.place(x =  ncx + 66, y = ncy, width = 66, height = 50)
button3=Button(root, font = ButtonFont1, text = '3', bg = bkgd, fg = frgd)
button3.place(x =  ncx + 132, y = ncy, width = 66, height = 50)
button4=Button(root, font = ButtonFont1, text = '4', bg = bkgd, fg = frgd)
button4.place(x =  ncx, y = ncy + 50, width = 66, height = 50)
button5=Button(root, font = ButtonFont1, text = '5', bg = bkgd, fg = frgd)
button5.place(x =  ncx + 66, y = ncy + 50, width = 66, height = 50)
button6=Button(root, font = ButtonFont1, text = '6', bg = bkgd, fg = frgd)
button6.place(x =  ncx + 132, y = ncy + 50, width = 66, height = 50)
button7=Button(root, font = ButtonFont1, text = '7', bg = bkgd, fg = frgd)
button7.place(x =  ncx, y = ncy + 100, width = 66, height = 50)
button8=Button(root, font = ButtonFont1, text = '8', bg = bkgd, fg = frgd)
button8.place(x =  ncx + 66, y = ncy + 100, width = 66, height = 50)
button9=Button(root, font = ButtonFont1, text = '9', bg = bkgd, fg = frgd)
button9.place(x =  ncx + 132, y = ncy + 100, width = 66, height = 50)
button0=Button(root, font = ButtonFont1, text = '0', bg = bkgd, fg = frgd)
button0.place(x =  ncx + 66, y = ncy + 150, width = 66, height = 50)
buttonX = Button(root, font = ButtonFont1, text = '<', bg = bkgd, fg = frgd)
buttonX.place(x =  ncx + 132, y = ncy + 150, width = 66, height = 50)
nums('off')

button_Phantom = Button(root, command=key_entry)
button_Phantom.place(x = 638, y = ncy + 150, width = 0, height = 0)
button_Phantom.configure(state = DISABLED)

#text-entry frame & logo
screen_Frame=Frame(root, bg = frgd)
screen_Frame.place(x = 10, y = 10, width = 750, height = 350)
screen_Live = Label(root, bg = frgd, fg = bkgd, wraplength = 725, justify = LEFT)
screen_Live.config(font = TextFont1, text = '_')
screen_Live.place(x = 25, y = 20)
Logo = Label(text = '*ncrypt^2_', font = LogoFont, bg = bkgd, fg = 'darkgrey')
Logo.place(x = 10, y = ncy + 150)
counter = Label(font = CounterFont, bg = frgd, fg = 'yellow')
counter.place(x = 715, y = 330)

# text entry bind
screen_Live.focus_force()
screen_Live.bind('<Key>', read_keys)

#status display
display_PowerState = Label(root, text = 'Power %s' %status, font = CounterFont, bg = frgd, fg = bkgd)
display_PowerState.place(x = 25, y = 330)
display_KeyEntry = Label(root, font = CounterFont, bg = frgd, fg = 'yellow')
display_KeyEntry.place(x = 600, y = 330)
display_Key = Label(root, text = 'Key: %s' %key, font = CounterFont, bg = frgd, fg = bkgd)
display_Key.place(x = 600, y = 330)
display_Filepath = Label(root, text = 'File: %s' %filepath, font = CounterFont, bg = frgd, fg = bkgd)
display_Filepath.place(x = 230, y = 330)
display_ScrambleState = Label(root, font = CounterFont, bg = frgd, fg = 'yellow')
display_ScrambleState.place(x = 120, y = 330)

root.mainloop()
