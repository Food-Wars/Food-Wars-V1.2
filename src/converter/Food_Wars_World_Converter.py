# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 17:26:32 2025

"""
#import libraries
import tkinter as tk
from tkinter import filedialog, ttk, font
from PIL import ImageTk
import random
import os
#import files
import licenses
import image_storage
import Versions
import Conversions
#get tk imae from PIL image
def get_tk_image(PIL_image, label):
    tk_image = ImageTk.PhotoImage(PIL_image)
    label.image = tk_image
    label['image'] = tk_image
#list of flavour text phrases
flavour_text = ['Making Cotten Candy', 'Planting Trees', 'Refrigerating Gelatin', 'importing pygame', 'Wrangling Pythons', 'Weaving Sugercloth', 'Smashing Rocks']

#main class, inherites main window from tkinter
class Main(tk.Tk):
    def __init__(self):
        #intisalise parent class
        super().__init__()
        #add title
        self.title("Food Wars Converter")
        self.current_frame = None
        #add menu bar
        self.option_add('*tearOff', False)
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        menu_file = tk.Menu(menu_bar)
        #menu_help = tk.Menu(menu_bar)
        menu_file.add_command(label='Main Menu', command=lambda: self.new_page(Start_Page, 'center', font=label_font))
        menu_file.add_command(label='Exit Program', command=lambda: self.destroy())
        menu_bar.add_cascade(menu=menu_file, label='File')
        #menu_bar.add_cascade(menu=menu_help, label='Help')
        menu_bar.add_command(label='About', command=lambda: self.new_page(About_Page, 'n'))
        #get icon
        self.icon = ImageTk.PhotoImage(image_storage.icon_image)
        self.iconphoto(False, self.icon)
        #start maxamized
        self.state('zoomed')
    def new_page(self, new_frame, anchor, *args, **kwargs):
        if self.current_frame != None:
            self.current_frame.destroy()
        self.current_frame = new_frame(self, *args, **kwargs)
        self.current_frame.pack(anchor=anchor, expand=True)
#define app 
app = Main()
#page classes
class About_Page(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.about_label = ttk.Label(self, text='Food Wars Converter Version 1.0')
        self.about_label.pack()
        self.licenses_frame = ttk.Frame(self)
        self.pillow_text = ttk.Label(self.licenses_frame, text='Pillow-10.4.0:')
        self.pillow_text.grid(row = 0, column = 0)
        self.pillow_button = ttk.Button(self.licenses_frame, text='View License', command=lambda:self.view_license(licenses.licenses['pillow-10.4.0']))
        self.pillow_button.grid(row = 0, column = 1)
        self.licenses_frame.pack()
    def view_license(self, license_text):
        #create new window containing the license text
        license_window = tk.Toplevel(self.parent)
        license_window.title("License text")
        license_window.resizable(False, False)
        #have to finish with this window before going back to the main window
        license_window.grab_set()
        #add license text to the window
        license_label = ttk.Label(license_window, text=license_text)
        license_label.pack()
class Start_Page(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.font = kwargs['font']
        #get logo image
        self.logo_frame = ttk.Frame(self)
        self.logo_label = ttk.Label(self.logo_frame)
        get_tk_image(image_storage.logo_image, self.logo_label)
        self.logo_label['padding'] = 5
        self.logo_label.pack()
        self.converter_label = ttk.Label(self.logo_frame, text='CONVERTER')
        self.converter_label['font'] = self.font
        self.converter_label.pack()
        self.logo_frame.grid(row=1, column = 1, sticky="nsew")
        self.open_folder_button = ttk.Button(self, text='Open Folder', command=lambda:self.open_folder())
        self.open_folder_button.grid(row=2, column = 1, sticky="nsew")
    def open_folder(self):
        #get world directiory name, then move to folder loading frame
        directory_name = filedialog.askdirectory()
        if directory_name != '':
            self.parent.new_page(Load_Folder, 'center', directory_name=directory_name)
class Load_Folder(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.directory_name = kwargs['directory_name']
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=200, mode='indeterminate')
        self.progress_bar.start()
        self.progress_bar.pack()
        self.progress_label_text = tk.StringVar()
        self.progress_label = ttk.Label(self)
        self.progress_label['textvariable'] = self.progress_label_text
        self.progress_label_text.set('Retrieving Version...')
        self.progress_label.pack()
        #bind event to run if there is an error, or move to next page
        self.bind_all("<<Error_Loading_World>>", lambda event: self.error_occured())
        self.bind_all("<<World_Loaded>>", lambda event: self.parent.new_page(Select_New_Version, 'n', world=self.world, font=error_font))
        #schedule functions to run
        self.after(100, self.run_functions)
    def run_functions(self):
        #get version
        version = find_version(self.directory_name)
        #create version class
        if version == '1.1':
            self.world = Versions.Version_1_1(self.directory_name)
        else:
            self.world = Versions.Version_1_0(self.directory_name)
        self.progress_label_text.set('Retrieving Version... \n Loading Files...')
        self.load_files()
        self.progress_label_text.set('Retrieving Version... \n Loading Files... \n Building Workspace...')
    def load_files(self):
        #having this as a function allows to get a return from the used function
        self.world.load_files(self.parent)
    def error_occured(self):
        #self.parent.after_cancel(self.work_space_id)
        self.parent.new_page(Loading_Error, 'center', font=error_font)
class Loading_Error(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.error_font = kwargs['font']
        self.error_label = ttk.Label(self, text='There was an error loading the file. Sorry :(')
        self.error_label['font'] = self.error_font
        self.error_label.pack()
        self.menu_button = ttk.Button(self, text='Main Menu', command=lambda:self.parent.new_page(Start_Page, 'center', font=label_font))
        self.menu_button.pack()
class Select_New_Version(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.label_font = kwargs['font']
        self.select_label = ttk.Label(self, text='Select New Version:')
        self.select_label['font'] = self.label_font
        self.select_label.grid(row=0, column=0, columnspan=3)
        self.parent = parent
        self.world=kwargs['world']
        self.buttons = {}
        row_count = 1
        column_count = 0
        for version in Versions.versions:
            #skipping visual workspace; can't figure out making a map of the world. For these version, honestly probobly don't need to 
            self.buttons[version] = ttk.Button(self, text=version, command=lambda v=version: self.parent.new_page(Convert_World, 'center', version=v, world=self.world))
            self.buttons[version].grid(row = row_count, column = column_count)
            if column_count == 3:
                column_count = 0
                row_count += 1
            else:
                column_count += 1
        self.buttons[self.world.version].state(['disabled']) 
class Build_Workspace(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.new_version = kwargs['version']
        self.world = kwargs['world']
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=200, mode='indeterminate')
        self.progress_bar.start()
        self.progress_bar.pack()
        self.parent.after(100, self.build_workspace)
        self.bind_all("<<Workspace_Built>>", lambda event: self.parent.new_page(Adjust_World, 'center', version=self.new_version, world=self.world))
    def build_workspace(self):
        self.world.build_workspace(self.parent)
class Adjust_World(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.new_version = kwargs['version']
class Convert_World(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.new_version = kwargs['version']
        self.world = kwargs['world']
        self.flavour_text = tk.StringVar()
        self.flavour_label = ttk.Label(self)
        self.flavour_label['textvariable'] = self.flavour_text
        self.flavour_text.set(random.choice(flavour_text))
        #self.flavour_text.set(random.choice(flavour_text))
        self.flavour_label.pack()
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=200, mode='indeterminate')
        self.progress_bar.start()
        self.progress_bar.pack()
        self.progress_label_text = tk.StringVar()
        self.progress_label = ttk.Label(self)
        self.progress_label['textvariable'] = self.progress_label_text
        self.progress_label_text.set('Current version: ' + self.world.version)
        self.progress_label.pack()
        self.parent.after(100, self.convert_world)
        #bind event to detect when world is finished converting
        self.bind_all("<<Map_Converted>>", lambda event: self.check_world())
    def convert_world(self):
        self.flavour_changer_id = self.parent.after(60000, lambda: self.change_flavour_text())
        if self.world.version == '1.1':
            self.converter = Conversions.C_1_0_to_1_1.One_To_Zero(self.world)
            self.converter.get_chunk_keys()
            self.parent.after(100, lambda: self.converter.convert_main_items())
            self.parent.after(110, lambda: self.converter.run_map_conversion(self.parent))
        else:
            self.converter = Conversions.C_1_0_to_1_1.Zero_To_One(self.world)
            self.converter.get_chunk_keys()
            self.parent.after(100, lambda: self.converter.convert_main_items())
            self.parent.after(110, lambda: self.converter.convert_hotbar_items())
            self.parent.after(120, lambda: self.converter.convert_armour_items())
            self.parent.after(130, lambda: self.converter.convert_armour_items())
            self.parent.after(140, lambda: self.converter.run_map_conversion(self.parent))
    def check_world(self):
        #get converted world
        if self.world.version == '1.0':
            self.world = self.converter.output_class(Versions.Version_1_1)
        else:
            self.world = self.converter.output_class(Versions.Version_1_0)
        #check to see if it is the right version
        if self.world.version == self.new_version:
            self.parent.after_cancel(self.flavour_changer_id)
            self.parent.new_page(Save_World, 'center', world=self.world, font=label_font)
        else:
            self.progress_label_text.set('Current version: ' + self.world.version)
            self.flavour_changer_id = self.parent.after(60000, lambda: self.change_flavour_text())
    def change_flavour_text(self):
        self.flavour_text.set(random.choice(flavour_text))
        self.flavour_changer_id = self.parent.after(60000, lambda: self.change_flavour_text())
class Save_World(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.world = kwargs['world']
        self.font = kwargs['font']
        self.converter_label = ttk.Label(self, text='Save World:')
        self.converter_label['font'] = self.font
        self.converter_label.pack()
        #world number selector setup
        self.world_num = tk.StringVar()
        self.world_num.set('1')
        world_1 = ttk.Radiobutton(self, text='World 1', variable=self.world_num, value='1')
        world_1.pack()
        world_2 = ttk.Radiobutton(self, text='World 2', variable=self.world_num, value='2')
        world_2.pack()
        world_3 = ttk.Radiobutton(self, text='World 3', variable=self.world_num, value='3')
        world_3.pack()
        world_4 = ttk.Radiobutton(self, text='World 4', variable=self.world_num, value='4')
        world_4.pack()
        #save button setup
        self.open_folder_button = ttk.Button(self, text='Save World', command=lambda:self.get_save_folder())
        self.open_folder_button.pack()
        self.warning_label = ttk.Label(self, text='WARNING: SAVING WILL OVERWRIGHT EXISTING WORLD OF SAME NUMBERS')
        self.warning_label.pack()
    def get_save_folder(self):
        #get save directiory name, then run save command
        directory_path = filedialog.askdirectory()
        if directory_path != '':
            self.world.save_world(directory_path, self.world_num.get())
            self.parent.new_page(World_Saved, 'center', font=self.font)
class World_Saved(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #run parent init
        super().__init__(parent)
        self.parent = parent
        self.font = kwargs['font']
        self.label = ttk.Label(self, text='World Saved!')
        self.label['font'] = self.font
        self.label.pack()
        self.main_menu_button = ttk.Button(self, text='Main Menu', command=lambda:self.parent.new_page(Start_Page, 'center', font=label_font))
        self.main_menu_button.pack()
def find_version(path):
    '''Find World version using the path'''
    version = 0
    if os.path.isdir(path + '/entities'):
        version = '1.1'
    else:
        version = '1.0'
    return version
#define fonts
label_font = font.Font(family='Helvetica', name='label_font', size=24, weight='bold')
error_font = font.Font(family='Helvetica', name='error_font', size=24, weight='bold')
#set up app to run
app.new_page(Start_Page, 'center', font=label_font)
#run main loop
app.mainloop()