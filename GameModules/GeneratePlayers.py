import difflib
import tkinter
import random
import numpy as np

from tkinter import messagebox
from Modules.ReadWrite import write_toArray

# Global variables for storing flag library and player names
file_path = r'Docs/profanities.txt'
profanities = write_toArray(file_path)
flag_libr = {
  "valid": ['david', 'susan', 'mathew'],
  'invalid': profanities,
  'data': [str, int],
}

## The cutoff threshold (0.7) used in flagFilter for close match validation
MATCH_ratio = 0.9

# player_generated is to be passed to DrawCrads module
players_generated = {}

def flagFilter(user_input, flag_copy):
  """
  Matches user input against elements in flag_copy and returns the closest match.

  Args:
    user_input (str): The input string provided by the user.
    flag_copy (dict): Dictionary of flag categories and their possible values.

  Returns:
    tuple: (closest match, flag category name)
      - closest match: The closest matching element from flag_copy based on the cutoff ratio (0.7).
      - flag category name: The name of the category (e.g., 'invalid') in which the match was found.

  The function uses difflib.get_close_matches with a cutoff of 0.7 to find close matches 
  for the user input. If a match is found in the 'invalid' flag category, it is returned 
  immediately. Otherwise, the first match found is returned.
  """
  return_match = ''
  return_name = ''
  instance = False
  for flag_name, flag_elements in flag_copy.items():
    flag_match = difflib.get_close_matches(user_input, flag_elements, cutoff = MATCH_ratio, n=1)
    if flag_match and flag_name == 'invalid':
      return flag_match, flag_name
    elif flag_match and not instance:
      instance = True
      return_match = flag_match
      return_name = flag_name
  return return_match, return_name

def checkDuplicate(user_input, names_list):
  """Checks if user input is a duplicate and suggests a modified name if necessary"""
  characters = ['@', '$', '&', '%', '^']
  if user_input in names_list:
    appended = user_input
    while appended in names_list:
      rand_size = np.random.randint(1, 4, size=1)
      rand_num = np.random.randint(1, 10, size=rand_size).astype(str)
      rand_char = random.choice(characters)
      str_num = ''.join(rand_num)
      appended = ''.join((user_input, rand_char, str_num))
    
    answer = messagebox.askyesno('NAME USED', f'{user_input.upper()} already used, do you want to try {appended}?')
    if answer:
      return appended
    else:
      return None
  return user_input

def parseInput(event = None):
  """Handles user input parsing and validation"""
  flag_copy = flag_libr.copy()
  user_input = input_tab.get().strip().lower()

  # Check if the input is a duplicate
  user_input = checkDuplicate(user_input, list(players_generated.keys()))
  
  if user_input is None:
    return  # Do nothing if user declined the duplicate name
  elif user_input:
    dtype_is_valid = True
    flag_dtype = flag_libr.get('data', None)
    
    if flag_dtype is not None:
      flag_copy.pop('data')
      if not isinstance(user_input, tuple(flag_dtype)):
        dtype_is_valid = False

    if dtype_is_valid:
      close_match, name_flag = flagFilter(user_input, flag_copy)
      if close_match:
        bool_flag = user_input == close_match[0]
        if name_flag == 'invalid':
          messagebox.showwarning('INVALID ENTRY', f'Please ensure input does not contain {close_match[0].upper()}')
        elif bool_flag:
          players_generated[user_input] = []
        else:
          answer = messagebox.askyesno('VALIDATION', f'Were you trying to type {close_match[0]}?')
          user_input = close_match[0] if answer else user_input
          players_generated[user_input] = []
      else:
        players_generated[user_input] = []
    else:
      messagebox.showerror('INVALID DATA TYPE', f'Please ensure input is of data type {flag_dtype}')
  else:
    messagebox.showerror('VOID ENTRY ERROR', 'Void input invalid')

  input_tab.delete(0, 'end')

def cancel(event = None):
  """Closes the application"""
  widget_root.destroy()

def centerWidget(widget_root, root_width, root_height, hoizontal_shift = 0, vertical_shift = 0):
  """Centers the widget on the screen"""
  screen_width = widget_root.winfo_screenwidth()
  screen_height = widget_root.winfo_screenheight()
  x = (screen_width // 2) - (root_width // 2) + hoizontal_shift
  y = (screen_height // 2) - (root_height // 2) + vertical_shift
  widget_root.geometry(f"{root_width}x{root_height}+{x}+{y}")

def RunGeneratePlayers():
  """Main function to run the application"""
  global input_tab, widget_root

  # Widget root
  widget_colour = 'grey'
  widget_width = 400
  widget_height = 400
  global_font = ('Arial', 16)
  
  # Shift vertical and horizontal from center
  v_shift = -100
  h_shift = 0

  widget_root = tkinter.Tk()
  widget_root.title('USER INPUT')
  widget_root.config(bg=widget_colour)
  centerWidget(widget_root, widget_width, widget_height, h_shift, v_shift)

  entry_label = tkinter.Label(widget_root, text='Enter Name below', font=global_font, bg='black', fg='white')
  entry_label.place(relx=0.5, rely=0.3, anchor='center')

  input_tab = tkinter.Entry(widget_root, width=widget_width // 10)
  input_tab.place(relx=0.5, rely=0.5, anchor='center')

  submit_button = tkinter.Button(widget_root, command=parseInput, text='Submit', font=global_font, bg='darkred', fg='white')
  submit_button.place(relx=0.3, rely=0.7, anchor='center')

  cancel_button = tkinter.Button(widget_root, command=cancel, text='Cancel', font=global_font, bg='darkred', fg='white')
  cancel_button.place(relx=0.7, rely=0.7, anchor='center')

  widget_root.bind('<Return>', parseInput)
  widget_root.bind('<Escape>', cancel)

  widget_root.mainloop()


