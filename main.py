import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from priority_queue import PriorityQueue
from PIL import Image, ImageTk

#relief=tk.SUNKEN, borderwidth=2
#text="Hospital Reception", font=("Helvetica", 20)

class HospitalQueueApp:
  def __init__(self, root):
    self.root = root #main application window
    self.root.title("Hospital Reception Queue") #set title of the window
    self.queue = PriorityQueue()
    self.setup_ui() #calls the method to set up the UI
    
  def simple_input(self, prompt):
    return simpledialog.askstring("Input", prompt, parent=self.root)
    
  def setup_ui(self):
    #Title
    title_frame = tk.Frame(self.root)
    title_frame.pack(pady=10)
    
    try:
      img_path = "assets/reception.png"
      img = Image.open(img_path)
      img = img.resize((50, 50))
      self.img_tk = ImageTk.PhotoImage(img)
      img_label = tk.Label(title_frame, image=self.img_tk)
      img_label.grid(row=0, column=0, padx=(0, 10))
    except Exception as e:
      print(f"Error loading image")
      
    title_label = tk.Label(title_frame, text="Hospital Reception", font=("Helvetica", 20))
    title_label.grid(row=0, column=1, padx=(0, 10))
      
    tk.Button(title_frame, text="Call Next(Receptionist)", command=self.call_next).grid(row=0, column=2, padx=5)
    
  # Create a frame for the scrollable area
    self.queue_frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=2)
    self.queue_frame.pack(expand=True, fill=tk.BOTH, pady=10)

    # Create a canvas
    self.canvas = tk.Canvas(self.queue_frame)
    self.scrollbar = ttk.Scrollbar(self.queue_frame, orient="vertical", command=self.canvas.yview)
    self.scrollable_frame = tk.Frame(self.canvas)

    # Configure the canvas
    self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

    # Pack the scrollbar and canvas
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Connect scrollbar to the canvas
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    
    #Buttons
    button_frame = tk.Frame(self.root)
    button_frame.pack(side=tk.BOTTOM, pady=10)
  
    tk.Button(button_frame, text="Remove by Name", command=self.remove_by_name).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Add person", command=self.add_person).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Show first person", command=self.display_first_person).grid(row=0, column=3, padx=5)
    tk.Button(button_frame, text="Update Profile", command=self.update_profile).grid(row=0, column=4, padx=5)
    tk.Button(button_frame, text="Is Empty", command=self.check_is_empty).grid(row=0, column=5, padx=5)
    tk.Button(button_frame, text="Length of queue", command=self.check_length).grid(row=0, column=6, padx=5)
    self.update_queue_display()
    
  def update_queue_display(self):
    #clear current display
    for widget in self.scrollable_frame.winfo_children():
      widget.destroy()
    
    #display each person in the queue
    if not self.queue.is_empty():
      for priority, _, profile in sorted(self.queue.data):
        try:
          img_path = "assets/person.png"
          img = Image.open(img_path)
          img = img.resize((50, 50))
          img_tk = ImageTk.PhotoImage(img)
        except Exception as e:
          print(f"Error loading image")
          img_tk = None
          
        person_frame = tk.Frame(self.scrollable_frame)
        person_frame.pack(pady=5)
        
        if  img_tk:
          img_label = tk.Label(person_frame, image=img_tk)
          img_label.image = img_tk
          img_label.pack(side=tk.LEFT, padx=(0, 5))
          
        person_label = tk.Label(
          person_frame, 
          text=f"{profile['name']} (Age: {profile['age']})", 
          font=("Helvetica", 14))
        person_label.pack(side=tk.LEFT, pady=2)
    else:
      empty_label = tk.Label(self.scrollable_frame, text="Queue is empty", font=("Helvetica", 14))
      empty_label.pack()
      
  def call_next(self):
    removed = self.queue.remove_min()
    if removed:
      messagebox.showinfo("Receptionist", f"Next person: {removed['name']} (Age: {removed['age']})")
    else:
      messagebox.showwarning("Receptionist", "The queue is empty!")
    self.update_queue_display()
    
  def remove_by_name(self):
    name = self.simple_input("Enter the name of the person to be removed: ")
    if name:
      removed = self.queue.remove_by_name(name)
      if removed:
        messagebox.showinfo("Success", f"Removed {removed['name']} (Age: {removed['age']})")
      else:
        messagebox.showerror("Error", f"No person names {name} found in the queue.")
    # self.queue.data.sort(reverse=True)
    self.update_queue_display()
    
  def add_person(self):
    name = self.simple_input("Enter name")
    age = self.simple_input("Enter age:")
    if name and age:
      try:
        age = int(age)
        self.queue.add(age, {"name": name, "age": age})
        self.update_queue_display()
      except ValueError:
        messagebox.showerror("Error", "Age must be a number!")
        
  def display_first_person(self):
    if not self.queue.is_empty():
      first_person = self.queue.min()
      messagebox.showinfo("First person", f"Name: {first_person['name']}\nAge: {first_person['age']}")
    else:
      messagebox.showwarning("Queue Empty", "There is no one in the queue")
      
  def update_profile(self):
      name = self.simple_input("Enter the name of the person to update:")
      if name:
        for _, _, profile in self.queue.data:
          if profile['name'].lower() == name.lower():
            new_name = self.simple_input(f"Enter new name for {profile['name']} (leave blank to keep the same)")
            new_age = self.simple_input(f"Enter new age for {profile['name']}(leave blank to kepp the same)")
            updated_profile = profile.copy() #start with existing profile
            
            if new_name:
              # profile['name'] = new_name
              updated_profile['name'] = new_name
            if new_age:
              try:
                updated_profile['age'] = int(new_age)
                # self.queue.data[index] = (new_age, profile['name'], profile)
                # self.queue.data.sort(reverse=True) #resort the queue
                # messagebox.showinfo("Profile updated", f"{name}'s profile updated successfully")
              except ValueError:
                messagebox.showerror("Error", "Age must be a number")
                return
            
            try:
              self.queue.update(profile['name'], updated_profile['age'], updated_profile)
              messagebox.showinfo("Profile updated", f"{name}'s profile updated successfully")
              self.update_queue_display()
              return
            except ValueError as e:
              messagebox.showerror("Error", str(e))
              return
          
        messagebox.showerror("Error", f"No person named {name} found")
          
  def check_is_empty(self):
    if self.queue.is_empty():
      messagebox.showinfo("Queue Status", "The queue is currently empty")
    else:
      messagebox.showinfo("Queue Status", "The queue is not empty")
      
  def check_length(self):
    length = len(self.queue)
    messagebox.showinfo("Queue length", f"There are  {length} people in the queue")
       
          
if __name__ == "__main__":
  root = tk.Tk() #create main window
  root.geometry("800x600")
  app = HospitalQueueApp(root) #initialize the app
  root.mainloop() #start the GUI Loop
    