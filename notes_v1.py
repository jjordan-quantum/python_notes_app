from tkinter import *
import tkinter.font as tkfont
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pathlib, os

class MyApp:
	def __init__(self, parent):

		self.myParent = parent 

		self.myParent.title("Notes")

		self.current_note = ""

		self.title_saved = False

		self.note_saved = False

		self.bg_color = "thistle3"
		self.text_area_color = "thistle1"

		self.notes = []
		self.notes_frame_labels = []
		self.extension = '.txt'
		
		# Menus
		self.menubar = Menu(self.myParent)

		self.menu_file = Menu(self.menubar, tearoff=0)
		self.menu_file.add_command(label="New", command=self.new) # TODO - command
		self.menu_file.add_command(label="Open", command=self.do_nothing) # TODO - remove?
		self.menu_file.add_command(label="Save", command=self.save_note) # TODO - command
		self.menu_file.add_command(label="Save As", command=self.do_nothing) # TODO - change to copy note
		self.menu_file.add_command(label="Close", command=self.exit_app) # TODO - command
		self.menu_file.add_separator()
		self.menu_file.add_command(label="Exit", command=self.exit_app) # TODO - command

		self.menu_edit = Menu(self.menubar, tearoff=0)
		self.menu_edit.add_command(label="Undo", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Redo", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Cut", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Copy", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Paste", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Delete", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Select All", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Find", command=self.do_nothing) # TODO - command
		self.menu_edit.add_command(label="Replace", command=self.do_nothing) # TODO - command

		self.menu_settings = Menu(self.menubar, tearoff=0)
		self.menu_settings.add_command(label="Themes", command=self.do_nothing) # TODO - command
		self.menu_settings.add_command(label="Tabs", command=self.do_nothing) # TODO - command
		self.menu_settings.add_command(label="Highlighting", command=self.do_nothing) # TODO - command
		self.menu_settings.add_command(label="Extensions", command=self.do_nothing) # TODO - command
		self.menu_settings.add_command(label="Cloud", command=self.do_nothing) # TODO - command

		self.menubar.add_cascade(label="File", menu=self.menu_file)
		self.menubar.add_cascade(label="Edit", menu=self.menu_edit)
		self.menubar.add_cascade(label="Settings", menu=self.menu_settings)

		self.myParent.config(menu=self.menubar) # Add menu bar to window

		# Top level frame - paned
		self.top_frame = PanedWindow(self.myParent) 
		self.top_frame.pack(fill=BOTH, expand=1)  

		# Left frame - paned - add(left)
		self.left_frame = PanedWindow(
			self.top_frame, 
			orient=HORIZONTAL,
			bg=self.bg_color, 
		)
		self.top_frame.add(self.left_frame, sticky="ns", minsize=500)
		#self.left_frame.add(side=LEFT, fill=Y, expand=1)

		# Folders frame - add(left)
		self.folders_frame = Frame(
			self.left_frame,
			bg=self.bg_color,
			borderwidth=5,
			relief=RIDGE,
			width=250,
		)
		self.folders_frame.pack_propagate(False)
		self.left_frame.add(self.folders_frame, minsize=250)
		#self.folders_frame.add(left, fill=Y, expand=NO, minsize=200)
		
		# Notes frame - add(right)
		self.notes_frame = Frame(
			self.left_frame,
			bg=self.bg_color,
			borderwidth=5,
			relief=RIDGE,
			width=250,
		)
		self.notes_frame.pack_propagate(False)
		self.left_frame.add(self.notes_frame, minsize=250)
		#self.notes_frame.add(right, fill=Y, minsize=200)

		"""
		self.test_frame = Frame(self.notes_frame, bg="white", width=100, height=10)
		self.test_frame.pack(side=TOP)

		self.button1 = Button(self.notes_frame, text="Button 1", width=100)
		self.button1.pack(side=TOP, padx=2, pady=1)

		self.button2 = Button(self.notes_frame, text="Button 2", width=100)
		self.button2.pack(side=TOP, padx=2, pady=1)
		"""
		

		# Right frame - add(right)
		self.right_frame = Frame(
			self.top_frame, 
			background=self.bg_color,
			borderwidth=5,  
			relief=RIDGE,
			width=800,
		)
		self.top_frame.add(self.right_frame, sticky="nsew")
		#self.right_frame.add(right, fill=BOTH, expand=YES) 

		# Toolbar frame	
		self.toolbar_frame = Frame(self.right_frame, bg=self.bg_color, height=40)
		self.toolbar_frame.pack(side=TOP, fill=X, expand=NO)
		self.toolbar_frame.pack_propagate(False)

		self.new_note_button = Button(self.toolbar_frame, text="+")
		self.copy_note_button = Button(self.toolbar_frame, text="C")
		self.delete_note_button = Button(self.toolbar_frame, text="X")
		#self.rename_note_button = Button(self.toolbar_frame, text="_")

		self.new_note_button.pack(side=LEFT)
		self.copy_note_button.pack(side=LEFT)
		self.delete_note_button.pack(side=LEFT)
		#self.rename_note_button.pack(side=LEFT)

		self.new_note_button.bind("<Button-1>", self.on_new_note_button_click)
		self.delete_note_button.bind("<Button-1>", self.on_delete_note_button_click)
		self.copy_note_button.bind("<Button-1>", self.on_copy_note_button_click)

		# Text frame
		self.text_frame = Frame(self.right_frame, bg=self.bg_color, height=400)
		self.text_frame.pack(side=TOP, fill=BOTH, expand=YES)
		self.text_frame.pack_propagate(False)

		self.title_frame = Frame(self.text_frame)
		self.title_frame.pack(side=TOP, fill=X)

		self.update_title_button = Button(self.title_frame, text="Update Title")
		self.update_title_button.pack(side=LEFT)
		self.update_title_button.bind("<Button-1>", self.on_update_title_button_clicked)

		self.title_field = Entry(self.title_frame, bg=self.text_area_color)
		self.title_field.pack(side=LEFT, fill=X, expand=YES)
		self.title_field.bind("<Key>", self.on_title_field_key_press)

		self.text_area = Text(
			self.text_frame,	
			borderwidth=2,
			relief=RIDGE,
			height=100,
			bg=self.text_area_color
		)
		self.text_area.pack(side=TOP, fill=X)
		self.text_area.bind("<Key>", self.on_text_area_key_press)

		font = tkfont.Font(font=self.text_area['font'])  # get font associated with Text widget
		tab_width = font.measure(' ' * 4)  # compute desired width of tabs
		self.text_area.config(tabs=(tab_width,))  # configure Text widget tab stops		

		# Status frame
		self.status_frame = Frame(self.right_frame, bg="white", borderwidth=2, relief=RIDGE, height=20)
		self.status_frame.pack(side=TOP, fill=X, expand=NO)

		# Clears text from buffer
		self.clear_text()

		# populating notes to notes_frame and load note to text area:
		self.load_notes()


		#-----------------------------------------------------------
		# TESTING:
		"""
		text = ''
		for note in self.notes:
			text = text + str(note) + '\n'
		self.load_text(text)
		"""

		#------------------------------------------------------------

	def do_nothing(self):
		# place holder function
		a = 1 + 1

	# Deprecated
	"""
	def open_file(self):
		# Open a file for editing
		filepath = askopenfilename(
			filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
		)
		if not filepath:
			return
		self.text_area.delete("1.0", END)
		with open(filepath, "r") as input_file:
			text = input_file.read()
			self.text_area.insert(END, text)
		self.update_title(filepath)
		self.file_saved = True

	def save_as(self):
		# Save the current file as a new file
		filepath = asksaveasfilename(
			defaultextension=".txt",
			filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
		)
		if not filepath:
			return
		with open(filepath, "w") as output_file:
			text = self.text_area.get("1.0", END)
			output_file.write(text)
		self.update_title(filepath)
		self.file_saved = True

	def save_file(self):
		if not self.file_saved:
			self.save_as()
			return
		with open(self.filename, "w") as output_file:
			text = self.text_area.get("1.0", END)
			output_file.write(text)
		self.file_saved = True
	"""

	def clear_text(self):
		self.text_area.delete("1.0", END)

	def load_text(self, text):
		self.clear_text()
		self.text_area.insert(END, text)

	def get_text(self):
		return self.text_area.get("1.0", END)

	def new(self):
		self.save_note()
		self.text_area.delete("1.0", END)
		new_name = "Untitled"
		while (new_name in self.notes):
			new_name = new_name + " (copy)"
		self.update_title(new_name)
		self.current_note = new_name
		self.note_saved = False
		self.save_note()
		self.populate_notes()

	def save_note(self):
		if not self.note_saved:
			with open(self.current_note+self.extension, "w") as output_file:
				text = self.get_text()
				output_file.write(text)
			self.note_saved = True

	def exit_app(self):
		self.save_note()
		self.myParent.destroy()

	def update_title(self, new_title):
		self.title_field.delete(0,"end")
		self.title_field.insert(0, new_title)
		self.title_saved = True

	# Get list of notes in cwd:
	def get_notes(self):
		self.notes = []
		currentDir = pathlib.Path('.')
		for item in currentDir.iterdir():
			if not item.is_dir() and self.extension in str(item):
				self.notes.append(str(item)[:-4])

	# Add list of notes to notes_frame as labels:
	def add_notes(self):
		for child in self.notes_frame.winfo_children():
			child.destroy()

		self.notes_frame_labels = []

		for note in self.notes:
			self.notes_frame_labels.append(Label(self.notes_frame, text=note, fg='black', bg='white'))

		for note_label in self.notes_frame_labels:
			note_label.pack(side=TOP, padx=2, pady=1, fill=X)
			note_label.bind("<Enter>", self.on_enter_note)
			note_label.bind("<Leave>", self.on_leave_note)
			note_label.bind("<Button-1>", self.on_click_note)
			note_label.bind("<ButtonRelease-1>", self.on_release_note)
		
		Label(self.notes_frame, height=100, bg='white').pack(side=TOP, padx=2, pady=1, fill=BOTH, expand=True)


	# Populate note_frame
	def populate_notes(self):
		self.get_notes()
		self.add_notes()

	# change bg of note on mouse-over (<Enter> event):
	def on_enter_note(self, event):
		event.widget.configure(bg='blue')

	# change bg of note on mouse-leave (<Leave> event):
	def on_leave_note(self, event):
		event.widget.configure(bg='white')

	# change bg of note on mouse-click (<Button-1> event):
	def on_click_note(self, event):
		event.widget.configure(bg='red')
		self.save_note()
		self.load_note(event.widget['text'])

	# change bg of note on mouse-release (<ButtonRelease-1> event):
	def on_release_note(self, event):
		event.widget.configure(bg='blue')

	# load note from label clicked
	def load_note(self, notename):
		with open(notename+self.extension, "r") as input_file:
			text = input_file.read()
			self.load_text(text)
		self.current_note = notename
		self.update_title(notename)
		self.note_saved = True

	# action for text area key pressed (<Key>):
	def on_text_area_key_press(self, event):
		self.note_saved = False

	# action for update title button pressed (<Button-1>):
	def on_update_title_button_clicked(self, event):
		if not self.title_saved:
			self.delete_current_note()
			self.current_note = self.title_field.get()
			while(self.current_note in self.notes):
				self.current_note = self.current_note + " (alt)"
			self.note_saved = False
			self.save_note()
			self.title_field.configure(bg=self.text_area_color)
			self.populate_notes()
			self.title_saved = True

	# action for title field key pressed (<Key>):
	def on_title_field_key_press(self, event):
		event.widget.configure(bg='yellow')
		self.title_saved = False

	# action for clicking new note button (<Button-1>):
	def on_new_note_button_click(self, event):
		self.new()

	# action for clicking delete note button (<Button-1> event):
	def on_delete_note_button_click(self, event):
		self.delete_current_note()
		self.load_notes()

	# delete current note
	def delete_current_note(self):
		if os.path.exists(self.current_note+self.extension):
			os.remove(self.current_note+self.extension)

	# load notes into label list and load first note:
	def load_notes(self):
		self.populate_notes()
		if len(self.notes) == 0:  # CHECK THIS-------------------------------
			self.note_saved = True
			self.new()			
	
		else:
			self.load_note(self.notes[0])	
		
	# copy the current note
	def copy_note(self):
		self.save_note()
		while(self.current_note in self.notes):
			self.current_note = self.current_note + " (copy)"
		self.update_title(self.current_note)
		self.note_saved = False
		self.save_note()

	# action for clicking copy note button (<Button-1> event):
	def on_copy_note_button_click(self, event):
		self.copy_note()
		self.populate_notes()

		

root = Tk()
myapp = MyApp(root)
root.attributes("-zoomed", True) # Expand window to fill desktop
root.mainloop()
