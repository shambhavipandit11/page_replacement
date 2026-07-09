import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("light")

class ClaymorphicSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Page Replacement Simulator & Academy")
        self.geometry("1280x880")
        
        self.theme = {
            "bg": "#F4F2F9",
            "sidebar_bg": "#9D8DF1",
            "card_bg": "#FFFFFF",
            "text_dark": "#2D2A4A",
            "text_light": "#FFFFFF",
            "sub_text": "#7E7A9A",
            "accent_purple": "#B8A6FF",
            "accent_pink": "#FFB5B5",
            "accent_yellow": "#FFEAA7",
            "accent_blue": "#A8DADC",
            "border_soft": "#E6E2FF"
        }
        
        self.algo_insights = {
            "FIFO": {
                "title": "💡 How FIFO (First-In, First-Out) Works:",
                "desc": "Evicts the oldest page residing in memory, tracking allocations like a strict FIFO queue. Simple layout with low computational overhead, but completely blind to reference trends. Vulnerable to Belady's Anomaly."
            },
            "LRU": {
                "title": "💡 How LRU (Least Recently Used) Works:",
                "desc": "Evicts the page unaccessed for the longest duration based on physical history tracking. Relies heavily on Temporal Locality. Highly efficient, though system overhead increases due to continuous counter updating."
            },
            "MRU": {
                "title": "💡 How MRU (Most Recently Used) Works:",
                "desc": "Evicts the page accessed most recently. Ideal for instances of scanning loops where recent data isn't needed immediately, preventing cache pollution from repetitive serial reads."
            },
            "OPTIMAL": {
                "title": "💡 How Optimal (MIN) Works:",
                "desc": "Evicts the page that will not be needed for the longest future window. Requires look-ahead execution tracking. Theoretically produces the lowest possible drop fault metric, acting as an absolute baseline model."
            },
            "COMPARE ALL": {
                "title": "📊 Multi-Model Performance Matrix Active",
                "desc": "Evaluating all four processing cores concurrently over identical reference string states. Review the cross-comparison chart below to observe how different cache tracking models scale against caching vulnerabilities under your current frame constraints."
            }
        }
        
        self.configure(fg_color=self.theme["bg"])
        self.create_layout()
        self.run_simulation()

    def create_layout(self):
        # Left Sidebar Panel
        self.sidebar = ctk.CTkFrame(self, fg_color=self.theme["sidebar_bg"], corner_radius=24, width=260)
        self.sidebar.pack(side="left", fill="y", padx=20, pady=20)
        self.sidebar.pack_propagate(False)
        
        # Identity Header
        profile_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_frame.pack(fill="x", padx=15, pady=(30, 25))
        ctk.CTkLabel(profile_frame, text="Page Replacement Algorithm", font=("Plus Jakarta Sans", 14, "bold"), text_color=self.theme["text_light"], wraplength=220, justify="left").pack(anchor="w", pady=(0, 12))
        
        divider = ctk.CTkFrame(profile_frame, fg_color="#B8A6FF", height=2)
        divider.pack(fill="x", pady=(0, 12))
        
        meta_items = [("BRANCH:", "CYBER SECURITY"), ("CORE DEV:", "SHAMBHAVI PANDIT"), ("STATION ID:", "CY062")]
        for label, val in meta_items:
            row = ctk.CTkFrame(profile_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=label, font=("Plus Jakarta Sans", 10, "bold"), text_color="#E6E2FF").pack(side="left")
            ctk.CTkLabel(row, text=val, font=("Courier New", 11, "bold"), text_color=self.theme["accent_yellow"] if label == "STATION ID:" else self.theme["text_light"]).pack(side="right")

        # Config Controls
        ctk.CTkLabel(self.sidebar, text="ALGORITHM", font=("Plus Jakarta Sans", 11, "bold"), text_color="#E6E2FF").pack(anchor="w", padx=25, pady=(10, 4))
        self.algo_var = tk.StringVar(value="FIFO")
        self.algo_combo = ctk.CTkComboBox(self.sidebar, values=["FIFO", "LRU", "MRU", "OPTIMAL", "COMPARE ALL"], variable=self.algo_var, fg_color=self.theme["card_bg"], text_color=self.theme["text_dark"], button_color=self.theme["accent_purple"], button_hover_color="#8675E0", border_width=0, corner_radius=12, height=40, font=("Plus Jakarta Sans", 12))
        self.algo_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(self.sidebar, text="NUMBER OF FRAMES", font=("Plus Jakarta Sans", 11, "bold"), text_color="#E6E2FF").pack(anchor="w", padx=25, pady=(10, 4))
        self.frames_var = tk.StringVar(value="3")
        self.frames_entry = ctk.CTkEntry(self.sidebar, textvariable=self.frames_var, fg_color=self.theme["card_bg"], text_color=self.theme["text_dark"], border_width=0, corner_radius=12, height=40, font=("Plus Jakarta Sans", 12))
        self.frames_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(self.sidebar, text="REFERENCE STRING", font=("Plus Jakarta Sans", 11, "bold"), text_color="#E6E2FF").pack(anchor="w", padx=25, pady=(10, 4))
        self.ref_var = tk.StringVar(value="7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1")
        self.ref_entry = ctk.CTkEntry(self.sidebar, textvariable=self.ref_var, fg_color=self.theme["card_bg"], text_color=self.theme["text_dark"], border_width=0, corner_radius=12, height=40, font=("Plus Jakarta Sans", 12))
        self.ref_entry.pack(fill="x", padx=20, pady=(0, 4))
        
        self.run_btn = ctk.CTkButton(self.sidebar, text="Execute Simulation", command=self.run_simulation, fg_color="#2D2A4A", hover_color="#1E1C33", text_color=self.theme["text_light"], font=("Plus Jakarta Sans", 13, "bold"), corner_radius=16, height=46)
        self.run_btn.pack(fill="x", padx=20, pady=(30, 0))

        # Main Workspace Stage Wrapper
        self.container_stage = ctk.CTkFrame(self, fg_color="transparent")
        self.container_stage.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)
        
        # Navigation Bar Layout
        nav_frame = ctk.CTkFrame(self.container_stage, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(10, 10))
        
        title_sub_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        title_sub_frame.pack(side="left")
        self.stage_title = ctk.CTkLabel(title_sub_frame, text="Dashboard Workspace", font=("Plus Jakarta Sans", 24, "bold"), text_color=self.theme["text_dark"])
        self.stage_title.pack(anchor="w")
        self.stage_sub = ctk.CTkLabel(title_sub_frame, text="Real-time virtual memory execution trace grid sandbox environment.", font=("Plus Jakarta Sans", 12), text_color=self.theme["sub_text"])
        self.stage_sub.pack(anchor="w")
        
        # Tab View Switch Controllers
        self.view_mode = "SIM"
        self.tab_container = ctk.CTkFrame(nav_frame, fg_color="#E6E2FF", corner_radius=14)
