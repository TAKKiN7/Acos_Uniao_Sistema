import customtkinter as ctk
from tkinter import messagebox

class NotasCTEFrame(ctk.CTkFrame):
    """
    Frame referente à aba 'Notas CTE'.
    Contém instruções de validação de CT-e e campo para data de vencimento.
    Modo claro ajustado para tom cinza suave e elegante.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))

        self.lbl_modulo = ctk.CTkLabel(
            self.header_frame,
            text="LOGÍSTICA & TRANSPORTE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_modulo.pack(anchor="w")

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="Gestão de Notas CTE",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", pady=(2, 0))

        # Main Layout Container (2 Columns)
        self.content_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.content_grid.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.content_grid.grid_columnconfigure(0, weight=4)
        self.content_grid.grid_columnconfigure(1, weight=5)

        # Left Card - Instructions (Cinza Suave no modo claro)
        self.left_card = ctk.CTkFrame(
            self.content_grid,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)

        self.lbl_inst_title = ctk.CTkLabel(
            self.left_card,
            text="Instruções",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_inst_title.pack(anchor="w", padx=25, pady=(25, 10))

        self.lbl_inst_desc = ctk.CTkLabel(
            self.left_card,
            text="Insira a data de vencimento correspondente para sincronizar o manifesto de transporte e validar os Conhecimentos de Transporte Eletrônicos (CT-e).",
            font=ctk.CTkFont(size=13),
            text_color=("#1E293B", "#9CA3AF"),
            wraplength=280,
            justify="left"
        )
        self.lbl_inst_desc.pack(anchor="w", padx=25, pady=(0, 40))

        # Status Box at bottom of left card
        self.status_box = ctk.CTkFrame(
            self.left_card,
            fg_color=("#E2E8F0", "#171A1F"),
            corner_radius=8,
            border_color=("#94A3B8", "#252A34"),
            border_width=1
        )
        self.status_box.pack(fill="x", padx=25, pady=(0, 25), side="bottom")

        self.lbl_status = ctk.CTkLabel(
            self.status_box,
            text="STATUS DO SERVIDOR  • ONLINE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#047857", "#10B981")
        )
        self.lbl_status.pack(padx=15, pady=10, anchor="w")

        # Right Card - Form (Cinza Suave no modo claro)
        self.right_card = ctk.CTkFrame(
            self.content_grid,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.right_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=0)

        self.lbl_date_label = ctk.CTkLabel(
            self.right_card,
            text="DATA DE VENCIMENTO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_date_label.pack(anchor="w", padx=30, pady=(35, 8))

        # Entry for Date (Campo Cinza Suave)
        self.entry_date = ctk.CTkEntry(
            self.right_card,
            placeholder_text="📅  DD/MM/AAAA",
            font=ctk.CTkFont(size=14),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#475569", "#6B7280"),
            height=45,
            corner_radius=8
        )
        self.entry_date.pack(fill="x", padx=30, pady=(0, 5))

        self.lbl_format_hint = ctk.CTkLabel(
            self.right_card,
            text="FORMATO REQUERIDO: DIA/MÊS/ANO",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("#334155", "#6B7280")
        )
        self.lbl_format_hint.pack(anchor="w", padx=30, pady=(0, 30))

        # Action Button (Blue INICIAR)
        self.btn_iniciar = ctk.CTkButton(
            self.right_card,
            text="INICIAR  ▶",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=50,
            corner_radius=8,
            command=self.processar_inicio
        )
        self.btn_iniciar.pack(fill="x", padx=30, pady=(0, 35))

    def processar_inicio(self):
        data = self.entry_date.get().strip()
        if not data:
            messagebox.showwarning("Campo Vazio", "Por favor, insira a data de vencimento.")
        else:
            messagebox.showinfo("Processamento Iniciado", f"Manifesto sincronizado para a data: {data}")
