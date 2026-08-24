import tkinter as tk

from editor import Editor


class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mini CAD - Stack")
        self.root.geometry("1100x650")
        self.root.configure(bg="#1e1f24")
        self.root.minsize(1000, 600)

        self.editor = Editor()
        self.status_var = tk.StringVar(value="Estado: Esperando la primera acción")

        self._build_interface()

    def _build_interface(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        top_bar = tk.Frame(self.root, bg="#2a2d35", padx=18, pady=16)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

        title = tk.Label(
            top_bar,
            text="MINI CAD - STACK",
            font=("Arial", 18, "bold"),
            fg="#f5f5f5",
            bg="#2a2d35",
        )
        title.pack(anchor="w")

        buttons_frame = tk.Frame(top_bar, bg="#2a2d35")
        buttons_frame.pack(fill="x", pady=(12, 0))

        self._create_button(buttons_frame, "Línea", lambda: self.create_figure("line"), "#7dd3fc")
        self._create_button(buttons_frame, "Círculo", lambda: self.create_figure("circle"), "#a7f3d0")
        self._create_button(buttons_frame, "Rectángulo", lambda: self.create_figure("rectangle"), "#f9a8d4")
        self._create_button(buttons_frame, "Eliminar", self.delete_selected, "#fca5a5")
        self._create_button(buttons_frame, "Undo", self.undo_action, "#fbbf24")
        self._create_button(buttons_frame, "Redo", self.redo_action, "#c4b5fd")
        self._create_button(buttons_frame, "Limpiar", self.clear_all, "#94a3b8")

        work_area = tk.Frame(self.root, bg="#1e1f24")
        work_area.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))

        self.canvas = tk.Canvas(
            work_area,
            width=740,
            height=520,
            bg="#111318",
            highlightbackground="#3b3f46",
            highlightthickness=2,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.editor.canvas = self.canvas

        right_panel = tk.Frame(self.root, bg="#2a2d35", padx=16, pady=16)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

        history_title = tk.Label(
            right_panel,
            text="Historial",
            font=("Arial", 15, "bold"),
            fg="#ffffff",
            bg="#2a2d35",
        )
        history_title.pack(anchor="w")

        self.history_listbox = tk.Listbox(
            right_panel,
            height=14,
            bg="#1f232a",
            fg="#e5e7eb",
            highlightthickness=0,
            bd=0,
            activestyle="none",
            font=("Arial", 11),
        )
        self.history_listbox.pack(fill="both", expand=True, pady=(12, 10))

        info_frame = tk.Frame(right_panel, bg="#2a2d35")
        info_frame.pack(fill="x")

        self.undo_label = tk.Label(
            info_frame,
            text="Undo: 0",
            fg="#fcd34d",
            bg="#2a2d35",
            font=("Arial", 11, "bold"),
        )
        self.undo_label.pack(anchor="w", pady=(4, 0))

        self.redo_label = tk.Label(
            info_frame,
            text="Redo: 0",
            fg="#c4b5fd",
            bg="#2a2d35",
            font=("Arial", 11, "bold"),
        )
        self.redo_label.pack(anchor="w")

        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#2a2d35",
            fg="#e5e7eb",
            anchor="w",
            padx=20,
            pady=12,
            font=("Arial", 11),
        )
        status_bar.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.refresh_history()

    def _create_button(self, parent, text, command, color):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="#111827",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=8,
            bd=0,
            cursor="hand2",
        )
        button.pack(side="left", padx=(0, 8), pady=4)

    def on_canvas_click(self, event):
        item_id = self.canvas.find_closest(event.x, event.y)
        if not item_id:
            return

        current_item_id = item_id[0]
        figure = self._find_figure_by_item(current_item_id)
        if figure is None:
            return

        self.editor.selected_figure_id = figure.id
        self.status_var.set(f"Estado: Figura seleccionada → {figure.type.upper()}")

    def _find_figure_by_item(self, item_id):
        for figure in self.editor.figures.values():
            if figure.canvas_item_id == item_id:
                return figure
        return None

    def create_figure(self, figure_type):
        self.editor.create_figure(figure_type)
        self.status_var.set(f"Estado: Última acción → CREATE {figure_type.upper()}")
        self.refresh_history()

    def delete_selected(self):
        if self.editor.delete_figure():
            self.status_var.set("Estado: Última acción → DELETE")
            self.refresh_history()
        else:
            self.status_var.set("Estado: Debes seleccionar una figura antes de eliminar")

    def undo_action(self):
        if self.editor.undo():
            action = self.editor.undo_stack.peek()
            if action is not None:
                self.status_var.set(f"Estado: Última acción → {action.description}")
            else:
                self.status_var.set("Estado: Sin acciones en el historial")
            self.refresh_history()
        else:
            self.status_var.set("Estado: No hay acciones para hacer Undo")

    def redo_action(self):
        if self.editor.redo():
            action = self.editor.undo_stack.peek()
            if action is not None:
                self.status_var.set(f"Estado: Última acción → {action.description}")
            else:
                self.status_var.set("Estado: Sin acciones en el historial")
            self.refresh_history()
        else:
            self.status_var.set("Estado: No hay acciones para hacer Redo")

    def clear_all(self):
        self.editor.clear()
        self.status_var.set("Estado: Canvas limpiado y historiales reiniciados")
        self.refresh_history()

    def refresh_history(self):
        self.history_listbox.delete(0, tk.END)

        actions = list(reversed(self.editor.undo_stack.items))
        if not actions:
            self.history_listbox.insert(tk.END, "Sin acciones")
        else:
            for index, action in enumerate(actions):
                if index == 0:
                    self.history_listbox.insert(tk.END, f"TOP -> {action.description}")
                else:
                    self.history_listbox.insert(tk.END, action.description)

        self.undo_label.config(text=f"Undo: {self.editor.undo_stack.size()}")
        self.redo_label.config(text=f"Redo: {self.editor.redo_stack.size()}")

        if self.editor.undo_stack.peek() is not None:
            self.status_var.set(f"Estado: Última acción → {self.editor.undo_stack.peek().description}")

    def run(self):
        self.root.mainloop()
