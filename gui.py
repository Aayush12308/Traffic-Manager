import tkinter as tk
from PIL import Image, ImageTk
import cv2

# Traffic Light Class
class TrafficLight:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, width=60, height=180, bg="white")
        self.canvas.pack()
        self.create_lights()

    def create_lights(self):
        self.canvas.create_rectangle(10, 10, 50, 170, fill="black", outline="black")
        self.red = self.canvas.create_oval(15, 20, 45, 50, fill="gray", outline="black")
        self.yellow = self.canvas.create_oval(15, 55, 45, 85, fill="gray", outline="black")
        self.green = self.canvas.create_oval(15, 90, 45, 120, fill="gray", outline="black")

    def update_light(self, state):
        self.canvas.itemconfig(self.red, fill="gray")
        self.canvas.itemconfig(self.yellow, fill="gray")
        self.canvas.itemconfig(self.green, fill="gray")

        if state == "red":
            self.canvas.itemconfig(self.red, fill="red")
        elif state == "green":
            self.canvas.itemconfig(self.green, fill="green")

# Function to update video frames
def update_video(video_frame, cap, traffic_light, idx):
    global current_video_index

    ret, frame = cap.read()

    if ret:
        frame = cv2.resize(frame, (200, 150))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        video_frame.imgtk = imgtk
        video_frame.configure(image=imgtk)

        traffic_light.update_light("green")  # Green while playing

        root.after(30, update_video, video_frame, cap, traffic_light, idx)  # Continue playing

    else:
        # Video ended -> Pause & Switch to Next
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        traffic_light.update_light("red")  # Red when stopped

        current_video_index += 1
        if current_video_index >= len(caps):  # Loop back to the first video
            current_video_index = 0

        start_video(current_video_index)

# Function to start a specific video
def start_video(idx):
    global current_video_index
    current_video_index = idx

    for i in range(len(caps)):
        if i == idx:
            update_video(video_frames[i], caps[i], traffic_lights[i], i)  # Play this video
        else:
            caps[i].set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset frame
            traffic_lights[i].update_light("red")  # Stop others

# Initialize main window
root = tk.Tk()
root.title("Traffic Light Simulation with Videos")
root.geometry("800x800")

# Create video frames & traffic lights
video_frames = []
traffic_lights = []

positions = [(250, 50), (250, 550), (50, 250), (450, 250)]
video_paths = [
    "vids/vid1.mp4",
    "vids/vid2.mp4",
    "vids/vid3.mp4",
    "vids/vid4.mp4"
]

caps = [cv2.VideoCapture(path) for path in video_paths]
current_video_index = 0  # Track which video is currently playing

for i, (x, y) in enumerate(positions):
    frame = tk.Frame(root, width=260, height=180)
    frame.place(x=x, y=y)

    video_frame = tk.Label(frame, bg="black")
    video_frame.pack(side=tk.LEFT)
    video_frames.append(video_frame)

    traffic_frame = tk.Frame(frame)
    traffic_light = TrafficLight(traffic_frame)
    traffic_light.update_light("red")  # Initially red
    traffic_frame.pack(side=tk.RIGHT)
    traffic_lights.append(traffic_light)

# Start first video automatically
start_video(0)

# Handle window closing
def on_closing():
    for cap in caps:
        if cap.isOpened():
            cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
