"""

Initial code take from tutorial on zetcode.com:
zetcode.com/gui/tkinter/layout/

"""

import os
import time

import sys

from PIL import Image, ImageTk
from Tkinter import Tk, N,S,W,E, Label, BOTH, RIGHT, RAISED, LEFT
from Tkinter import TOP, BOTTOM, Menu
import tkMessageBox
from ttk import Frame, Style, Button
from ttk import Entry

from gui_helper import take_snapshot, run_pupil


sys.path.insert(0, '..')
from facepp.face_plus_plus import facial_detection, compare, add_face
from facepp.train_groups import update_group

test_mode = False
comparison_directory = "CSE_481_photos"
update_group(comparison_directory, comparison_directory)
WIDGETS = {}
class Example(Frame):
    def onExit(self):
        self.quit()
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()

    def initUI(self):
      #global test_mode
      if not test_mode:
        run_pupil()

      #  Defining a method for absolute positioning of an image
      def place_img(self, filename, x, y):
        img = Image.open(filename)
        img = ImageTk.PhotoImage(img)
        lbl1 = Label(self, image=img)
        lbl1.image = img
        lbl1.place(x=x, y=y)

      def clear_frame(frame):
        for child in frame.winfo_children():
          child.destroy()

      def clear_panel(panel):
        for match_label in panel['match_labels']:
          match_label['text'] = ''
        for pic_frame in panel['match_pics']:
          clear_frame(pic_frame)
        clear_frame( panel['left_pic'] )
        panel['left_pic_label']['text'] = ''

      #  Defining a method for framewise positioning of an image
      # @params
      #   frame   the frame to attach filename to
      def insert_img(self, filename, frame, pic_path, label):
        # First, remove anything currently in the frame
        for child in frame.winfo_children():
          child.destroy()
        sizeY = frame.winfo_height()
        sizeX = frame.winfo_width()
        img = Image.open(filename)
        img = img.resize((sizeY, sizeX), Image.ANTIALIAS)
        # Subtract 8 for various borders in the frame.
        img = img.resize((sizeX-8, sizeY-8), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        lbl1 = Label(frame, image=img)

        def save_image(event):
          global comparison_directory
          folder = "../face_comparison/%s/%s" %(comparison_directory,label)
          os.system("ls " + folder + " | wc -l > output.txt")
          f = open("output.txt", 'r')
          file_number = str(int(f.readline().rstrip().lstrip()) + 1)
          command = "cp " + pic_path + " " + folder + "/" +  file_number + ".jpg"
          add_face(pic_path, label)
          
          print command
          os.system(command)

        lbl1.image = img
        lbl1.bind('<Button-1>', save_image)
        lbl1.setvar('pic', pic_path)
        lbl1.setvar('label', label)
        lbl1.place(x=frame.winfo_x(), y=frame.winfo_y())

      self.parent.title("Student Name Recollection Helper")
      #self.pack(fill=BOTH, expand=1)

      menubar = Menu(self.parent)
      self.parent.config(menu=menubar)
  
      fileMenu = Menu(menubar)

      submenu = Menu(fileMenu)
      classes = get_dir_names()
      for cls in classes:
        #  This nesting is sort of weird, but is necessary. 
        def make_fn(x):
          def fn():
            global comparison_directory
            comparison_directory = x
            update_group(comparison_directory, comparison_directory)
          return fn
        submenu.add_command(label=cls, command = make_fn(cls))
          
      fileMenu.add_cascade(label='Choose Class', menu=submenu, underline=0)
      fileMenu.add_separator()
      fileMenu.add_command(label="Exit", command=self.onExit)
      menubar.add_cascade(label="File", menu=fileMenu)

      style = Style()
      style.configure("TButton", padding=(0, 5, 0, 5), 
                      font='serif 10')
      style.configure("TFrame", background="#333")        
      style.configure("TLabel", background="#333")        

      self.columnconfigure(0,pad=10, minsize=650, weight=1)
      self.columnconfigure(1,pad=10)
      self.rowconfigure(0,pad=10, minsize=500, weight=1)
      self.rowconfigure(1,pad=10, weight=1)

      self.pack()

      def other():
        print "Not implemented"

      # Top box
      upper_frame = Frame(self, relief=RAISED )
      upper_frame.grid(row = 0, column = 0, columnspan=2, sticky=N+E+S+W)

      # Creates a panel in the frame passed in, and returns a list of frame objects
      #  that need to be accessed in the panel
      def save_image(event):
        print event.widget
        print "save_image!!!"
        
        folder = "../face_comparison/" + comparison_directory + "/" + \
              event.widget.getvar('label')
        os.system("ls " + folder + " | wc -l > output.txt")
        f = open("output.txt", 'r')
        file_number = str(int(f.readline().rstrip().lstrip()) + 1)
        command = "cp " + event.widget.getvar('pic') + " " + folder + "/" +  file_number + ".jpg"
        print command
        os.system(command)

      def make_panel(panel_frame):
        ### P1 is the main panel being made
        p1 = Frame(upper_frame, relief=RAISED, borderwidth =1)
        p1.pack(side = TOP, fill = BOTH, expand=1)

        pic_frame1 = Frame(p1, relief=RAISED, borderwidth =1)
        pic_frame1.pack(side = LEFT, fill = BOTH, expand=1,padx=15, pady=4)
        pic1 = Frame(pic_frame1, relief=RAISED, borderwidth =1)
        pic1.pack(side = TOP, fill = BOTH, expand=1)
        label1 = Label(pic_frame1, relief=RAISED, borderwidth =1, 
            text ="Captured face", width = 15)
        label1.pack(side = BOTTOM, fill = BOTH)

        info_panel = Frame(p1, relief=RAISED, borderwidth =1)
        info_panel.pack(side = LEFT, fill = BOTH, expand=1)
        bt = Label(info_panel, text="Best\nMatches:", background="#ececec")
        bt.pack(pady=20)

        match_pictures = []
        match_labels = []
        #  These are the tree matches in the panel
        for i in range(3):
          pic_frame = Frame(p1, relief=RAISED, borderwidth =1)
          pic_frame.pack(side = LEFT, fill = BOTH, expand=1,padx=15, pady=4)
          pic = Frame(pic_frame, relief=RAISED, borderwidth =1)
          pic.pack(side = TOP, fill = BOTH, expand=1)
          #pic.bind('<Button-1>', save_image)
          match_pictures.append(pic)
          label = Label(pic_frame, relief=RAISED, borderwidth =1, 
              text = "Match %d"%(i+1), width=15)
          label.pack(side = BOTTOM, fill = BOTH)
          match_labels.append(label)


        return {"left_pic":pic1, "left_pic_label":label1,  "match_pics":match_pictures, 
                                "match_labels":match_labels}

      #  make 3 panels
      panel_data = []
      panel_data.append( make_panel(upper_frame) )
      panel_data.append( make_panel(upper_frame) )
      panel_data.append( make_panel(upper_frame) )

      def capture():
        coord = []
        if not test_mode:
          pic_file, coord = take_snapshot()
          pic_file = os.path.abspath(pic_file)
        else:
          pic_file = sys.argv[1]
          if len(sys.argv) >= 4:
            coord = [float(sys.argv[2]), float(sys.argv[3])]
          else:
            coord = [0.5,0.5]

        if len(coord) == 0:
          tkMessageBox.showwarning("Error",
                "Pupil device failed to capture gaze.")

        else:
          im=Image.open(pic_file)
          im.size # (width,height) tuple
          coord[0] = int(float(coord[0]) * im.size[0])
          coord[1] = int(float(coord[1]) * im.size[1])
          print "file name " + pic_file
          faces = facial_detection(pic_file, coord[0], coord[1])
          print "length of faces"
          print len(faces)
          print "faces"
          print faces
          associated_matches = {}
          if len(faces) == 0:
            tkMessageBox.showwarning("Error",
                "No faces were found.")

          for face in faces:
            print "comparison directory"
            print comparison_directory
            #get the top three matches for each face
            associated_matches[face['path']] = compare( face, 
                   comparison_directory)

          index = -1
          for index, face in enumerate(faces):
            #get the top three matches for each face
            face_matches = associated_matches[face['path']]
            panel = panel_data[index]
            #place the captured face in the panel
            insert_img(self, face['path'], panel['left_pic'], face['path'], "")
            panel['left_pic_label']['text'] = "Captured face"
            j = -1
            for j, match in enumerate(face_matches):
              #place the matches in the panel
              panel['match_labels'][j]['text'] = match['id'].replace('_',' ')
              insert_img(self, match['match_path'], panel['match_pics'][j], face['path'], match['id'])
            # Clear the non-match frames
            for k in range(j+1, len(panel['match_pics'])):
              clear_frame( panel['match_pics'][k]  )
              panel['match_labels'][k]['text'] = "No more matches"
          # Clear the non-match panels
          for k in range(index+1, len(panel_data)):
            clear_panel(panel_data[k])
          if index == -1:
            panel_data[0]['left_pic_label']['text'] = "No faces detected"


      def key(event):
        # 'Enter' key triggers capture.
        if event.char == '\r':
          capture()

      # Bind to parent, so that the focus never leaves it. 
      self.parent.focus_set()
      self.parent.bind('<Key>', key)

      ent_msg = Label(self, text="Press Enter to capture gaze. Click on a matching face to add the captured face to the daset of the match.", background="#ececec")
      ent_msg.grid(row=1,column=0)

      # Some weird hack to bring this window to the front as it is launched. 
      #  Won't work on windows.
      if os.name == "posix":
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
      

# Returns the names of the classes (directories) that might contain
#  photos for comparison. 
def get_dir_names():
  contents = os.listdir("../face_comparison")
  return filter(lambda x: os.path.isdir("../face_comparison/" + x), contents)

def exit_function():
  f = open("../pupil/pupil_src/capture/pic/quit.txt", 'w') 
  f.write("quit")
import atexit
atexit.register(exit_function)

def main():
  root = Tk()
  app = Example(root)
  root.mainloop()  

def removeQuit(): 
  os.system("rm ../pupil/pupil_src/capture/pic/quit.txt")
  os.system("touch ../pupil/pupil_src/capture/pic/quit.txt")
if __name__ == '__main__':
  if len(sys.argv) > 1:
    test_mode = True
  removeQuit()#need to make sure quit file is gone!
  main()  

