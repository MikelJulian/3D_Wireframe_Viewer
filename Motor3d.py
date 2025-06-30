import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

class WireframeViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Wireframe Viewer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2d2d30')

        # Variables for the model
        self.vertices = None
        self.faces = None
        self.model_loaded = False
        self.current_file = ""

        # Color variables
        self.wireframe_color = '#00ffff'  # Cyan
        self.vertex_color = '#00ffff'     # Cyan
        self.face_color = '#007acc'       # New color for faces
        self.background_color = '#000000' # Black

        # Display control variables
        self.wireframe_var = tk.BooleanVar(value=True) # Controls if wireframe is visible
        self.show_faces_var = tk.BooleanVar(value=False) # New: Controls if filled faces are visible

        self.setup_ui()
        self.setup_3d_plot()

    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2d2d30')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure grid for main_frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

        # Control panel (left)
        control_frame = tk.Frame(main_frame, bg='#3f3f46', width=300)
        control_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        # Title
        title_label = tk.Label(control_frame, text="3D Wireframe Viewer",
                                 bg='#3f3f46', fg='#007acc',
                                 font=('Segoe UI', 11, 'bold'))
        title_label.pack(pady=20)

        # Import section
        import_frame = tk.LabelFrame(control_frame, text="Import Model",
                                         bg='#3f3f46', fg='white',
                                         font=('Segoe UI', 10, 'bold'))
        import_frame.pack(fill=tk.X, padx=10, pady=10)

        self.btn_import = tk.Button(import_frame, text="Import Mesh",
                                         bg='#007acc', fg='white',
                                         font=('Segoe UI', 10, 'bold'),
                                         command=self.import_mesh,
                                         cursor='hand2')
        self.btn_import.pack(fill=tk.X, padx=10, pady=10)

        self.status_label = tk.Label(import_frame, text="No model loaded",
                                         bg='#3f3f46', fg='#cccccc',
                                         font=('Segoe UI', 9))
        self.status_label.pack(padx=10, pady=(0, 10))

        # Color controls section
        color_frame = tk.LabelFrame(control_frame, text="Color Controls",
                                         bg='#3f3f46', fg='white',
                                         font=('Segoe UI', 10, 'bold'))
        color_frame.pack(fill=tk.X, padx=10, pady=10)

        # Wireframe/edges color button
        wireframe_color_frame = tk.Frame(color_frame, bg='#3f3f46')
        wireframe_color_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(wireframe_color_frame, text="Edges Color:",
                 bg='#3f3f46', fg='white', font=('Segoe UI', 9)).pack(side=tk.LEFT)

        self.wireframe_color_btn = tk.Button(wireframe_color_frame, text="  ",
                                          bg=self.wireframe_color, width=3,
                                          command=self.change_wireframe_color,
                                          cursor='hand2')
        self.wireframe_color_btn.pack(side=tk.RIGHT)

        # Vertices color button
        vertex_color_frame = tk.Frame(color_frame, bg='#3f3f46')
        vertex_color_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(vertex_color_frame, text="Vertices Color:",
                 bg='#3f3f46', fg='white', font=('Segoe UI', 9)).pack(side=tk.LEFT)

        self.vertex_color_btn = tk.Button(vertex_color_frame, text="  ",
                                       bg=self.vertex_color, width=3,
                                       command=self.change_vertex_color,
                                       cursor='hand2')
        self.vertex_color_btn.pack(side=tk.RIGHT)

        # New: Faces color button
        face_color_frame = tk.Frame(color_frame, bg='#3f3f46')
        face_color_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(face_color_frame, text="Faces Color:",
                 bg='#3f3f46', fg='white', font=('Segoe UI', 9)).pack(side=tk.LEFT)

        self.face_color_btn = tk.Button(face_color_frame, text="  ",
                                         bg=self.face_color, width=3,
                                         command=self.change_face_color,
                                         cursor='hand2')
        self.face_color_btn.pack(side=tk.RIGHT)

        # Background color button
        bg_color_frame = tk.Frame(color_frame, bg='#3f3f46')
        bg_color_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(bg_color_frame, text="Background Color:",
                 bg='#3f3f46', fg='white', font=('Segoe UI', 9)).pack(side=tk.LEFT)

        self.bg_color_btn = tk.Button(bg_color_frame, text="  ",
                                       bg=self.background_color, width=3,
                                       command=self.change_background_color,
                                       cursor='hand2')
        self.bg_color_btn.pack(side=tk.RIGHT)

        # Reset colors button
        reset_colors_btn = tk.Button(color_frame, text="Reset Colors",
                                         bg='#6c757d', fg='white',
                                         font=('Segoe UI', 9),
                                         command=self.reset_colors,
                                         cursor='hand2')
        reset_colors_btn.pack(fill=tk.X, padx=10, pady=(5, 10))

        # Camera views section
        camera_frame = tk.LabelFrame(control_frame, text="Camera Views",
                                         bg='#3f3f46', fg='white',
                                         font=('Segoe UI', 10, 'bold'))
        camera_frame.pack(fill=tk.X, padx=10, pady=10)

        # View buttons grid
        views_grid = tk.Frame(camera_frame, bg='#3f3f46')
        views_grid.pack(padx=10, pady=10)

        # View buttons in a 2x3 grid
        views = [
            ("Front", 0, 0, self.front_view),
            ("Back", 0, 1, self.back_view),
            ("Left", 1, 0, self.left_view),
            ("Right", 1, 1, self.right_view),
            ("Top", 2, 0, self.top_view),
            ("Bottom", 2, 1, self.bottom_view)
        ]

        self.view_buttons = []
        for text, row, col, command in views:
            btn = tk.Button(views_grid, text=text, command=command,
                            bg='#28a745', fg='white', font=('Segoe UI', 9),
                            width=10, state='disabled', cursor='hand2')
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
            self.view_buttons.append(btn)

        # Configure grid columns
        views_grid.columnconfigure(0, weight=1)
        views_grid.columnconfigure(1, weight=1)

        # Rendering and options section
        render_frame = tk.LabelFrame(control_frame, text="Rendering and Options",
                                         bg='#3f3f46', fg='white',
                                         font=('Segoe UI', 10, 'bold'))
        render_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        # Checkbox for wireframe
        wireframe_check = tk.Checkbutton(render_frame, text="Show Wireframe",
                                         variable=self.wireframe_var,
                                         bg='#3f3f46', fg='white',
                                         selectcolor='#3f3f46',
                                         command=self.update_plot)
        wireframe_check.pack(padx=10, pady=5)

        # New: Checkbox to show faces
        faces_check = tk.Checkbutton(render_frame, text="Show Faces",
                                         variable=self.show_faces_var,
                                         bg='#3f3f46', fg='white',
                                         selectcolor='#3f3f46',
                                         command=self.update_plot)
        faces_check.pack(padx=10, pady=5)

        # Render button
        self.btn_render = tk.Button(render_frame, text="Take Render",
                                         bg='#17a2b8', fg='white',
                                         font=('Segoe UI', 10, 'bold'),
                                         command=self.take_render,
                                         cursor='hand2', state='disabled')
        self.btn_render.pack(fill=tk.X, padx=10, pady=10)

        # Close button
        btn_close = tk.Button(control_frame, text="Close Application",
                                         bg='#dc3545', fg='white',
                                         font=('Segoe UI', 12, 'bold'),
                                         command=self.close_application,
                                         cursor='hand2')
        btn_close.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Frame for the 3D viewport
        self.plot_frame = tk.Frame(main_frame, bg='black')
        self.plot_frame.grid(row=0, column=1, sticky="nsew")

    def setup_3d_plot(self):
        self.fig = Figure(figsize=(8, 6), facecolor=self.background_color)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor(self.background_color)

        # Hide background panels of the 3D box
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')

        # Set initial axis labels
        self.ax.set_xlabel('X', color='white')
        self.ax.set_ylabel('Y', color='white')
        self.ax.set_zlabel('Z', color='white')

        self.ax.tick_params(colors='white')
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = tk.Frame(self.plot_frame, bg='#2d2d30')
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        nav_toolbar = NavigationToolbar2Tk(self.canvas, toolbar)
        nav_toolbar.configure(bg='#2d2d30')
        nav_toolbar.update()

        self.show_initial_message()

    def show_initial_message(self):
        self.ax.clear()
        self.ax.set_facecolor(self.background_color)

        # Hide background panels of the 3D box
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')

        self.ax.text(0, 0, 0, 'Import a 3D model to begin',
                     color='white', fontsize=16, ha='center', va='center')
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_zlim(-1, 1)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.canvas.draw()

    def change_wireframe_color(self):
        color = colorchooser.askcolor(color=self.wireframe_color, title="Select color for edges")
        if color[1]:
            self.wireframe_color = color[1]
            self.wireframe_color_btn.config(bg=self.wireframe_color)
            self.update_plot()

    def change_vertex_color(self):
        color = colorchooser.askcolor(color=self.vertex_color, title="Select color for vertices")
        if color[1]:
            self.vertex_color = color[1]
            self.vertex_color_btn.config(bg=self.vertex_color)
            self.update_plot()

    def change_face_color(self):
        color = colorchooser.askcolor(color=self.face_color, title="Select color for faces")
        if color[1]:
            self.face_color = color[1]
            self.face_color_btn.config(bg=self.face_color)
            self.update_plot()

    def change_background_color(self):
        color = colorchooser.askcolor(color=self.background_color, title="Select background color")
        if color[1]:
            self.background_color = color[1]
            self.bg_color_btn.config(bg=self.background_color)
            self.fig.patch.set_facecolor(self.background_color)
            self.ax.set_facecolor(self.background_color)
            self.update_plot()

    def reset_colors(self):
        self.wireframe_color = '#00ffff'
        self.vertex_color = '#00ffff'
        self.face_color = '#007acc'
        self.background_color = '#000000'

        self.wireframe_color_btn.config(bg=self.wireframe_color)
        self.vertex_color_btn.config(bg=self.vertex_color)
        self.face_color_btn.config(bg=self.face_color)
        self.bg_color_btn.config(bg=self.background_color)

        self.fig.patch.set_facecolor(self.background_color)
        self.ax.set_facecolor(self.background_color)

        self.update_plot()

    def import_mesh(self):
        file_types = [
            ("OBJ files", "*.obj"),
            ("PLY files", "*.ply"),
            ("STL files", "*.stl"),
            ("All files", "*.*")
        ]

        filename = filedialog.askopenfilename(
            title="Select 3D model file",
            filetypes=file_types
        )

        if filename:
            try:
                self.load_model(filename)
                self.current_file = filename
                self.status_label.config(text=f"Loaded: {os.path.basename(filename)}")
                self.model_loaded = True
                self.enable_buttons()
                self.update_plot()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load model:\n{str(e)}")
                self.status_label.config(text="Error loading model")

    def load_model(self, filename):
        vertices = []
        faces = []

        if filename.lower().endswith('.obj'):
            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith('v '):
                        parts = line.strip().split()
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        vertices.append([x, y, z])
                    elif line.startswith('f '):
                        parts = line.strip().split()
                        face = []
                        for part in parts[1:]:
                            vertex_idx = int(part.split('/')[0]) - 1
                            face.append(vertex_idx)
                        faces.append(face)

        elif filename.lower().endswith('.ply'):
            self.load_ply(filename, vertices, faces)
        elif filename.lower().endswith('.stl'):
            self.load_stl(filename, vertices, faces)
        else:
            raise Exception("Unsupported file format")

        self.vertices = np.array(vertices)
        self.faces = faces

        if len(vertices) == 0:
            raise Exception("No vertices found in file")

    def load_ply(self, filename, vertices, faces):
        with open(filename, 'r') as file:
            vertex_count = 0
            face_count = 0
            reading_vertices = False
            reading_faces = False

            for line in file:
                if line.startswith('element vertex'):
                    vertex_count = int(line.split()[-1])
                elif line.startswith('element face'):
                    face_count = int(line.split()[-1])
                elif line.startswith('end_header'):
                    reading_vertices = True
                    continue

                if reading_vertices and len(vertices) < vertex_count:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        vertices.append([float(parts[0]), float(parts[1]), float(parts[2])])
                elif len(vertices) == vertex_count and not reading_faces:
                    reading_faces = True
                    reading_vertices = False

                if reading_faces and len(faces) < face_count:
                    parts = line.strip().split()
                    if len(parts) > 1:
                        num_vertices = int(parts[0])
                        face = [int(parts[i+1]) for i in range(num_vertices)]
                        faces.append(face)

    def load_stl(self, filename, vertices, faces):
        with open(filename, 'r') as file:
            vertex_buffer = []
            for line in file:
                if 'vertex' in line:
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                        vertex_buffer.append(vertex)

                        if len(vertex_buffer) == 3:
                            start_idx = len(vertices)
                            vertices.extend(vertex_buffer)
                            faces.append([start_idx, start_idx + 1, start_idx + 2])
                            vertex_buffer = []

    def enable_buttons(self):
        for btn in self.view_buttons:
            btn.config(state='normal')
        self.btn_render.config(state='normal')

    def update_plot(self):
        if not self.model_loaded or self.vertices is None:
            self.show_initial_message()
            return

        self.ax.clear()
        self.ax.set_facecolor(self.background_color)

        # Hide background panels of the 3D box
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')

        # --- Rendering Logic ---

        # 1. Draw Filled Faces (if show_faces_var is True)
        if self.show_faces_var.get():
            visible_face_vertices = []

            for face in self.faces:
                if len(face) >= 3:
                    if len(face) == 3:
                        visible_face_vertices.append(self.vertices[face])
                    elif len(face) > 3:
                        # Triangulate N-gon (simple fan triangulation from the first vertex)
                        for i in range(1, len(face) - 1):
                            tri_indices = [face[0], face[i], face[i+1]]
                            visible_face_vertices.append(self.vertices[tri_indices])

            if visible_face_vertices:
                mesh = Poly3DCollection(visible_face_vertices, alpha=0.5, facecolor=self.face_color, edgecolors='none')
                self.ax.add_collection3d(mesh)

        # 2. Draw Wireframe (if wireframe_var is True)
        # MOVED AFTER FACES TO RENDER ON TOP
        if self.wireframe_var.get():
            for face in self.faces:
                if len(face) >= 3:
                    face_vertices = self.vertices[face]
                    # Close the loop for drawing edges
                    face_vertices_closed = np.vstack([face_vertices, face_vertices[0]])

                    self.ax.plot(face_vertices_closed[:, 0],
                                 face_vertices_closed[:, 1],
                                 face_vertices_closed[:, 2],
                                 color=self.wireframe_color, linewidth=1)

        # --- Axis and Visibility Configuration ---
        if self.model_loaded and self.vertices is not None and len(self.vertices) > 0:
            # Auto-scale plot limits based on model's bounding box
            min_coords = self.vertices.min(axis=0)
            max_coords = self.vertices.max(axis=0)

            max_range = np.max(max_coords - min_coords) / 2.0

            mid_x = (max_coords[0] + min_coords[0]) * 0.5
            mid_y = (max_coords[1] + min_coords[1]) * 0.5
            mid_z = (max_coords[2] + min_coords[2]) * 0.5

            # Set limits with a small buffer for better visualization
            buffer = max_range * 0.1
            self.ax.set_xlim(mid_x - max_range - buffer, mid_x + max_range + buffer)
            self.ax.set_ylim(mid_y - max_range - buffer, mid_y + max_range + buffer)
            self.ax.set_zlim(mid_z - max_range - buffer, mid_z + max_range + buffer)

        self.ax.tick_params(colors='white') # Ensure tick colors remain white

        self.canvas.draw()

    def toggle_wireframe(self):
        self.update_plot()

    def front_view(self):
        if self.model_loaded:
            self.ax.view_init(elev=0, azim=0)
            self.update_plot()

    def back_view(self):
        if self.model_loaded:
            self.ax.view_init(elev=0, azim=180)
            self.update_plot()

    def left_view(self):
        if self.model_loaded:
            self.ax.view_init(elev=0, azim=90)
            self.update_plot()

    def right_view(self):
        if self.model_loaded:
            self.ax.view_init(elev=0, azim=-90)
            self.update_plot()

    def top_view(self):
        if self.model_loaded:
            self.ax.view_init(elev=90, azim=0)
            self.update_plot()

    def bottom_view(self):
        if self.model_loaded:
            self.ax.view_init(elev=-90, azim=0)
            self.update_plot()

    def take_render(self):
        if not self.model_loaded:
            messagebox.showwarning("Warning", "No model loaded")
            return

        filename = filedialog.asksaveasfilename(
            title="Save render",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )

        if filename:
            try:
                self.fig.savefig(filename, facecolor=self.background_color, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Render saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save render:\n{str(e)}")

    def close_application(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WireframeViewer(root)
    root.mainloop()