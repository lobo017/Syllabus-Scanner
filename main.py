import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from icalendar import Calendar, Event
from datetime import datetime
import re
import pytz
from SyllabusProcessor import SyllabusProcessor  # Changed import statement

class SyllabusConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Syllabus to iCalendar Converter")
        self.root.geometry("600x700")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Course Information
        ttk.Label(self.main_frame, text="Course Information", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
        
        # Course Title
        ttk.Label(self.main_frame, text="Course Title:").grid(row=1, column=0, sticky=tk.W)
        self.course_title = ttk.Entry(self.main_frame, width=50)
        self.course_title.grid(row=1, column=1, pady=5)
        
        # Instructor
        ttk.Label(self.main_frame, text="Instructor:").grid(row=2, column=0, sticky=tk.W)
        self.instructor = ttk.Entry(self.main_frame, width=50)
        self.instructor.grid(row=2, column=1, pady=5)
        
        # Timezone
        ttk.Label(self.main_frame, text="Timezone:").grid(row=3, column=0, sticky=tk.W)
        self.timezone = ttk.Combobox(self.main_frame, values=pytz.all_timezones, width=47)
        self.timezone.set('UTC')
        self.timezone.grid(row=3, column=1, pady=5)
        
        # Syllabus Input
        ttk.Label(self.main_frame, text="Paste Syllabus Schedule:", font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Text area for syllabus input with scrollbar
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.syllabus_text = tk.Text(self.text_frame, height=20, width=70)
        self.scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.syllabus_text.yview)
        self.syllabus_text.configure(yscrollcommand=self.scrollbar.set)
        
        self.syllabus_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Example Format
        example_text = "Example format:\nJan 15, 2024 - Introduction to Course\nJan 22, 2024 - Chapter 1 Discussion\n..."
        ttk.Label(self.main_frame, text=example_text, font=('Arial', 8, 'italic')).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Convert to iCalendar", command=self.convert_to_ical).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).grid(row=0, column=1, padx=5)
        
    def parse_date(self, date_str):
        try:
            # Try to parse the date string
            date_obj = datetime.strptime(date_str.strip(), "%b %d, %Y")
            # Set time to 9 AM by default
            date_obj = date_obj.replace(hour=9, minute=0)
            return date_obj
        except ValueError:
            return None
    
    def convert_to_ical(self):
        processor = SyllabusProcessor()  # Create instance of the class
        
        if not self.course_title.get() or not self.syllabus_text.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Please fill in the course title and syllabus schedule.")
            return
        
        course_info = {
            'title': self.course_title.get(),
            'instructor': self.instructor.get()
        }
        
        try:
            calendar = processor.process_syllabus(
                self.syllabus_text.get("1.0", tk.END),
                course_info=course_info,
                timezone=self.timezone.get()
            )
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".ics",
                filetypes=[("iCalendar files", "*.ics")]
            )
            
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(calendar.to_ical())
                messagebox.showinfo("Success", "Calendar file created successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error processing syllabus: {str(e)}")
    
    def clear_fields(self):
        self.course_title.delete(0, tk.END)
        self.instructor.delete(0, tk.END)
        self.syllabus_text.delete("1.0", tk.END)
        self.timezone.set('UTC')

if __name__ == "__main__":
    root = tk.Tk()
    app = SyllabusConverter(root)
    root.mainloop()