#!/usr/bin/python
# Python GUI module
import Tkinter
import Tkconstants
import tkFileDialog
import tkMessageBox

class TkOpenFileDialog(Tkinter.Frame):
    def __init__(self, root, label_txt = 'Input file:', button_txt = 'Choose File', defaultextension = '.txt', filetypes = [('text files', '.txt')], initialdir = 'C:\\'):
        '''
        Sets up the widgets for this FileDialog        
        '''
        
        Tkinter.Frame.__init__(self, root)
        # options for buttons
        common_opt = {'fill': Tkconstants.BOTH, 'padx': 40, 'pady': 5}
        
        # define widgets
        self.label = Tkinter.Label(root, text=label_txt)
        self.label.pack(common_opt)
        self.entry = Tkinter.Entry(root, bd =5)
        self.entry.pack(common_opt)
        self.button = Tkinter.Button(self, text=button_txt, command=self.askopenfilename).pack(**common_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = defaultextension
        options['filetypes'] = filetypes
        options['initialdir'] = initialdir
        options['parent'] = root
        options['title'] = 'File Selection'

    def askopenfilename(self):
        '''        
        Dialog filename and the filename is set in the entry widget.
        '''

        # get filename
        filename = tkFileDialog.askopenfilename(**self.file_opt)

        # open file on your own
        if filename:      
            self.entry.delete(0)
            self.entry.insert(0, filename)
            
class GuiManager():
    def __init__(self, syncBtnCallBack):
        self.root = Tkinter.Tk()
    
        # Properties
        self.root.geometry("470x350")
        self.root.title("SubSync - Automatic Subtitle Synchronizer")
        self.root.resizable(0,0)
        
        # Code to add widgets will go here
        self.video_file_dialog = TkOpenFileDialog(self.root, label_txt = "Video input file:", defaultextension = '.avi', filetypes = [('Audio Video Interleave', '.avi')])
        self.video_file_dialog.pack()
        self.subtitle_file_dialog = TkOpenFileDialog(self.root, label_txt = "Subtitle input file:", defaultextension = '.srt', filetypes = [('SubRip text file', '.srt')])
        self.subtitle_file_dialog.pack()
        self.btn_syn = Tkinter.Button(self.root, text ="Synchronize subtitle", command = syncBtnCallBack, bg = '#ffc2b3')
        self.btn_syn.pack({'fill': Tkconstants.BOTH, 'padx': 100, 'pady': 25})
        self.GenerateMenuBar()
        
    def RunSubSyncGuiMainLoop(self):
        # Kick off the main loop
        self.root.mainloop()
        
    def DisplayPromptMsg(self, window_name = "Prompt", message_txt = "Message"):
        tkMessageBox.showinfo(window_name, message_txt)
        
    def GenerateMenuBar(self):
        
        def donothing():
            self.DisplayPromptMsg(message_txt = "Under Implementation")
            
        def ShowAbout():
            self.about_window = Tkinter.Toplevel()
            self.about_window.geometry("400x400")
            self.about_window.transient(self.root)
            self.about_window.grab_set()
            self.root.wait_window(about_window)
            
        menubar = Tkinter.Menu(self.root)
        
        filemenu = Tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Synchronization", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        
        menubar.add_cascade(label="File", menu=filemenu)
        
        editmenu = Tkinter.Menu(menubar, tearoff=0)        
        editmenu.add_command(label="Language Options", command=donothing)
        editmenu.add_command(label="Parameter Tuning", command=donothing)
        
        menubar.add_cascade(label="Configuration", menu=editmenu)
        
        helpmenu = Tkinter.Menu(menubar, tearoff=0)        
        helpmenu.add_command(label="User Manual", command=donothing)
        helpmenu.add_command(label="About SubSync", command=ShowAbout)
        
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)