# (Padding is handled implicitly via child widget packing inside CustomTkinter instead)
        self.tab_container.pack(side="right", anchor="n", pady=5)
        
        self.sim_tab_btn = ctk.CTkButton(self.tab_container, text="Simulation Tool", width=110, height=32, corner_radius=10, fg_color=self.theme["card_bg"], text_color=self.theme["text_dark"], font=("Plus Jakarta Sans", 11, "bold"), command=lambda: self.toggle_tab_view("SIM"))
        self.sim_tab_btn.pack(side="left")
        
        self.theory_tab_btn = ctk.CTkButton(self.tab_container, text="Theory Academy", width=110, height=32, corner_radius=10, fg_color="transparent", text_color=self.theme["sub_text"], font=("Plus Jakarta Sans", 11, "bold"), command=lambda: self.toggle_tab_view("THEORY"))
        self.theory_tab_btn.pack(side="right")

        # Core View Windows Holders
        self.workspace_view_frame = ctk.CTkFrame(self.container_stage, fg_color="transparent")
        self.workspace_view_frame.pack(fill="both", expand=True)
        
        self.theory_view_frame = ctk.CTkFrame(self.container_stage, fg_color="transparent")
        
        self.build_simulation_workspace()
        self.build_theory_academy_workspace()

    def build_simulation_workspace(self):
        self.stats_frame = ctk.CTkFrame(self.workspace_view_frame, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=(10, 15))
        
        self.stat_cards = {}
        metrics_setup = [("Total Faults", self.theme["accent_pink"]), ("Total Hits", self.theme["accent_blue"]), ("Fault Ratio", self.theme["accent_yellow"]), ("Hit Ratio", self.theme["accent_purple"])]
        for name, color in metrics_setup:
            card = ctk.CTkFrame(self.stats_frame, fg_color=self.theme["card_bg"], corner_radius=18, height=90)
            card.pack(side="left", fill="both", expand=True, padx=(0 if name=="Total Faults" else 12, 0))
            card.pack_propagate(False)
            ctk.CTkFrame(card, fg_color=color, width=6, corner_radius=3).pack(side="left", fill="y", padx=(12, 4), pady=12)
            info_inner = ctk.CTkFrame(card, fg_color="transparent")
            info_inner.pack(side="left", fill="both", pady=12, padx=4)
            ctk.CTkLabel(info_inner, text=name, font=("Plus Jakarta Sans", 11, "bold"), text_color=self.theme["sub_text"]).pack(anchor="w")
            val_lbl = ctk.CTkLabel(info_inner, text="-", font=("Plus Jakarta Sans", 22, "bold"), text_color=self.theme["text_dark"])
            val_lbl.pack(anchor="w", pady=(2, 0))
            self.stat_cards[name] = val_lbl

        self.arena_split = ctk.CTkFrame(self.workspace_view_frame, fg_color="transparent")
        self.arena_split.pack(fill="both", expand=True)
        self.left_panel = ctk.CTkFrame(self.arena_split, fg_color="transparent")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.grid_card = ctk.CTkFrame(self.left_panel, fg_color=self.theme["card_bg"], corner_radius=24)
        self.grid_card.pack(fill="both", expand=True, pady=(0, 15))
        
        self.info_card = ctk.CTkFrame(self.left_panel, fg_color=self.theme["card_bg"], corner_radius=20, height=135)
        self.info_card.pack(fill="x")
        self.info_card.pack_propagate(False)
        self.info_title = ctk.CTkLabel(self.info_card, text="", font=("Plus Jakarta Sans", 11, "bold"), text_color=self.theme["sidebar_bg"])
        self.info_title.pack(anchor="w", padx=15, pady=(12, 2))
        self.info_body = ctk.CTkLabel(self.info_card, text="", font=("Plus Jakarta Sans", 11), text_color=self.theme["text_dark"], wraplength=520, justify="left")
        self.info_body.pack(anchor="w", padx=15)

        self.chart_card = ctk.CTkFrame(self.arena_split, fg_color=self.theme["card_bg"], corner_radius=24, width=380)
        self.chart_card.pack(side="right", fill="both", padx=(10, 0))
        self.chart_card.pack_propagate(False)

    def build_theory_academy_workspace(self):
        scroll_container = ctk.CTkScrollableFrame(self.theory_view_frame, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True)
        
    def build_theory_academy_workspace(self):
        scroll_container = ctk.CTkScrollableFrame(self.theory_view_frame, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True)
        
        # Row 1: Core Paging Theory Bento Block (Padding fixed)
        paging_card = ctk.CTkFrame(scroll_container, fg_color=self.theme["card_bg"], corner_radius=20)
        paging_card.pack(fill="x", pady=(10, 15), padx=20) # Padding handled via pack layout manager
        
        ctk.CTkLabel(paging_card, text="Core Architecture: Virtual Memory & Paging", font=("Plus Jakarta Sans", 16, "bold"), text_color=self.theme["text_dark"]).pack(anchor="w", padx=20, pady=(20, 0))
        ctk.CTkLabel(paging_card, text="Paging is a memory management scheme that eliminates the need for contiguous allocation of physical memory. The operating system breaks secondary memory into equal-sized blocks called Pages, and physical RAM into blocks called Frames. When a process requests a page not currently mapped in RAM, a hardware exception called a Page Fault occurs, triggering the kernel to fetch data from secondary storage and swap out an existing frame if memory capacity is fully exhausted.", font=("Plus Jakarta Sans", 12), text_color=self.theme["text_dark"], wraplength=900, justify="left").pack(anchor="w", padx=20, pady=(8, 15))
        
        # Diagram Lane Frame Wrapper inside Bento box
        diag_frame_1 = ctk.CTkFrame(paging_card, fg_color="#F4F2F9", corner_radius=14, height=180)
        diag_frame_1.pack(fill="x", padx=20, pady=(0, 20))
        diag_frame_1.pack_propagate(False)
        self.render_abstract_paging_diagram(diag_frame_1)

        # Row 2: Algorithmic Properties Detailed Matrix Breakdown (Padding fixed)
        algo_vault_card = ctk.CTkFrame(scroll_container, fg_color=self.theme["card_bg"], corner_radius=20)
        algo_vault_card.pack(fill="x", pady=5, padx=20) # Padding handled via pack layout manager
        ctk.CTkLabel(algo_vault_card, text="Operational Mechanics & Structural Tradeoffs", font=("Plus Jakarta Sans", 16, "bold"), text_color=self.theme["text_dark"]).pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(algo_vault_card, text="Operational Mechanics & Structural Tradeoffs", font=("Plus Jakarta Sans", 16, "bold"), text_color=self.theme["text_dark"]).pack(anchor="w", pady=(0, 10))
        
        tech_specs = [
            ("First-In, First-Out (FIFO)", "Operates on a pure linear queue layout framework. It targets the longest-resident page slot for eviction regardless of lookup request frequency metrics. Simple code architecture, but subject to Belady's Anomaly where allocating more frame units can directly cause drop faults to scale worse."),
            ("Least Recently Used (LRU)", "Tracks recent operation timeline states dynamically. The model evicts the page node left unreferenced for the maximum historical duration window. Highly efficient, but requires continuous back-end timestamp matrix sorting updates to maintain system state parameters."),
            ("Most Recently Used (MRU)", "The complete analytical inverse of LRU. Evicts frames accessed closest to the immediate validation step index pointer. Extremely effective in situations where a thread serially loops scanning wide sequences repeatedly, preserving old nodes from early cache sweeps."),
            ("Optimal Replacement (MIN)", "The absolute performance benchmark algorithm. Evaluates historical patterns forward by surveying the prospective reference stream to drop frames uncalled for the longest duration. Real-time engineering deployments are impossible due to prospective data unpredictability.")
        ]
        
        for name, spec in tech_specs:
            spec_row = ctk.CTkFrame(algo_vault_card, fg_color="transparent")
            spec_row.pack(fill="x", pady=8)
            ctk.CTkLabel(spec_row, text=f"• {name}: ", font=("Plus Jakarta Sans", 12, "bold"), text_color=self.theme["sidebar_bg"]).pack(side="left", anchor="n")
            ctk.CTkLabel(spec_row, text=spec, font=("Plus Jakarta Sans", 12), text_color=self.theme["text_dark"], wraplength=720, justify="left").pack(side="left", fill="x", expand=True)

    def toggle_tab_view(self, target_tab):
        if target_tab == "SIM":
            self.theory_view_frame.pack_forget()
            self.workspace_view_frame.pack(fill="both", expand=True)
            self.sim_tab_btn.configure(fg_color=self.theme["card_bg"], text_color=self.theme["text_dark"])
            self.theory_tab_btn.configure(fg_color="transparent", text_color=self.theme["sub_text"])
            self.stage_title.configure(text="Dashboard Workspace")
            self.stage_sub.configure(text="Real-time virtual memory execution trace grid sandbox environment.")
        else:
            self.workspace_view_frame.pack_forget()
            self.theory_view_frame.pack(fill="both", expand=True)
            self.theory_tab_btn.configure(fg_color=self.theme["card_bg"], text_color=self.theme["text_dark"])
            self.sim_tab_btn.configure(fg_color="transparent", text_color=self.theme["sub_text"])
            self.stage_title.configure(text="Theory Academy Vault")
            self.stage_sub.configure(text="Architectural breakdown structures and formal caching design specs.")

    def render_abstract_paging_diagram(self, master_widget):
        fig, ax = plt.subplots(figsize=(10, 1.8), facecolor="#F4F2F9")
        ax.set_facecolor("#F4F2F9")
        
        # Drawing Page Mapping blocks manually on matplotlib canvas
        ax.text(0.5, 0.5, "Virtual Pages\n(Secondary Disk)", ha='center', va='center', bbox=dict(boxstyle='round,pad=0.6', facecolor=self.theme["accent_purple"], edgecolor='#9D8DF1', lw=1.5), fontname="sans-serif", weight="bold", fontsize=9, color="#2D2A4A")
        ax.annotate('', xy=(3.1, 0.5), xytext=(1.7, 0.5), arrowprops=dict(arrowstyle="->", color="#9D8DF1", lw=2))
        
        ax.text(4.2, 0.5, "Page Table\n[MAPPED ID Matrix]", ha='center', va='center', bbox=dict(boxstyle='square,pad=0.5', facecolor='#FFFFFF', edgecolor='#B8A6FF', lw=1.5), fontname="sans-serif", fontsize=8, color="#2D2A4A")
        ax.annotate('', xy=(6.7, 0.5), xytext=(5.3, 0.5), arrowprops=dict(arrowstyle="->", color="#9D8DF1", lw=2))
        
        ax.text(7.9, 0.5, "Physical Frames\n(Main RAM Slots)", ha='center', va='center', bbox=dict(boxstyle='round,pad=0.6', facecolor=self.theme["accent_blue"], edgecolor='#A8DADC', lw=1.5), fontname="sans-serif", weight="bold", fontsize=9, color="#2D2A4A")
        
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 1)
        ax.axis('off')
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=master_widget)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def parse_inputs(self):
        raw_ref = self.ref_var.get().replace(",", " ")
        pages = [int(x) for x in raw_ref.split() if x.isdigit()]
        try:
            frames = int(self.frames_var.get())
            if frames < 1 or frames > 7: raise ValueError
        except ValueError:
            return None, None
        return pages, frames

    def run_simulation(self):
        pages, frames = self.parse_inputs()
        if not pages or not frames:
            messagebox.showerror("Config Error", "Please declare valid integer parameters (Frames: 1-7).")
            return
            
        for child in self.grid_card.winfo_children():
            child.pack_forget()
        for child in self.chart_card.winfo_children():
            child.pack_forget()
            
        algo = self.algo_var.get()
        self.info_title.configure(text=self.algo_insights[algo]["title"])
        self.info_body.configure(text=self.algo_insights[algo]["desc"])
        
        if algo == "COMPARE ALL":
            self.stats_frame.pack_forget()
            self.chart_card.pack_forget()
            self.execute_comparison(pages, frames)
        else:
            self.chart_card.pack(side="right", fill="both", padx=(10, 0))
            self.stats_frame.pack(fill="x", pady=(0, 15))
            results = self.core_engine(algo, pages, frames)
            self.update_kpis(results)
            self.render_trace_grid(pages, frames, results)
            self.render_realtime_pie(results, algo)

    def core_engine(self, algo, pages, capacity):
        frames = []
        timeline = []
        status_log = []
        hits, faults = 0, 0
        
        for i, page in enumerate(pages):
            is_hit = False
            if page in frames:
                is_hit = True
                hits += 1
            else:
                faults += 1
                if len(frames) < capacity:
                    frames.append(page)
                else:
                    idx = 0
                    if algo == "FIFO":
                        idx = (faults - 1) % capacity
                        frames[idx] = page
                    elif algo == "LRU":
                        sub = pages[:i]
                        recents = [len(sub) - 1 - sub[::-1].index(f) for f in frames]
                        idx = recents.index(min(recents))
                        frames[idx] = page
                    elif algo == "MRU":
                        sub = pages[:i]
                        recents = [len(sub) - 1 - sub[::-1].index(f) for f in frames]
                        idx = recents.index(max(recents))
                        frames[idx] = page
                    elif algo == "OPTIMAL":
                        futures = []
                        for f in frames:
                            try: next_idx = pages[i+1:].index(f) + i + 1
                            except ValueError: next_idx = float('inf')
                            futures.append(next_idx)
                        idx = futures.index(max(futures))
                        frames[idx] = page
                                
            timeline.append(list(frames))
            status_log.append("HIT" if is_hit else "MISS")
            
        return {"timeline": timeline, "status": status_log, "hits": hits, "faults": faults, "total": len(pages)}

    def update_kpis(self, res):
        h_ratio = (res["hits"] / res["total"]) * 100
        f_ratio = (res["faults"] / res["total"]) * 100
        self.stat_cards["Total Faults"].configure(text=str(res["faults"]))
        self.stat_cards["Total Hits"].configure(text=str(res["hits"]))
        self.stat_cards["Fault Ratio"].configure(text=f"{f_ratio:.1f}%")
        self.stat_cards["Hit Ratio"].configure(text=f"{h_ratio:.1f}%")

    def render_trace_grid(self, pages, capacity, res):
        scroll_win = ctk.CTkScrollableFrame(self.grid_card, fg_color="transparent", orientation="horizontal", corner_radius=24)
        scroll_win.pack(fill="both", expand=True, padx=15, pady=15)
        
        table = tk.Frame(scroll_win, bg=self.theme["card_bg"])
        table.pack(padx=10, pady=10)
        
        tk.Label(table, text="Ref String", font=("Plus Jakarta Sans", 10, "bold"), bg="#F4F2F9", fg=self.theme["text_dark"], width=12, height=2, bd=0).grid(row=0, column=0, padx=2, pady=2)
        for c, p in enumerate(pages):
            tk.Label(table, text=str(p), font=("Plus Jakarta Sans", 11, "bold"), bg="#E6E2FF", fg=self.theme["sidebar_bg"], width=5, height=2).grid(row=0, column=c+1, padx=2, pady=2)
            
        for r in range(capacity):
            tk.Label(table, text=f"Slot {r+1}", font=("Plus Jakarta Sans", 9, "bold"), bg="#F4F2F9", fg=self.theme["sub_text"], width=12, height=2).grid(row=r+1, column=0, padx=2, pady=2)
            for c in range(len(pages)):
                snap = res["timeline"][c]
                val = str(snap[r]) if r < len(snap) else "-"
                tk.Label(table, text=val, font=("Courier New", 11, "bold"), bg="#FAF9FC", fg=self.theme["text_dark"], width=5, height=2).grid(row=r+1, column=c+1, padx=2, pady=2)
                
        tk.Label(table, text="Outcome", font=("Plus Jakarta Sans", 10, "bold"), bg="#F4F2F9", fg=self.theme["text_dark"], width=12, height=2).grid(row=capacity+1, column=0, padx=2, pady=2)
        for c, status in enumerate(res["status"]):
            bg_c = "#D1FAE5" if status == "HIT" else "#FFE4E6"
            fg_c = "#065F46" if status == "HIT" else "#9F1239"
            lbl = tk.Label(table, text=status, font=("Plus Jakarta Sans", 8, "bold"), bg=bg_c, fg=fg_c, width=5, height=2)
            lbl.grid(row=capacity+1, column=c+1, padx=2, pady=2)

    def render_realtime_pie(self, res, algo_name):
        fig, ax = plt.subplots(figsize=(4, 4), facecolor=self.theme["card_bg"])
        ax.set_facecolor(self.theme["card_bg"])
        
        labels = ['Hits', 'Faults']
        sizes = [res["hits"], res["faults"]]
        colors = [self.theme["accent_blue"], self.theme["accent_pink"]]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.75, textprops=dict(color=self.theme["text_dark"], fontname="sans-serif", fontsize=10))
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=10)
        
        centre_circle = plt.Circle((0,0),0.55,fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_title(f"{algo_name} Ratio Breakout", color=self.theme["text_dark"], fontsize=12, fontweight="bold", pad=10)
        ax.axis('equal')  
        plt.tight_layout()
        
        chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_card)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        plt.close(fig)

    def execute_comparison(self, pages, frames):
        algos = ["FIFO", "LRU", "MRU", "OPTIMAL"]
        faults_data = []
        for algo in algos:
            res = self.core_engine(algo, pages, frames)
            faults_data.append(res["faults"])
            
        fig, ax = plt.subplots(figsize=(6, 3.8), facecolor=self.theme["card_bg"])
        ax.set_facecolor(self.theme["card_bg"])
        
        clay_colors = [self.theme["accent_pink"], self.theme["accent_blue"], "#C3B1E1", self.theme["accent_yellow"]]
        bars = ax.bar(algos, faults_data, color=clay_colors, width=0.45, edgecolor="#E6E2FF", linewidth=1)
        
        ax.set_title("Algorithmic Efficiency Cross-Comparison", color=self.theme["text_dark"], fontsize=12, fontweight="bold", pad=20)
        ax.tick_params(colors=self.theme["sub_text"], labelsize=10)
        ax.spines['bottom'].set_color('#E6E2FF')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E6E2FF')
        ax.yaxis.grid(True, color='#E6E2FF', linestyle='-', linewidth=0.7)
        ax.set_axisbelow(True)
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', color=self.theme["text_dark"], fontsize=10, fontweight="bold")
                        
        plt.tight_layout()
        chart_canvas = FigureCanvasTkAgg(fig, master=self.grid_card)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        plt.close(fig)

if __name__ == "__main__":
    app = ClaymorphicSimulator()
    app.mainloop()