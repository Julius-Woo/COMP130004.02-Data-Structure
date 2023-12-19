import tkinter as tk
from tkinter import messagebox, font
from mainpj2 import Graph
import tkinter.scrolledtext as scrolledtext

filepath = './edge.txt'
map1 = Graph()
map1.init_adjlist(filepath)
map1.dijkstra_allpairs()
n = len(map1.v)
alp = {chr(i + 65): i for i in range(26)}  # A-Z -> 0-25

# main window
root = tk.Tk()
root.title("Map Navigation System")
root.geometry("980x520+350+180")
root.minsize(960, 480)
root.maxsize(1000, 540)

custom_font = font.Font(family="Times New Roman", size=12)

# left canvas: map
map_canvas = tk.Canvas(root, width=750, height=450)
map_canvas.pack(side="left")
map_image = tk.PhotoImage(file='./resized.png')
map_canvas.create_image(0, 0, image=map_image, anchor='nw')

# initialize locations
points_data = {
    'A': (55, 164),
    'B': (103, 384),
    'C': (135, 199),
    'D': (148, 282),
    'E': (173, 374),
    'F': (212, 103),
    'G': (229, 181),
    'H': (242, 258),
    'I': (335, 63),
    'J': (342, 154),
    'K': (353, 237),
    'L': (370, 329),
    'M': (395, 406),
    'N': (437, 145),
    'O': (459, 209),
    'P': (474, 299),
    'Q': (492, 381),
    'R': (524, 76),
    'S': (525, 128),
    'T': (531, 196),
    'U': (559, 285),
    'V': (602, 21),
    'W': (606, 113),
    'X': (612, 187),
    'Y': (621, 271),
    'Z': (627, 372)
}


def clear_contents():
    location_entry_1.delete(0, tk.END)
    location_entry_2.delete(0, tk.END)
    result_display.delete(1.0, tk.END)
    map_canvas.delete("path_line")


def op_clear():
    result_display.delete(1.0, tk.END)
    map_canvas.delete("path_line")


# right UI framework
ui_frame = tk.Frame(root)
ui_frame.pack(side="right", fill="both", expand=True)


location_frame = tk.Frame(ui_frame)
location_frame.grid(row=0, column=0, padx=(0, 20), pady=(0, 10), sticky="nw")


location_label_1 = tk.Label(location_frame, text="Location 1:")
location_label_1.grid(row=0, column=0, padx=5, pady=2, sticky="w")

location_entry_1 = tk.Entry(location_frame, width=10)
location_entry_1.grid(row=0, column=1, padx=5, pady=2, sticky="we")

location_label_2 = tk.Label(location_frame, text="Location 2:")
location_label_2.grid(row=1, column=0, padx=5, pady=2, sticky="w")

location_entry_2 = tk.Entry(location_frame, width=10)
location_entry_2.grid(row=1, column=1, padx=5, pady=2, sticky="we")

clear_button = tk.Button(location_frame, text="Reset", command=clear_contents)
clear_button.grid(row=2, column=0, columnspan=2, padx=5, pady=12)


operation_frame = tk.Frame(ui_frame)
operation_frame.grid(row=1, column=0, padx=(0, 20), pady=(10, 10), sticky="nw")


