from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.animation as animation

class heat_analysis():

    def __init__(self, file_path="D:/Programming/Python/ali_project/",
                csv_file_name="heat_data.csv", npy_file_name="heat_data.npy",
                start_time=0, end_time=36000):
        self.file_path = file_path
        self.csv_file_name = csv_file_name
        self.npy_file_name = npy_file_name
        self.full_path_csv = file_path + csv_file_name
        self.full_path_npy = file_path + npy_file_name
        self.is_npy_format_made = False
        self.convert_csv_to_numpy_file()
        self.data_array = None
        self.find_data_array()
        self.start_time = start_time
        self.end_time = end_time
        self.points = {1:(0.000, 0.050), 2:(0.025, 0.050), 3:(0.050, 0.050), 4:(0.000, 0.075),
                       5:(0.025, 0.075), 6:(0.050, 0.075), 7:(0.075, 0.075), 8:(0.000, 0.100),
                       9:(0.025, 0.100),
                       10:(0.050, 0.100), 11:(0.075, 0.100), 12:(0.100, 0.100)}
        self.points_coords = [coords for coords in self.points.values()]
        self.points_names = [name for name in self.points.keys()]
        self.points_x_coords = [coords[0] for coords in self.points_coords]
        self.points_y_coords = [-coords[1] for coords in self.points_coords]
        self.index_s = [i for i in range(len(self.points))]
        self.time_s = np.array(self.data_array[12][:])
        self.num_of_frames = len(self.time_s)

    def convert_csv_to_numpy_file(self):
        
        file = open(self.full_path_csv)
        with open(self.full_path_csv) as file:
            reader = csv.reader(file, delimiter=',', skipinitialspace=True)
            first_row = next(reader)
            num_cols = len(first_row)    
        
        data_arr = np.loadtxt(self.full_path_csv, delimiter=',', usecols=range(1, num_cols))
        np.save(self.full_path_npy, data_arr)
        self.is_npy_format_made = True

    def find_data_array(self):
        if self.is_npy_format_made:
            self.data_array = np.load(self.full_path_npy)
        
    def make_animating_plot(self):

        def bar_temps(time_index):
            temp_s_at_t = np.zeros(len(self.points))
            for i in range(len(self.points)):
                temp_s_at_t[i] = self.data_array[i][time_index]
            return temp_s_at_t

        fig, ax = plt.subplots(figsize=(8,6))

        def animate(time_index, initial_bar, ax):
            if time_index + 1 < len(self.points):
                new_index = time_index + 1
            else:
                new_index = time_index
            new_bar = bar_temps(new_index)
            time = self.time_s[time_index]
            # ax.text("", "", "", ha='center', color="b", size="8")
            for i, bar in enumerate(initial_bar):
                bar.set_height(new_bar[i])
                # temp = bar.get_height()
                # text = f"{temp}"
                # text_x = bar.get_x() + bar.get_width() / 2
                # text_y = bar.get_y() + temp
                # ax.text(text_x, text_y, text, ha="center", color="b", size="8")
            ax.set_title(f'Time = {time}s')
            return initial_bar
            
        ax.set_ylim(0, 800)   
        ax.set_xlabel("Number of Point")
        ax.set_xticks([x for x in range(13)])
        ax.set_ylabel("Temperature (K)")
        initial_bar = plt.bar(self.points_names, bar_temps(0), color='g')
        anim = animation.FuncAnimation(fig, animate, self.num_of_frames, fargs=(initial_bar, ax),
                             interval=0.5, blit=False, repeat=False)
        anim.save("D:/Programming/Python/ali_project/anim.mp4")
        plt.show()            

sample = heat_analysis()
# sample.make_animating_plot()
# sample.convert_csv_to_numpy_file()
# sample.find_data_array()
sample.make_animating_plot()