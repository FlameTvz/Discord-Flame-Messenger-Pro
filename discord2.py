import pyautogui
import time
import threading
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkFont
import datetime

CONFIG_FILE = "discord_config.json"

class ModernButton(tk.Button):
    def __init__(self, parent, text, command, bg_color="#FF4655", hover_color="#FF6B73", **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.bg_color = bg_color
        self.hover_color = hover_color

        self.configure(
            bg=bg_color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(bg=self.hover_color)

    def on_leave(self, e):
        self.configure(bg=self.bg_color)

class ModernDialog:
    def __init__(self, parent, title, fields, initial_values=None):
        self.parent = parent
        self.result = None
        self.entries = []
        
        # Criar janela modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x600")  # Aumentei a altura para acomodar o scroll
        self.dialog.configure(bg="#0F0F0F")
        self.dialog.resizable(False, False)
        
        # Sempre em cima e modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.lift()
        self.dialog.focus_force()
        
        # Centralizar na tela
        self.center_window()
        
        # Cores
        self.colors = {
            'bg_primary': '#0F0F0F',
            'bg_secondary': '#1A1A1A',
            'bg_tertiary': '#2C2F33',
            'accent': '#FF4655',
            'accent_hover': '#FF6B73',
            'text_primary': '#FFFFFF',
            'text_secondary': '#AAAAAA',
            'success': '#00FFB3',
            'input_bg': '#2C2F33',
            'input_border': '#404040'
        }
        
        self.create_widgets(title, fields, initial_values)
        
        # Bind para fechar com ESC
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        self.dialog.bind('<Return>', lambda e: self.ok())
        
        # Protocolo para fechar janela
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def center_window(self):
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self, title, fields, initial_values):
        # Container principal
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título com ícone
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_primary']
        ).pack()
        
        # Linha decorativa
        line = tk.Frame(title_frame, height=2, bg=self.colors['accent'])
        line.pack(fill='x', pady=(10, 0))
        
        # ===== ÁREA COM SCROLL =====
        # Frame container para o canvas e scrollbar
        scroll_container = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        scroll_container.pack(fill='both', expand=True, pady=(0, 20))
        
        # Canvas para scroll
        self.canvas = tk.Canvas(
            scroll_container,
            bg=self.colors['bg_secondary'],
            highlightthickness=0,
            bd=0
        )
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        
        # Frame que vai conter os campos
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_secondary'])
        
        # Configurar scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Criar janela no canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configurar scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind para ajustar largura
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Bind do mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Pack canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Padding interno no frame scrollable
        inner_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'])
        inner_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Criar campos de entrada
        for i, field in enumerate(fields):
            field_container = tk.Frame(inner_frame, bg=self.colors['bg_secondary'])
            field_container.pack(fill='x', pady=(0, 15))
            
            # Label do campo
            label = tk.Label(
                field_container,
                text=field,
                font=("Segoe UI", 11, "bold"),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']
            )
            label.pack(anchor='w', pady=(0, 5))
            
            # Frame para o campo de entrada com borda
            entry_frame = tk.Frame(field_container, bg=self.colors['input_border'], relief='solid', bd=1)
            entry_frame.pack(fill='x')
            
            # Campo de entrada
            entry = tk.Entry(
                entry_frame,
                font=("Segoe UI", 12),
                bg=self.colors['input_bg'],
                fg=self.colors['text_primary'],
                insertbackground=self.colors['text_primary'],
                bd=0,
                relief='flat'
            )
            entry.pack(fill='x', padx=2, pady=2, ipady=8)
            
            # Valor inicial se fornecido
            if initial_values and i < len(initial_values):
                entry.insert(0, str(initial_values[i]))
            
            # Efeitos de foco
            entry.bind('<FocusIn>', lambda e, frame=entry_frame: frame.config(bg=self.colors['accent']))
            entry.bind('<FocusOut>', lambda e, frame=entry_frame: frame.config(bg=self.colors['input_border']))
            
            self.entries.append(entry)
        
        # Focar no primeiro campo
        if self.entries:
            self.entries[0].focus_set()
        
        # Atualizar scroll region após criar todos os campos
        self.dialog.after(100, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Frame para botões (fora da área de scroll)
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill='x')
        
        # Botão Cancelar
        cancel_btn = ModernButton(
            button_frame,
            "❌ Cancelar",
            self.cancel,
            bg_color="#6C757D",
            hover_color="#868E96"
        )
        cancel_btn.pack(side='right', padx=(10, 0))
        
        # Botão OK
        ok_btn = ModernButton(
            button_frame,
            "✅ Confirmar",
            self.ok,
            bg_color="#28A745",
            hover_color="#34CE57"
        )
        ok_btn.pack(side='right')
        
        # Adicionar dica de teclas
        hint_label = tk.Label(
            main_frame,
            text="💡 Dica: Use Enter para confirmar ou Esc para cancelar | Use a roda do mouse para fazer scroll",
            font=("Segoe UI", 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        hint_label.pack(pady=(10, 0))
    
    def on_canvas_configure(self, event):
        # Atualizar a largura do frame interno para corresponder ao canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def _on_mousewheel(self, event):
        # Verificar se o mouse está sobre o canvas
        if self.canvas.winfo_containing(event.x_root, event.y_root) == self.canvas:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def ok(self):
        values = []
        for entry in self.entries:
            value = entry.get().strip()
            if not value:
                messagebox.showerror("❌ Erro", "Todos os campos devem ser preenchidos!", parent=self.dialog)
                return
            try:
                values.append(int(value))
            except ValueError:
                messagebox.showerror("❌ Erro", "Por favor, digite apenas números válidos!", parent=self.dialog)
                return
        
        self.result = values
        self.dialog.destroy()
    
    def cancel(self):
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        self.dialog.wait_window()
        return self.result

class DiscordBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Flame Messenger Pro")
        self.root.geometry("900x700")
        self.root.configure(bg="#0F0F0F")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)

        self.colors = {
            'bg_primary': '#0F0F0F',
            'bg_secondary': '#1A1A1A',
            'bg_tertiary': '#2C2F33',
            'accent': '#FF4655',
            'accent_hover': '#FF6B73',
            'text_primary': '#FFFFFF',
            'text_secondary': '#AAAAAA',
            'success': '#00FFB3',
            'warning': '#FFA500',
            'error': '#FF4655'
        }

        self.coordenadas = []
        self.mensagem = "alg pra jogar ap, rpd"
        self.pause_minutes = 10
        self.running = False
        self.mouse_position = tk.StringVar()
        self.status_text = tk.StringVar()
        self.status_text.set("Status: Parado")

        self.load_config()
        self.create_widgets()
        self.track_mouse_position()
        self.update_status_display()

    def create_widgets(self):
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Criar o canvas com scrollbar otimizado
        self.canvas = tk.Canvas(
            main_container, 
            bg=self.colors['bg_primary'], 
            highlightthickness=0,
            bd=0
        )
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        
        # Frame que vai conter todo o conteúdo
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_primary'])

        # Configurar o scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Criar a janela no canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configurar a scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Bind para redimensionar o frame interno quando a janela muda de tamanho
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        # Bind do mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Pack do canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Criar todas as seções
        self.create_header()
        self.create_mouse_section()
        self.create_message_section()
        self.create_pause_section()
        self.create_coordinates_section()
        self.create_controls_section()
        self.create_status_section()

    def on_canvas_configure(self, event):
        # Atualizar a largura do frame interno para corresponder ao canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_header(self):
        frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_primary'])
        frame.pack(fill='x', pady=(0, 20))

        tk.Label(
            frame,
            text="🔥 Discord Flame Messenger Pro",
            font=("Segoe UI", 20, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_primary']
        ).pack()

        tk.Label(
            frame,
            text="Automatização inteligente de mensagens",
            font=("Segoe UI", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        ).pack(pady=(5, 0))

    def create_mouse_section(self):
        mouse_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        mouse_frame.pack(fill='x', pady=(0, 15))
        
        # Título da seção
        tk.Label(
            mouse_frame,
            text="📍 Posição do Mouse",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(pady=(10, 5))
        
        # Posição atual
        tk.Label(
            mouse_frame,
            textvariable=self.mouse_position,
            font=("Consolas", 12, "bold"),
            fg=self.colors['success'],
            bg=self.colors['bg_secondary']
        ).pack(pady=(0, 10))

    def create_message_section(self):
        msg_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        msg_frame.pack(fill='x', pady=(0, 15))
        
        # Título da seção
        tk.Label(
            msg_frame,
            text="💬 Configuração da Mensagem",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(pady=(10, 5))
        
        # Campo de entrada da mensagem
        entry_frame = tk.Frame(msg_frame, bg=self.colors['bg_secondary'])
        entry_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        self.msg_entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 11),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            bd=0,
            relief='flat'
        )
        self.msg_entry.insert(0, self.mensagem)
        self.msg_entry.pack(fill='x', ipady=8)

    def create_pause_section(self):
        pause_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        pause_frame.pack(fill='x', pady=(0, 15))
        
        # Título da seção
        tk.Label(
            pause_frame,
            text="⏰ Tempo de Pausa Entre Ciclos",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(pady=(10, 5))
        
        # Configuração do tempo
        time_config_frame = tk.Frame(pause_frame, bg=self.colors['bg_secondary'])
        time_config_frame.pack(pady=(0, 10))
        
        tk.Label(
            time_config_frame,
            text="Intervalo (minutos):",
            font=("Segoe UI", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left', padx=(0, 10))
        
        self.pause_entry = tk.Entry(
            time_config_frame,
            font=("Segoe UI", 11),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            bd=0,
            relief='flat',
            width=8,
            justify='center'
        )
        self.pause_entry.insert(0, str(self.pause_minutes))
        self.pause_entry.pack(side='left', ipady=5)
        
        tk.Label(
            time_config_frame,
            text="minutos",
            font=("Segoe UI", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        ).pack(side='left', padx=(10, 20))
        
        # Botão para aplicar o tempo
        apply_btn = ModernButton(
            time_config_frame,
            "✅ Aplicar",
            self.apply_pause_time,
            bg_color="#4CAF50",
            hover_color="#66BB6A"
        )
        apply_btn.pack(side='left')
        
        # Exibir tempo atual
        self.current_pause_label = tk.Label(
            pause_frame,
            text=f"Tempo atual: {self.pause_minutes} minutos",
            font=("Segoe UI", 9),
            fg=self.colors['warning'],
            bg=self.colors['bg_secondary']
        )
        self.current_pause_label.pack(pady=(0, 10))

    def create_coordinates_section(self):
        coord_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        coord_frame.pack(fill='x', pady=(0, 15))
        
        # Título da seção
        tk.Label(
            coord_frame,
            text="🎯 Coordenadas Salvas",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(pady=(10, 5))
        
        # Lista de coordenadas
        list_frame = tk.Frame(coord_frame, bg=self.colors['bg_secondary'])
        list_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        # Scrollbar para a lista
        list_scrollbar = tk.Scrollbar(list_frame)
        list_scrollbar.pack(side='right', fill='y')
        
        self.coord_list = tk.Listbox(
            list_frame,
            font=("Consolas", 9),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground='white',
            bd=0,
            relief='flat',
            yscrollcommand=list_scrollbar.set,
            height=5
        )
        self.coord_list.pack(fill='x', side='left', expand=True)
        list_scrollbar.config(command=self.coord_list.yview)
        
        # Botões de gerenciamento
        btn_frame = tk.Frame(coord_frame, bg=self.colors['bg_secondary'])
        btn_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        # Linha 1 de botões
        btn_row1 = tk.Frame(btn_frame, bg=self.colors['bg_secondary'])
        btn_row1.pack(fill='x', pady=(0, 5))
        
        ModernButton(btn_row1, "➕ Adicionar", self.add_coordinate).pack(side='left', padx=(0, 5))
        ModernButton(btn_row1, "📝 Editar", self.edit_coordinate, bg_color="#4CAF50", hover_color="#66BB6A").pack(side='left', padx=(0, 5))
        ModernButton(btn_row1, "🗑️ Remover", self.remove_coordinate, bg_color="#F44336", hover_color="#E57373").pack(side='left')
        
        # Linha 2 de botões
        btn_row2 = tk.Frame(btn_frame, bg=self.colors['bg_secondary'])
        btn_row2.pack(fill='x')
        
        ModernButton(btn_row2, "🧹 Limpar Tudo", self.clear_coordinates, bg_color="#FF9800", hover_color="#FFB74D").pack(side='left', padx=(0, 5))
        ModernButton(btn_row2, "💾 Salvar", self.save_config, bg_color="#9C27B0", hover_color="#BA68C8").pack(side='left')

    def create_controls_section(self):
        control_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        control_frame.pack(fill='x', pady=(0, 15))

        tk.Label(
            control_frame,
            text="🎮 Controles",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(pady=(10, 5))

        buttons_container = tk.Frame(control_frame, bg=self.colors['bg_secondary'])
        buttons_container.pack(pady=(0, 10))

        self.start_btn = ModernButton(
            buttons_container,
            "▶️ Iniciar Automação",
            self.start_automation,
            bg_color="#4CAF50",
            hover_color="#66BB6A"
        )
        self.start_btn.pack(side='left', padx=(0, 10))

        self.stop_btn = ModernButton(
            buttons_container,
            "⏹️ Parar Automação",
            self.stop_automation,
            bg_color="#F44336",
            hover_color="#E57373"
        )
        self.stop_btn.pack(side='left')
        self.stop_btn.configure(state='disabled')

    def create_status_section(self):
        status_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        status_frame.pack(fill='x', pady=(0, 10))
        
        # Título da seção
        tk.Label(
            status_frame,
            text="📊 Status do Sistema",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(pady=(10, 5))
        
        # Status atual
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_text,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        self.status_label.pack(pady=(0, 10))

    def apply_pause_time(self):
        try:
            new_pause = int(self.pause_entry.get())
            if new_pause < 1:
                messagebox.showerror("❌ Erro", "O tempo de pausa deve ser pelo menos 1 minuto.")
                return
            
            self.pause_minutes = new_pause
            self.current_pause_label.config(text=f"Tempo atual: {self.pause_minutes} minutos")
            self.save_config()
            messagebox.showinfo("✅ Sucesso", f"Tempo de pausa atualizado para {self.pause_minutes} minutos!")
        except ValueError:
            messagebox.showerror("❌ Erro", "Por favor, digite um número válido de minutos.")

    def track_mouse_position(self):
        try:
            x, y = pyautogui.position()
            self.mouse_position.set(f"X: {x:4d}  |  Y: {y:4d}")
        except Exception:
            self.mouse_position.set("Erro ao capturar posição")
        
        if not self.root.winfo_exists():
            return
        self.root.after(100, self.track_mouse_position)

    def update_status_display(self):
        if not self.root.winfo_exists():
            return
            
        if self.running:
            self.status_label.configure(fg=self.colors['success'])
        else:
            self.status_label.configure(fg=self.colors['text_secondary'])
        self.root.after(1000, self.update_status_display)

    def update_coords_list(self):
        self.coord_list.delete(0, tk.END)
        for i, (x1, y1, x2, y2) in enumerate(self.coordenadas):
            self.coord_list.insert(tk.END, f"{i+1:2d}. Aba({x1:4d},{y1:4d}) → Conversa({x2:4d},{y2:4d})")

    def add_coordinate(self):
        dialog = ModernDialog(
            self.root,
            "➕ Adicionar Nova Coordenada",
            [
                "🎯 Coordenada X da Aba:",
                "🎯 Coordenada Y da Aba:",
                "💬 Coordenada X da Conversa:",
                "💬 Coordenada Y da Conversa:"
            ]
        )
        
        result = dialog.show()
        if result:
            x1, y1, x2, y2 = result
            self.coordenadas.append((x1, y1, x2, y2))
            self.update_coords_list()
            self.save_config()
            messagebox.showinfo("✅ Sucesso", "Coordenada adicionada com sucesso!")

    def edit_coordinate(self):
        selection = self.coord_list.curselection()
        if not selection:
            messagebox.showwarning("⚠️ Aviso", "Selecione uma coordenada para editar.")
            return
        
        index = selection[0]
        old = self.coordenadas[index]
        
        dialog = ModernDialog(
            self.root,
            "📝 Editar Coordenada",
            [
                "🎯 Coordenada X da Aba:",
                "🎯 Coordenada Y da Aba:",
                "💬 Coordenada X da Conversa:",
                "💬 Coordenada Y da Conversa:"
            ],
            initial_values=old
        )
        
        result = dialog.show()
        if result:
            x1, y1, x2, y2 = result
            self.coordenadas[index] = (x1, y1, x2, y2)
            self.update_coords_list()
            self.save_config()
            messagebox.showinfo("✅ Sucesso", "Coordenada editada com sucesso!")

    def remove_coordinate(self):
        selection = self.coord_list.curselection()
        if selection:
            if messagebox.askyesno("🗑️ Confirmar", "Deseja remover a coordenada selecionada?"):
                index = selection[0]
                del self.coordenadas[index]
                self.update_coords_list()
                self.save_config()
                messagebox.showinfo("✅ Sucesso", "Coordenada removida com sucesso!")
        else:
            messagebox.showwarning("⚠️ Aviso", "Selecione uma coordenada para remover.")

    def clear_coordinates(self):
        if messagebox.askyesno("🧹 Confirmar", "Deseja remover TODAS as coordenadas?"):
            self.coordenadas.clear()
            self.update_coords_list()
            self.save_config()
            messagebox.showinfo("✅ Sucesso", "Todas as coordenadas foram removidas!")

    def start_automation(self):
        if not self.coordenadas:
            messagebox.showerror("❌ Erro", "Adicione ao menos uma coordenada antes de iniciar.")
            return
        
        self.mensagem = self.msg_entry.get().strip()
        if not self.mensagem:
            messagebox.showerror("❌ Erro", "A mensagem não pode estar vazia.")
            return

        self.running = True
        self.status_text.set("Status: Iniciando em 5 segundos...")
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        
        threading.Thread(target=self.automation_loop, daemon=True).start()

    def stop_automation(self):
        self.running = False
        self.status_text.set("Status: Parando...")
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self.status_text.set("Status: Parado")

    def automation_loop(self):
        # Countdown inicial
        for i in range(5, 0, -1):
            if not self.running:
                break
            self.status_text.set(f"Status: Iniciando em {i} segundos...")
            time.sleep(1)
        
        if not self.running:
            self.stop_automation()
            return
        
        cycle_count = 0
        while self.running:
            cycle_count += 1
            self.status_text.set(f"Status: Executando ciclo {cycle_count}...")
            
            for i, (x1, y1, x2, y2) in enumerate(self.coordenadas):
                if not self.running:
                    break
                
                self.status_text.set(f"Status: Processando coordenada {i+1}/{len(self.coordenadas)}")
                
                try:
                    # Clique na aba
                    pyautogui.click(x1, y1)
                    time.sleep(1)
                    
                    # Clique na conversa
                    pyautogui.click(x2, y2)
                    time.sleep(1)
                    
                    # Envio da mensagem
                    pyautogui.write(self.mensagem)
                    pyautogui.press('enter')
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Erro na automação: {e}")
                    continue
            
            # Aguarda o tempo configurado pelo usuário antes do próximo ciclo
            if self.running:
                pause_seconds = self.pause_minutes * 60
                for i in range(pause_seconds, 0, -1):
                    if not self.running:
                        break
                    
                    mins, secs = divmod(i, 60)
                    self.status_text.set(f"Status: Próximo ciclo em {mins:02d}:{secs:02d}")
                    time.sleep(1)
        
        self.stop_automation()

    def save_config(self):
        try:
            config_data = {
                'coordenadas': self.coordenadas,
                'mensagem': self.mensagem,
                'pause_minutes': self.pause_minutes,
                'saved_at': datetime.datetime.now().isoformat()
            }
            
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao salvar configurações:\n{str(e)}")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.coordenadas = data.get('coordenadas', [])
                    self.mensagem = data.get('mensagem', self.mensagem)
                    self.pause_minutes = data.get('pause_minutes', 10)
                    
                self.update_coords_list()
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")

if __name__ == '__main__':
    # Configuração inicial do pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    root = tk.Tk()
    app = DiscordBotApp(root)
    root.mainloop()