operation_buttons = []
for i in range(4):
    operation_button = tk.Button(operation_frame, text=f"Operation {i+1}")
    operation_button.grid(row=i//2, column=i % 2, padx=5, pady=5)
    operation_buttons.append(operation_button)


result_frame = tk.Frame(ui_frame)
result_frame.grid(row=2, column=0, padx=(0, 20), pady=(10, 0), sticky="nw")

result_label = tk.Label(result_frame, text="Output:")
result_label.pack()

result_display = scrolledtext.ScrolledText(result_frame,
                                           bg="white", width=25, height=12, wrap=tk.WORD, font=custom_font)
result_display.pack()


def create_clickable_areas(canvas, points):
    for point, (x, y) in points.items():
        canvas.create_rectangle(
            x-8, y-8, x+8, y+8, outline="", fill="", tags=('clickable_area', point))



create_clickable_areas(map_canvas, points_data)


def point_selected(event):
    click_x = map_canvas.canvasx(event.x)
    click_y = map_canvas.canvasy(event.y)
    selected = map_canvas.find_closest(click_x, click_y, halo=10)
    tags = map_canvas.gettags(selected)
    if 'clickable_area' in tags:
        point_id = tags[1]
        if location_entry_1.get() == "":
            location_entry_1.insert(0, point_id)
        elif location_entry_2.get() == "":
            location_entry_2.insert(0, point_id)
        else:
            messagebox.showinfo(
                "Selection Full", "Two locations are already selected.")


map_canvas.tag_bind('clickable_area', '<Button-1>', point_selected)


def h_loc(location):
    x, y = location
    size = 20  # Size of the triangle
    points = [x, y, x + size, y + size, x - size, y + size]
    map_canvas.create_polygon(points, fill="Gold", tags="path_line")


def operation1():
    op_clear()
    start_id = location_entry_1.get().upper()
    end_id = location_entry_2.get().upper()
    if start_id in points_data and end_id in points_data:
        h_loc(points_data[start_id])
        h_loc(points_data[end_id])
        path_objects = map1.allpaths[alp[start_id]][alp[end_id]][0]
        path_points = [point.id for point in path_objects]
        for i in range(len(path_points) - 1):
            start_point = path_points[i]
            end_point = path_points[i + 1]
            start_x, start_y = points_data[start_point]
            end_x, end_y = points_data[end_point]
            map_canvas.create_line(
                start_x, start_y, end_x, end_y, fill="yellow", width=4, tags="path_line")

        path_str = "Shortest path from {} to {}:\n {}".format(start_id, end_id, map1.get_pathstr(
            map1.v[alp[start_id]], map1.v[alp[end_id]]))
        path_length = "Path length: {}km".format(map1.calc_path(path_objects))
        result_display.insert(tk.END, f"{path_str}\n{path_length}")
    else:
        messagebox.showerror(
            "Error", "Please select valid start and end points.")


def operation2():
    op_clear()
    location = location_entry_1.get().upper()
    if location and location in alp:
        h_loc(points_data[location])
        map1.dijkstra(map1.v[alp[location]])
        output_text = ""
        for j in range(26):
            end_location = chr(j + 65)
            if end_location in alp:
                path = map1.allpaths[alp[location]][alp[end_location]][0]
                for k in range(len(path) - 1):
                    start_point = path[k].id
                    end_point = path[k + 1].id
                    start_x, start_y = points_data[start_point]
                    end_x, end_y = points_data[end_point]
                    map_canvas.create_line(
                        start_x, start_y, end_x, end_y, fill="purple", width=4, tags="path_line")
                path_str = "Shortest path from {} to {}:\n {}".format(
                    end_location, location, map1.get_pathstr(map1.v[alp[end_location]], map1.v[alp[location]]))
                path_length = "Path length: {}km".format(map1.calc_path(path))
                output_text += f"{path_str}\n{path_length}\n"
        result_display.insert(tk.END, output_text)
    else:
        messagebox.showerror("Error", "Please enter a valid start location.")


def operation3():
    op_clear()
    location = location_entry_1.get().upper()
    if location:
        h_loc(points_data[location])
        mst = map1.mst_prim(map1.v[alp[location]])
    else:
        mst = map1.mst_kruskal()

    for u, v, _ in mst:
        start_x, start_y = points_data[u.id]
        end_x, end_y = points_data[v.id]
        map_canvas.create_line(start_x, start_y, end_x,
                               end_y, fill="blue", width=4, tags="path_line")

    total_length = map1.print_mst(mst)
    result_display.insert(tk.END, f"Subway route total length: {total_length}km")


def operation4():
    op_clear()
    location = location_entry_1.get().upper()
    if location:
        h_loc(points_data[location])
        total, edges = map1.bus_route(map1.v[alp[location]])
        for u, v in edges:
            start_x, start_y = points_data[u.id]
            end_x, end_y = points_data[v.id]
            map_canvas.create_line(
                start_x, start_y, end_x, end_y, fill="green", width=4, tags="path_line")

        result_display.insert(
            tk.END, f"Bus route starting from {location} \n total length: {total}km")
    else:
        messagebox.showerror(
            "Error", "Please enter a start location for the bus route.")

operation_buttons[0].config(command=operation1)
operation_buttons[1].config(command=operation2)
operation_buttons[2].config(command=operation3)
operation_buttons[3].config(command=operation4)


root.mainloop()
