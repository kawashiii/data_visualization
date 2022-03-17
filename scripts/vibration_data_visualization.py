import os
import sys
import math

import pandas as pd
import matplotlib.pyplot as plt

import config

class DataVisualization(object):
    def __init__(self):
    	self.fig = plt.figure(figsize=(10, 18))

    def read_csv(self, file_path):
        self.df = pd.read_csv(file_path, encoding = 'UTF-8')

    def drop_df(self, start_index, end_index):
        drop_index_list = list(range(start_index, end_index))
        self.df.drop(drop_index_list, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

    def extract_target_index(self, index):
        value = 0
        for i, x in enumerate(self.df[index]):
            if i == 0: a = x

            if a != x:
                value = i
                break
        return value

    def get_size(self):
        return len(self.df)

    def insert(self, l, c, v):
        self.df.insert(loc=l, column=c, value=v)
        
    def update(self, i, f):
        self.df[i] = list(map(f, self.df[i]))

    def set_graph_config(self, c):
        for i, x in enumerate(c):
            ax1 = self.fig.add_subplot(3, 1, i+1)

            config = c[x]
            ax1.set_title(config['title'], fontsize=config['fontsize'])
            for k, y in enumerate(config['y1_index']):
                ax1.plot(self.df[config['x_index']], self.df[config['y1_index'][k]], label=config['y1_legend'][k], color=config['y1_plot_color'][k])

            ax1.set_xlabel(config['x_label'], fontsize=config['fontsize'])
            ax1.set_ylabel(config['y1_label'], fontsize=config['fontsize'])

            ax1.set_xlim(config['x_lim_min'], config['x_lim_max'](self.df[config['x_index']]))
            ax1.set_ylim(config['y1_lim_min'], config['y1_lim_max'])

            handler1, label1 = ax1.get_legend_handles_labels()
            if config['axis-len'] == 1:
                ax1.legend(handler1, label1, loc=2, borderaxespad=0, fontsize=10)
            elif config['axis-len'] == 2:
                ax2 = ax1.twinx()
                for k, y in enumerate(config['y2_index']):
                    ax2.plot(self.df[config['x_index']], self.df[config['y2_index'][k]], label=config['y2_legend'][k], color=config['y2_plot_color'][k])
                ax2.set_ylabel(config['y2_label'], fontsize=config['fontsize'])
                ax2.set_ylim(config['y2_lim_min'], config['y2_lim_max'])
                handler2, label2 = ax2.get_legend_handles_labels()
                ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0, fontsize=10)
	        
            ax1.grid(which = 'major', alpha = 0.8, linestyle = '--', linewidth = 1)

time_conv = lambda x: str(int(x[:2],16)).zfill(2) + "-" + str(int(x[2:4],16)).zfill(2) + "-" + str(int(x[4:6],16)).zfill(2) + " " + str(int(x[6:8],16)).zfill(2) + ":" + str(int(x[8:10],16)).zfill(2) + ":" + str(int(x[10:12],16)).zfill(2)
temp_conv = lambda x: str(x).zfill(4)
accel_conv = lambda x: "{:.8f}".format(round((int(str(x).zfill(4), 16) - (1<<16)  if int(str(x).zfill(4), 16) & (1 << 16 - 1) else int(str(x).zfill(4), 16)) * ACCEL_SCALE, 8))
gyro_conv = lambda x: "{:.8f}".format(round((int(str(x).zfill(4), 16) - (1<<16)  if int(str(x).zfill(4), 16) & (1 << 16 - 1) else int(str(x).zfill(4), 16)) * GYRO_SCALE, 8))

ACCEL_SCALE = 0.00097 
GYRO_SCALE  = 0.005
TEMP_SCALE = 0.1
HUMIDITY_SCALE = 0.1

def create_csv_file(file_path):
    with open(file_path, 'rb') as f:
        count = 0
        output = ['datetime,time,seq_no,sys_clock,accel_x,accel_y,accel_z,gyro_x,gyro_y,temperature,humidity\n']

        while True:
            data = f.read(154)
            if data == b'': break

            datetime = time_conv(data[20:26].hex()) + ','
            seq_no = str(int(data[12:14].hex(), 16)) + ','
            temperature = str(round(int(temp_conv(data[26:28].hex()), 16) * 0.1, 1)) + ','
            humidty = str(round(int(temp_conv(data[28:30].hex()), 16) * 0.1, 1)) + '\n'

            for i in range(34, 154, 12):
                data2 = data[i : (i+12)]
                time = str(count * 0.001) + ','
                sys_clock = str(int(data2[:2].hex(), 16)) + ','
                accel_x = str(accel_conv(data2[2:4].hex())) + ','
                accel_y = str(accel_conv(data2[4:6].hex())) + ','
                accel_z = str(accel_conv(data2[6:8].hex())) + ','
                gyro_x = str(gyro_conv(data2[8:10].hex())) + ','
                gyro_y = str(gyro_conv(data2[10:12].hex())) + ','

                output.append(datetime + time + seq_no + sys_clock + accel_x + accel_y + accel_z + gyro_x + gyro_y + temperature + humidty)

                count += 1

        with open('sample_vibration_data.csv', 'w') as output_file:
            for i in range(len(output)):
                output_file.write(output[i])

def main():
    #file_path = sys.argv[1]
    file_path = 'sample_vibration_data.dat'
    create_csv_file(file_path)

    ins = DataVisualization()
    file_path = 'sample_vibration_data.csv'
    ins.read_csv(file_path)

    ins.set_graph_config(config.vibration_graph_config)
    plt.subplots_adjust(wspace=0.5, hspace=0.4)
    plt.savefig("result.png", facecolor="azure", bbox_inches='tight', pad_inches=0.1)
    plt.show()         

if __name__ == '__main__':
    main()

