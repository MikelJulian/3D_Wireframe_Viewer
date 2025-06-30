3D Wireframe Viewer
An intuitive and lightweight desktop application for visualizing 3D models in wireframe and solid-faced representations. Developed with tkinter for the user interface and matplotlib for 3D rendering, this tool is ideal for engineers, designers, and enthusiasts who need a quick and straightforward way to inspect 3D models without the complexity of full-fledged CAD software.

Key Features
Multi-Format Loading: Supports popular 3D model file formats including .obj, .ply, and .stl.

Flexible Visualization: Easily switch between wireframe and filled face views to suit your inspection needs.

Customizable Color Controls: Adjust colors for edges, vertices, faces, and the background. It also includes an option to reset all colors to their default values.

Predefined Views: Quickly snap to orthogonal views like Front, Back, Left, Right, Top, and Bottom for detailed inspection from various angles.

Interactive Navigation: Utilize built-in Matplotlib navigation tools to rotate, zoom, and pan your 3D model with ease.

Render Export: Save snapshots of your current view as .png and .jpg images, perfect for documentation or presentations.

How to Run the Application
To run this application from source, you'll need Python 3 installed along with the required libraries.

Clone this repository to your local machine:

Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
(Remember to replace your-username and your-repository-name with your actual GitHub details.)

Install the dependencies using pip:

Bash

pip install matplotlib numpy
(Note: tkinter is usually included with standard Python installations.)

Execute the main application file from your terminal:

Bash

python main.py # Or whatever your main Python file is named (e.g., WireframeViewer.py)
Interface Usage
Upon launching the application, you'll see a black screen with the message "Import a 3D model to begin".

Click the "Import Mesh" button in the left control panel to load your 3D model file (.obj, .ply, .stl).

Once the model is loaded, it will be displayed in the 3D plotting area.

Use the controls in the left panel to:

Change the colors of edges, vertices, faces, and the background.

Toggle the visibility of the wireframe and filled faces using the checkboxes.

Select one of the predefined views (Front, Top, Left, etc.).

You can interact directly with the model in the plotting area by dragging your mouse to rotate, using the mouse wheel to zoom, and the icons in the bottom toolbar for other navigation actions.

Click "Take Render" to save an image of the current view.

Click "Close Application" to exit.

Underlying Technologies
Python 3

tkinter

matplotlib

NumPy

About the Author
This project was developed by Mikel Julián Villena as a demonstration of my skills in desktop application development and 3D visualization, with an aspiration to become a Technical Artist. This tool showcases my ability to bridge programming with visual content creation.

If you have any questions, suggestions, or just want to connect, feel free to reach out.

Author
Mikel Julián Villena

Connect with me on www.linkedin.com/in/mikel-julián-villena-a95775267
