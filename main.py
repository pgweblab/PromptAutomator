import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pynput import mouse, keyboard
import pyautogui
import json
import threading
import time
from datetime import datetime
import os

class ModernAutomationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title('AI Prompt Automator')
        self.root.geometry('1000x800')
        self.root.minsize(800, 600)  # Dimensione minima
        
        # Finestra sempre in primo piano
        self.root.attributes('-topmost', True)
        
        # Stile moderno
        self.setup_modern_style()
        
        # Variabili
        self.start_coordinates = None
        self.artifact_coordinates = None
        self.instructions = []
        self.instruction_widgets = []
        self.is_recording = False
        self.is_automation_running = False
        self.is_automation_paused = False
        self.current_instruction_index = 0
        self.current_recording_type = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.automation_thread = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_modern_style(self):
        # Colori moderni
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.accent_color = '#007ACC'
        self.secondary_color = '#2d2d30'
        self.success_color = '#4CAF50'
        self.danger_color = '#f44336'
        self.text_bg = '#3c3c3c'
        
        self.root.configure(bg=self.bg_color)
        
        # Stile ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurazione stili
        style.configure('Modern.TFrame', background=self.bg_color)
        style.configure('Card.TFrame', background=self.secondary_color, relief='flat', borderwidth=1)
        style.configure('Modern.TLabel', background=self.bg_color, foreground=self.fg_color, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=self.bg_color, foreground=self.fg_color, font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background=self.secondary_color, foreground=self.fg_color, font=('Segoe UI', 12, 'bold'))
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Small.TButton', font=('Segoe UI', 9))
        
        # Mappatura dei colori per i bottoni
        style.map('Accent.TButton',
                 background=[('active', '#005a9e'), ('!active', self.accent_color)],
                 foreground=[('active', 'white'), ('!active', 'white')])
        style.map('Success.TButton',
                 background=[('active', '#45a049'), ('!active', self.success_color)],
                 foreground=[('active', 'white'), ('!active', 'white')])
        style.map('Danger.TButton',
                 background=[('active', '#da190b'), ('!active', self.danger_color)],
                 foreground=[('active', 'white'), ('!active', 'white')])
        
    def setup_ui(self):
        # Container principale con gestione responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_rowconfigure(2, weight=1)  # La riga delle istruzioni si espande
        main_container.grid_columnconfigure(0, weight=1)
        
        # Titolo
        title_label = ttk.Label(main_container, text="AI Prompt Automator", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Frame per le coordinate
        self.setup_coordinates_frame(main_container, row=1)
        
        # Frame per le istruzioni (espandibile)
        self.setup_instructions_frame(main_container, row=2)
        
        # Frame per controlli automazione
        self.setup_automation_frame(main_container, row=3)
        
    def setup_coordinates_frame(self, parent, row):
        # Card per le coordinate
        coord_card = ttk.Frame(parent, style='Card.TFrame')
        coord_card.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        coord_card.grid_columnconfigure(0, weight=1)
        
        # Padding interno
        coord_inner = ttk.Frame(coord_card, style='Card.TFrame')
        coord_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Titolo sezione
        coord_title = ttk.Label(coord_inner, text="📍 Coordinate", style='Subtitle.TLabel')
        coord_title.pack(anchor='w', pady=(0, 10))
        
        # Frame per i due campi
        fields_frame = ttk.Frame(coord_inner, style='Card.TFrame')
        fields_frame.pack(fill=tk.X)
        
        # Campo Start
        start_frame = ttk.Frame(fields_frame, style='Card.TFrame')
        start_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Label(start_frame, text="Campo Start:", style='Modern.TLabel').pack(anchor='w')
        self.start_label = ttk.Label(start_frame, text="Non impostato", style='Modern.TLabel', 
                                    font=('Segoe UI', 10, 'bold'))
        self.start_label.pack(anchor='w', pady=(5, 5))
        
        self.start_button = ttk.Button(start_frame, text="Registra Start", 
                                      command=lambda: self.start_coordinate_recording('start'),
                                      style='Accent.TButton')
        self.start_button.pack(fill=tk.X, pady=(5, 0))
        
        # Campo Artifact
        artifact_frame = ttk.Frame(fields_frame, style='Card.TFrame')
        artifact_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(artifact_frame, text="Campo Artifact:", style='Modern.TLabel').pack(anchor='w')
        self.artifact_label = ttk.Label(artifact_frame, text="Non impostato", style='Modern.TLabel',
                                       font=('Segoe UI', 10, 'bold'))
        self.artifact_label.pack(anchor='w', pady=(5, 5))
        
        self.artifact_button = ttk.Button(artifact_frame, text="Registra Artifact", 
                                         command=lambda: self.start_coordinate_recording('artifact'),
                                         style='Accent.TButton')
        self.artifact_button.pack(fill=tk.X, pady=(5, 0))
        
        # Istruzioni per le coordinate
        instructions_text = "Premi il bottone per registrare, muovi il mouse e premi SPAZIO per confermare (ESC per annullare)"
        instructions_label = ttk.Label(coord_inner, text=instructions_text, style='Modern.TLabel', 
                                     font=('Segoe UI', 9, 'italic'))
        instructions_label.pack(anchor='w', pady=(10, 0))
        
    def setup_instructions_frame(self, parent, row):
        # Card per le istruzioni
        inst_card = ttk.Frame(parent, style='Card.TFrame')
        inst_card.grid(row=row, column=0, sticky="nsew", pady=(0, 15))
        inst_card.grid_rowconfigure(0, weight=1)
        inst_card.grid_columnconfigure(0, weight=1)
        
        # Padding interno
        inst_inner = ttk.Frame(inst_card, style='Card.TFrame')
        inst_inner.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        inst_inner.grid_rowconfigure(1, weight=1)
        inst_inner.grid_columnconfigure(0, weight=1)
        
        # Header con titolo e bottone aggiungi
        header_frame = ttk.Frame(inst_inner, style='Card.TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        inst_title = ttk.Label(header_frame, text="📝 Istruzioni", style='Subtitle.TLabel')
        inst_title.pack(side=tk.LEFT)
        
        # Frame per i bottoni
        buttons_frame = ttk.Frame(header_frame, style='Card.TFrame')
        buttons_frame.pack(side=tk.RIGHT)
        
        # Bottoni per salvare/caricare
        load_button = ttk.Button(buttons_frame, text="📂 Carica", 
                               command=self.load_instructions,
                               style='Accent.TButton')
        load_button.pack(side=tk.LEFT, padx=(0, 5))
        
        save_button = ttk.Button(buttons_frame, text="💾 Salva", 
                               command=self.save_instructions,
                               style='Accent.TButton')
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        add_button = ttk.Button(buttons_frame, text="➕ Aggiungi Istruzione", 
                               command=self.add_instruction_field,
                               style='Success.TButton')
        add_button.pack(side=tk.LEFT)
        
        # Frame con scrollbar per le istruzioni
        scroll_container = ttk.Frame(inst_inner, style='Card.TFrame')
        scroll_container.grid(row=1, column=0, sticky="nsew")
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        # Canvas e scrollbar
        self.canvas = tk.Canvas(scroll_container, bg=self.secondary_color, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(scroll_container, orient="horizontal", command=self.canvas.xview)
        
        self.scrollable_frame = ttk.Frame(self.canvas, style='Card.TFrame')
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Layout scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind per aggiornare scroll region
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind per scroll con rotella mouse
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        self.instructions_container = self.scrollable_frame
        
        # Aggiungi il primo campo
        self.add_instruction_field()
        
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        # Adatta la larghezza del frame al canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def add_instruction_field(self):
        # Frame per singola istruzione
        instruction_frame = ttk.Frame(self.instructions_container, style='Card.TFrame')
        instruction_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10), padx=5)
        
        # Header con numero e bottone rimuovi
        header = ttk.Frame(instruction_frame, style='Card.TFrame')
        header.pack(fill=tk.X, pady=(0, 5))
        
        num = len(self.instruction_widgets) + 1
        label = ttk.Label(header, text=f"Istruzione {num}:", style='Modern.TLabel', 
                         font=('Segoe UI', 11, 'bold'))
        label.pack(side=tk.LEFT)
        
        # Text widget con auto-resize
        text_frame = ttk.Frame(instruction_frame, style='Card.TFrame')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, height=3, wrap=tk.WORD,
                             bg=self.text_bg, fg='white', insertbackground='white',
                             font=('Segoe UI', 11), relief=tk.FLAT, bd=10,
                             padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar per il text widget
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=text_scrollbar.set)
        
        # Bind per auto-resize
        text_widget.bind('<KeyRelease>', lambda e: self.auto_resize_text(text_widget))
        text_widget.bind('<FocusIn>', lambda e: self.on_text_focus(text_widget))
        
        # Bottone rimuovi (solo se non è il primo)
        if len(self.instruction_widgets) > 0:
            remove_btn = ttk.Button(header, text="❌ Rimuovi", 
                                   command=lambda idx=len(self.instruction_widgets): self.remove_instruction(idx),
                                   style='Small.TButton')
            remove_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.instruction_widgets.append({
            'frame': instruction_frame,
            'text': text_widget,
            'label': label,
            'header': header
        })
        
        # Focus sul nuovo campo
        text_widget.focus_set()
        
    def auto_resize_text(self, text_widget):
        # Calcola l'altezza necessaria in base al contenuto
        lines = text_widget.get("1.0", "end-1c").split('\n')
        num_lines = len(lines)
        
        # Calcola anche le linee wrapped
        widget_width = text_widget.winfo_width()
        if widget_width > 1:  # Widget già renderizzato
            char_width = 8  # Larghezza media carattere
            chars_per_line = widget_width // char_width
            
            total_lines = 0
            for line in lines:
                if line:
                    wrapped_lines = (len(line) // chars_per_line) + 1
                    total_lines += wrapped_lines
                else:
                    total_lines += 1
                    
            num_lines = max(num_lines, total_lines)
        
        # Imposta altezza minima 3, massima 15
        new_height = max(3, min(num_lines + 1, 15))
        text_widget.config(height=new_height)
        
        # Aggiorna scroll region
        self.on_frame_configure()
        
    def on_text_focus(self, text_widget):
        # Scorri per rendere visibile il widget focused
        self.root.after(100, lambda: self.scroll_to_widget(text_widget))
        
    def scroll_to_widget(self, widget):
        # Ottieni posizione del widget nel canvas
        widget_top = widget.winfo_rooty()
        canvas_top = self.canvas.winfo_rooty()
        relative_top = widget_top - canvas_top
        
        canvas_height = self.canvas.winfo_height()
        
        if relative_top < 0 or relative_top > canvas_height - 100:
            # Scorri per centrare il widget
            total_height = self.scrollable_frame.winfo_reqheight()
            if total_height > 0:
                fraction = relative_top / total_height
                self.canvas.yview_moveto(max(0, fraction - 0.1))
    
    def remove_instruction(self, index):
        if index < len(self.instruction_widgets):
            # Rimuovi il frame
            self.instruction_widgets[index]['frame'].destroy()
            # Rimuovi dall'array
            self.instruction_widgets.pop(index)
            # Rinumera le istruzioni rimanenti
            self.renumber_instructions()
            # Aggiorna scroll region
            self.on_frame_configure()
    
    def renumber_instructions(self):
        for i, inst in enumerate(self.instruction_widgets):
            inst['label'].config(text=f"Istruzione {i+1}:")
            
            # Aggiorna i bottoni rimuovi
            for child in inst['header'].winfo_children():
                if isinstance(child, ttk.Button) and "Rimuovi" in child.cget('text'):
                    child.destroy()
                    
            if i > 0:  # Non il primo
                remove_btn = ttk.Button(inst['header'], text="❌ Rimuovi",
                                       command=lambda idx=i: self.remove_instruction(idx),
                                       style='Small.TButton')
                remove_btn.pack(side=tk.RIGHT, padx=(10, 0))
    
    def setup_automation_frame(self, parent, row):
        # Card per automazione
        auto_card = ttk.Frame(parent, style='Card.TFrame')
        auto_card.grid(row=row, column=0, sticky="ew", pady=(0, 0))
        
        # Padding interno
        auto_inner = ttk.Frame(auto_card, style='Card.TFrame')
        auto_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Titolo sezione
        auto_title = ttk.Label(auto_inner, text="⚙️ Controlli Automazione", style='Subtitle.TLabel')
        auto_title.pack(anchor='w', pady=(0, 10))
        
        # Frame controlli
        controls_frame = ttk.Frame(auto_inner, style='Card.TFrame')
        controls_frame.pack(fill=tk.X)
        
        # Timer
        timer_frame = ttk.Frame(controls_frame, style='Card.TFrame')
        timer_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(timer_frame, text="Timer (secondi):", style='Modern.TLabel').pack(anchor='w')
        self.timer_var = tk.StringVar(value="300")
        timer_entry = tk.Entry(timer_frame, textvariable=self.timer_var, width=10,
                              bg=self.text_bg, fg='white', insertbackground='white',
                              font=('Segoe UI', 11), relief=tk.FLAT, bd=5)
        timer_entry.pack(pady=(5, 0))
        ttk.Label(timer_frame, text="(5 minuti = 300 secondi)", style='Modern.TLabel',
                 font=('Segoe UI', 9, 'italic')).pack()
        
        # Bottone avvio
        button_frame = ttk.Frame(controls_frame, style='Card.TFrame')
        button_frame.pack(side=tk.LEFT, padx=20)
        
        self.automation_button = ttk.Button(button_frame, text="▶ Avvia Automazione",
                                          command=self.toggle_automation,
                                          style='Success.TButton')
        self.automation_button.pack()
        
        self.resume_label = ttk.Label(button_frame, text="", style='Modern.TLabel',
                                     font=('Segoe UI', 9, 'italic'))
        self.resume_label.pack(pady=(5, 0))
        
        # Status
        status_frame = ttk.Frame(controls_frame, style='Card.TFrame')
        status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.status_label = ttk.Label(status_frame, text="✓ Sistema pronto", style='Modern.TLabel',
                                     font=('Segoe UI', 11))
        self.status_label.pack(anchor='w')
        
        self.progress_label = ttk.Label(status_frame, text="", style='Modern.TLabel',
                                       font=('Segoe UI', 10, 'italic'))
        self.progress_label.pack(anchor='w')
        
    def start_coordinate_recording(self, coord_type):
        if self.is_recording:
            messagebox.showwarning("Attenzione", "Registrazione già in corso!")
            return
            
        self.is_recording = True
        self.current_recording_type = coord_type
        
        # Minimizza temporaneamente la finestra per non interferire
        self.root.iconify()
        time.sleep(0.3)
        
        # Aggiorna UI
        if coord_type == 'start':
            self.status_label.config(text="🔴 Muovi il mouse e premi SPAZIO per Campo Start")
        else:
            self.status_label.config(text="🔴 Muovi il mouse e premi SPAZIO per Campo Artifact")
        
        # Avvia listeners
        self.mouse_listener = mouse.Listener(on_move=self.on_mouse_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
    def on_mouse_move(self, x, y):
        self.current_mouse_position = (x, y)
        
    def on_key_press(self, key):
        if key == keyboard.Key.space and hasattr(self, 'current_mouse_position'):
            x, y = self.current_mouse_position
            
            if self.current_recording_type == 'start':
                self.start_coordinates = (x, y)
                self.start_label.config(text=f"X: {x}, Y: {y}")
            else:
                self.artifact_coordinates = (x, y)
                self.artifact_label.config(text=f"X: {x}, Y: {y}")
            
            self.stop_recording()
            self.status_label.config(text=f"✓ Coordinate {self.current_recording_type} registrate!")
            
            # Ripristina la finestra
            self.root.deiconify()
            self.root.lift()
            
        elif key == keyboard.Key.esc:
            self.stop_recording()
            self.status_label.config(text="✗ Registrazione annullata")
            self.root.deiconify()
            self.root.lift()
            
    def stop_recording(self):
        self.is_recording = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            
    def toggle_automation(self):
        if not self.is_automation_running:
            self.start_automation()
        else:
            self.stop_automation()
            
    def start_automation(self):
        # Validazioni
        if not self.start_coordinates or not self.artifact_coordinates:
            messagebox.showerror("Errore", "Devi prima registrare entrambe le coordinate!")
            return
            
        # Raccogli istruzioni
        self.instructions = []
        for inst in self.instruction_widgets:
            text = inst['text'].get("1.0", tk.END).strip()
            if text:
                self.instructions.append(text)
                
        if not self.instructions:
            messagebox.showerror("Errore", "Devi inserire almeno un'istruzione!")
            return
            
        try:
            timer_seconds = int(self.timer_var.get())
            if timer_seconds < 1:
                raise ValueError("Timer deve essere almeno 1 secondo")
        except ValueError as e:
            messagebox.showerror("Errore", "Il timer deve essere un numero valido di secondi!")
            return
            
        # Avvia automazione
        self.is_automation_running = True
        self.automation_button.configure(text="⏹ Ferma Automazione", style='Danger.TButton')
        self.status_label.config(text="⚡ Automazione in corso...")
        
        # Thread per automazione
        self.automation_thread = threading.Thread(target=self.run_automation, args=(timer_seconds,))
        self.automation_thread.daemon = True
        self.automation_thread.start()
        
    def run_automation(self, timer_seconds):
        try:
            total_instructions = len(self.instructions)
            
            # Se partiamo dall'inizio, esegui la prima istruzione nel campo start
            if self.current_instruction_index == 0 and self.instructions:
                self.update_progress(1, total_instructions, "Inserimento prima istruzione...")
                
                pyautogui.click(self.start_coordinates[0], self.start_coordinates[1])
                time.sleep(0.5)
                pyautogui.typewrite(self.instructions[0])
                time.sleep(0.1)
                pyautogui.press('enter')
                
                self.current_instruction_index = 1
                
            # Istruzioni successive nel campo artifact
            for i in range(self.current_instruction_index, len(self.instructions)):
                if not self.is_automation_running:
                    break
                
                # Countdown visivo
                for remaining in range(timer_seconds, 0, -1):
                    if not self.is_automation_running:
                        break
                        
                    self.update_progress(i + 1, total_instructions, 
                                       f"Prossima istruzione tra {remaining} secondi...")
                    time.sleep(1)
                
                if not self.is_automation_running:
                    break
                
                self.update_progress(i + 1, total_instructions, "Inserimento in corso...")
                
                pyautogui.click(self.artifact_coordinates[0], self.artifact_coordinates[1])
                time.sleep(0.5)
                pyautogui.typewrite(self.instructions[i])
                time.sleep(0.1)
                pyautogui.press('enter')
                
                self.current_instruction_index = i + 1
                
            # Automazione completata
            if self.is_automation_running and self.current_instruction_index >= len(self.instructions):
                self.root.after(0, self.automation_completed)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Errore", f"Errore durante l'automazione: {str(e)}"))
            self.root.after(0, self.stop_automation)
            
    def update_progress(self, current, total, message):
        self.root.after(0, lambda: self.progress_label.config(
            text=f"Istruzione {current} di {total} - {message}"))
            
    def automation_completed(self):
        self.is_automation_running = False
        self.is_automation_paused = False
        self.current_instruction_index = 0
        self.automation_button.configure(text="▶ Avvia Automazione", style='Success.TButton')
        self.status_label.config(text="✓ Automazione completata!")
        self.progress_label.config(text="")
        self.resume_label.config(text="")
        messagebox.showinfo("Completato", "Automazione completata con successo!")
        
    def save_instructions(self):
        # Raccogli le istruzioni attuali
        instructions_to_save = []
        for inst in self.instruction_widgets:
            text = inst['text'].get("1.0", tk.END).strip()
            if text:
                instructions_to_save.append(text)
                
        if not instructions_to_save:
            messagebox.showwarning("Attenzione", "Nessuna istruzione da salvare!")
            return
            
        # Dialog per salvare il file
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")],
            title="Salva Istruzioni"
        )
        
        if filename:
            try:
                data = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'instructions': instructions_to_save,
                    'timer_seconds': self.timer_var.get(),
                    'coordinates': {
                        'start': self.start_coordinates,
                        'artifact': self.artifact_coordinates
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    
                messagebox.showinfo("Successo", f"Istruzioni salvate in:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nel salvataggio: {str(e)}")
                
    def load_instructions(self):
        # Dialog per aprire il file
        filename = filedialog.askopenfilename(
            filetypes=[("File JSON", "*.json"), ("Tutti i file", "*.*")],
            title="Carica Istruzioni"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Chiedi se caricare anche le coordinate
                load_coords = messagebox.askyesno(
                    "Carica Coordinate",
                    "Vuoi caricare anche le coordinate salvate?\n\n"
                    "Sì = Carica tutto\n"
                    "No = Carica solo le istruzioni"
                )
                
                # Carica coordinate se richiesto
                if load_coords and 'coordinates' in data:
                    if data['coordinates'].get('start'):
                        self.start_coordinates = tuple(data['coordinates']['start'])
                        self.start_label.config(text=f"X: {self.start_coordinates[0]}, Y: {self.start_coordinates[1]}")
                    if data['coordinates'].get('artifact'):
                        self.artifact_coordinates = tuple(data['coordinates']['artifact'])
                        self.artifact_label.config(text=f"X: {self.artifact_coordinates[0]}, Y: {self.artifact_coordinates[1]}")
                        
                # Carica timer se presente
                if 'timer_seconds' in data:
                    self.timer_var.set(data['timer_seconds'])
                    
                # Rimuovi tutti i campi esistenti
                for widget in self.instruction_widgets:
                    widget['frame'].destroy()
                self.instruction_widgets.clear()
                
                # Carica le istruzioni
                instructions = data.get('instructions', [])
                if not instructions:
                    messagebox.showwarning("Attenzione", "Nessuna istruzione trovata nel file!")
                    self.add_instruction_field()
                    return
                    
                # Crea i campi per ogni istruzione
                for instruction in instructions:
                    self.add_instruction_field()
                    # Inserisci il testo nell'ultimo campo aggiunto
                    self.instruction_widgets[-1]['text'].insert("1.0", instruction)
                    # Trigger auto-resize
                    self.auto_resize_text(self.instruction_widgets[-1]['text'])
                    
                messagebox.showinfo("Successo", f"Caricate {len(instructions)} istruzioni da:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore nel caricamento: {str(e)}")
                # Assicurati che ci sia almeno un campo
                if not self.instruction_widgets:
                    self.add_instruction_field()
        
    def stop_automation(self):
        self.is_automation_running = False
        self.automation_button.configure(text="▶ Avvia Automazione", style='Success.TButton')
        self.status_label.config(text="✗ Automazione interrotta")
        self.progress_label.config(text="")


if __name__ == '__main__':
    root = tk.Tk()
    app = ModernAutomationSystem(root)
    root.mainloop()
