#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from pathlib import Path
import sys

class ShiftLockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 ShiftLock - Caesar Cipher Tool")
        self.root.geometry("750x600")
        self.root.minsize(600, 450)  # Even smaller minimum window size
        self.root.resizable(True, True)
        
        # Configure colors and styling
        self.setup_styles()
        
        # Load character sets
        self.charsets = self.load_charsets()
        
        self.create_widgets()
        
    def setup_styles(self):
        """Setup modern styling and colors"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define color scheme
        self.colors = {
            'primary': '#2c3e50',      # Dark blue-gray
            'secondary': '#3498db',    # Blue
            'accent': '#e74c3c',       # Red
            'success': '#27ae60',      # Green
            'warning': '#f39c12',      # Orange
            'light': '#ecf0f1',        # Light gray
            'dark': '#2c3e50',         # Dark
            'white': '#ffffff',        # White
            'text': '#2c3e50',         # Dark text
            'bg': '#f8f9fa'            # Light background
        }
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'), 
                       foreground=self.colors['primary'],
                       background=self.colors['bg'])
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['primary'],
                       background=self.colors['bg'])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Primary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure frame styles
        style.configure('Card.TFrame', 
                       background=self.colors['white'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure label frame styles
        style.configure('Card.TLabelframe', 
                       background=self.colors['white'],
                       relief='solid',
                       borderwidth=2)
        style.configure('Card.TLabelframe.Label', 
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['white'])
    
    def load_charsets(self):
        """Load character sets from JSON file"""
        try:
            # Cross-platform way to check if running as root/admin
            try:
                is_admin = os.getuid() == 0 if hasattr(os, 'getuid') else False
            except:
                is_admin = False
            
            if is_admin:
                data_dir = Path('/usr/share/shiftlock')
            else:
                data_dir = Path(__file__).parent.parent / 'data'
            
            # Try both possible filenames
            charset_file = data_dir / 'charsets.json'
            if not charset_file.exists():
                charset_file = data_dir / 'character.json'
            
            with open(charset_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load character sets: {e}")
            return {}
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Configure main window background
        self.root.configure(bg=self.colors['bg'])
        
        # Create main canvas with scrollbars for the entire interface
        canvas = tk.Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(self.root, orient="horizontal", command=canvas.xview)
        
        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Grid the canvas and scrollbars
        canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights for scrolling
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame with padding and background - now inside canvas
        main_frame = ttk.Frame(canvas, padding="10", style='Card.TFrame')
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Configure canvas scrolling region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_window(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        main_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_window)
        
        # Configure grid weights for main frame
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title with icon and gradient effect - More compact
        title_frame = ttk.Frame(main_frame, style='Card.TFrame')
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 8))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, 
                               text="🔐 ShiftLock - Caesar Cipher Tool", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=5)
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="Secure text encryption and decryption with multiple character sets", 
                                  font=('Segoe UI', 8),
                                  foreground='#7f8c8d',
                                  background=self.colors['bg'])
        subtitle_label.grid(row=1, column=0, pady=(0, 5))
        
        # Operation selection with modern styling - More compact
        operation_frame = ttk.LabelFrame(main_frame, text="🎯 Operation", padding="8", style='Card.TLabelframe')
        operation_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 8))
        operation_frame.columnconfigure(1, weight=1)
        
        self.operation_var = tk.StringVar(value="encrypt")
        operation_buttons_frame = ttk.Frame(operation_frame)
        operation_buttons_frame.grid(row=0, column=1, sticky="ew")
        
        # Modern radio buttons with icons
        ttk.Radiobutton(operation_buttons_frame, text="🔒 Encrypt", variable=self.operation_var, 
                       value="encrypt").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(operation_buttons_frame, text="🔓 Decrypt", variable=self.operation_var, 
                       value="decrypt").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(operation_buttons_frame, text="🔍 Brute Force", variable=self.operation_var, 
                       value="bruteforce").pack(side=tk.LEFT)
        
        # Settings frame with modern design - More compact
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="8", style='Card.TLabelframe')
        settings_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 8))
        settings_frame.columnconfigure(1, weight=1)
        
        # Shift value with modern spinbox
        ttk.Label(settings_frame, text="🔢 Shift Value:", font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        self.shift_var = tk.StringVar(value="3")
        shift_spinbox = ttk.Spinbox(settings_frame, from_=-25, to=25, textvariable=self.shift_var, 
                                   width=8, font=('Segoe UI', 9))
        shift_spinbox.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Character set with modern combobox
        ttk.Label(settings_frame, text="📝 Character Set:", font=('Segoe UI', 9, 'bold')).grid(row=1, column=0, sticky="w", pady=5)
        self.charset_var = tk.StringVar(value="basic")
        charset_combo = ttk.Combobox(settings_frame, textvariable=self.charset_var, 
                                    values=list(self.charsets.keys()), state="readonly", 
                                    width=12, font=('Segoe UI', 9))
        charset_combo.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)
        
        # Input frame with modern design - More compact
        input_frame = ttk.LabelFrame(main_frame, text="📥 Input", padding="8", style='Card.TLabelframe')
        input_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 8))
        input_frame.columnconfigure(1, weight=1)
        
        # Input type selection with modern styling
        ttk.Label(input_frame, text="📋 Input Type:", font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        self.input_type_var = tk.StringVar(value="text")
        input_type_frame = ttk.Frame(input_frame)
        input_type_frame.grid(row=0, column=1, sticky="ew", pady=5)
        
        ttk.Radiobutton(input_type_frame, text="📝 Text", variable=self.input_type_var, 
                       value="text", command=self.toggle_input_type).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(input_type_frame, text="📁 File", variable=self.input_type_var, 
                       value="file", command=self.toggle_input_type).pack(side=tk.LEFT)
        
        # Input text with modern styling - Much smaller height for better output visibility
        ttk.Label(input_frame, text="📄 Input Text:", font=('Segoe UI', 9, 'bold')).grid(row=1, column=0, sticky="w", pady=5)
        self.input_text = scrolledtext.ScrolledText(input_frame, height=2, width=50, 
                                                   font=('Consolas', 9), 
                                                   bg=self.colors['white'],
                                                   fg=self.colors['text'],
                                                   insertbackground=self.colors['secondary'])
        self.input_text.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=5)
        
        # File input (initially hidden)
        self.file_frame = ttk.Frame(input_frame)
        self.file_frame.grid(row=2, column=1, sticky="ew", padx=(10, 0), pady=5)
        self.file_frame.grid_remove()  # Initially hidden
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=35, font=('Segoe UI', 9))
        file_entry.pack(side=tk.LEFT, padx=(0, 8))
        browse_btn = ttk.Button(self.file_frame, text="📂 Browse", command=self.browse_file, style='Primary.TButton')
        browse_btn.pack(side=tk.LEFT)
        
        # Output frame with modern design - Always visible with minimum height
        output_frame = ttk.LabelFrame(main_frame, text="📤 Output", padding="8", style='Card.TLabelframe')
        output_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(0, 8))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)
        
        # Output options with modern styling
        output_options_frame = ttk.Frame(output_frame)
        output_options_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(output_options_frame, text="💾 Output:", font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)
        self.output_type_var = tk.StringVar(value="display")
        ttk.Radiobutton(output_options_frame, text="📺 Display", variable=self.output_type_var, 
                       value="display").pack(side=tk.LEFT, padx=(10, 0))
        ttk.Radiobutton(output_options_frame, text="💾 Save to File", variable=self.output_type_var, 
                       value="file").pack(side=tk.LEFT, padx=(10, 0))
        
        # Output text area with modern styling - Always visible with scrollbars
        self.output_text = scrolledtext.ScrolledText(output_frame, height=5, width=50, wrap=tk.WORD,
                                                    font=('Consolas', 8),
                                                    bg=self.colors['light'],
                                                    fg=self.colors['text'],
                                                    insertbackground=self.colors['secondary'])
        self.output_text.grid(row=1, column=0, sticky="nsew", pady=5)
        
        # Add initial text to verify output area is visible
        self.output_text.insert(1.0, "🚀 Ready to process your text! Enter some text above and click Process.")
        
        # Ensure the output frame has a minimum height and scrollbars are always visible
        output_frame.grid_propagate(False)  # Prevent frame from shrinking
        output_frame.configure(height=180)  # Set minimum height
        
        # Force scrollbars to be visible by adding more content
        self.output_text.insert(tk.END, "\n\n" + "="*40 + "\n")
        self.output_text.insert(tk.END, "="*40)
        
        # Buttons frame with modern styling - More compact
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=8)
        
        # Modern buttons with icons and colors
        process_btn = ttk.Button(buttons_frame, text="🚀 Process", command=self.process_text, style='Success.TButton')
        process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(buttons_frame, text="🧹 Clear", command=self.clear_all, style='Warning.TButton')
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_btn = ttk.Button(buttons_frame, text="❌ Exit", command=self.root.quit, style='Primary.TButton')
        exit_btn.pack(side=tk.LEFT)
        
        # Status bar with modern styling
        self.status_var = tk.StringVar(value="✅ Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              font=('Segoe UI', 8),
                              foreground=self.colors['success'],
                              background=self.colors['light'],
                              relief='solid', borderwidth=1)
        status_bar.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        
        # Bind mouse wheel scrolling for better user experience
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Store canvas reference for later use
        self.canvas = canvas
    
    def toggle_input_type(self):
        """Toggle between text and file input"""
        if self.input_type_var.get() == "text":
            self.input_text.grid()
            self.file_frame.grid_remove()
        else:
            self.input_text.grid_remove()
            self.file_frame.grid()
    
    def browse_file(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def shift_text(self, text, shift, charset="basic"):
        """Caesar cipher implementation"""
        print(f"Debug: Using charset '{charset}' for shifting")
        
        if charset == 'basic':
            # Basic charset: A-Z and a-z separately
            upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            lower = 'abcdefghijklmnopqrstuvwxyz'
            result = []
            for char in text:
                if char in upper:
                    idx = upper.index(char)
                    new_idx = (idx + shift) % 26
                    result.append(upper[new_idx])
                elif char in lower:
                    idx = lower.index(char)
                    new_idx = (idx + shift) % 26
                    result.append(lower[new_idx])
                else:
                    result.append(char)
            return ''.join(result)
        else:
            # Use the selected charset from the JSON file
            charset_data = self.charsets.get(charset)
            if not charset_data:
                print(f"Debug: Charset '{charset}' not found, falling back to basic")
                return self.shift_text(text, shift, "basic")
            
            chars = charset_data['chars']
            wrap = len(chars)
            print(f"Debug: Using charset '{charset}' with {len(chars)} characters, wrap={wrap}")
            
            result = []
            for char in text:
                if char in chars:
                    idx = chars.index(char)
                    new_idx = (idx + shift) % wrap
                    result.append(chars[new_idx])
                else:
                    result.append(char)
            return ''.join(result)
    
    def process_text(self):
        """Process the input text/file"""
        try:
            # Get input content
            if self.input_type_var.get() == "text":
                content = self.input_text.get(1.0, tk.END).strip()
                if not content:
                    messagebox.showwarning("⚠️ Warning", "Please enter some text to process.")
                    return
            else:
                file_path = self.file_path_var.get()
                if not file_path:
                    messagebox.showwarning("⚠️ Warning", "Please select an input file.")
                    return
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    messagebox.showerror("❌ Error", f"Failed to read file: {e}")
                    return
            
            # Get parameters
            operation = self.operation_var.get()
            shift = int(self.shift_var.get())
            charset = self.charset_var.get()
            
            # Debug information
            print(f"Debug: Operation={operation}, Shift={shift}, Charset={charset}")
            print(f"Debug: Input content='{content}'")
            print(f"Debug: Available charsets={list(self.charsets.keys())}")
            
            # Validate shift range
            if not (-25 <= shift <= 25):
                messagebox.showerror("❌ Error", "Shift must be between -25 and 25")
                return
            
            # Update status
            self.status_var.set("🔄 Processing...")
            self.root.update()
            
            # Process content
            if operation == "encrypt":
                result = self.shift_text(content, shift, charset)
                print(f"Debug: Encrypt result='{result}'")
                operation_text = "🔒 Encrypted"
            elif operation == "decrypt":
                result = self.shift_text(content, -shift, charset)
                print(f"Debug: Decrypt result='{result}'")
                operation_text = "🔓 Decrypted"
            else:  # bruteforce
                result = "🔍 Brute-force results:\n"
                for i in range(1, 26):
                    result += f"Shift {i:2d}: {self.shift_text(content, -i, charset)}\n"
                print(f"Debug: Brute force completed")
                operation_text = "🔍 Brute Force"
            
            # Handle output
            if self.output_type_var.get() == "display":
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, result)
                self.status_var.set(f"✅ {operation_text} successfully!")
                print(f"Debug: Output displayed in GUI")
            else:
                # Save to file
                filename = filedialog.asksaveasfilename(
                    title="💾 Save Output File",
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                if filename:
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(result)
                        self.status_var.set(f"💾 {operation_text} and saved to file!")
                        messagebox.showinfo("✅ Success", f"Output saved to {filename}")
                    except Exception as e:
                        messagebox.showerror("❌ Error", f"Failed to save file: {e}")
                        self.status_var.set("❌ Error saving file")
        
        except Exception as e:
            print(f"Debug: Error occurred - {e}")
            messagebox.showerror("❌ Error", f"An error occurred: {e}")
            self.status_var.set("❌ Error occurred")
    
    def clear_all(self):
        """Clear all input and output"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, "🚀 Ready to process your text! Enter some text above and click Process.")
        self.output_text.insert(tk.END, "\n\n" + "="*40 + "\n")
        self.output_text.insert(tk.END, "Output area is ready with scrollbars!\n")
        self.output_text.insert(tk.END, "This area will show your encrypted/decrypted text.\n")
        self.output_text.insert(tk.END, "Scrollbars will appear when content exceeds this area.\n")
        self.output_text.insert(tk.END, "="*40)
        self.file_path_var.set("")
        self.status_var.set("✅ Ready")

def main():
    root = tk.Tk()
    app = ShiftLockGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 