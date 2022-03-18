import os
import sys
import math

import pandas as pd
import matplotlib.pyplot as plt

import config

class DataVisualization(object):
    def __init__(self):
    	self.fig = plt.figure(figsize=(20, 18))

    def read_csv(self, file_path):
        self.df = pd.read_csv(file_path, header = 2, encoding = 'UTF-8')

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

    def set_text(self):
        ax = self.fig.add_subplot(3, 3, 1)
        ax.set_axis_off()
        ax.text(0, 0.2, 'cycle count: ' + str(self.df['D410'][0]), fontsize=14)
        ax.text(0, 0.4, 'datetime: ' + str(self.df['TIME'][0]), fontsize=14)

    def set_graph_config(self, c):
        for i, x in enumerate(c):
            ax1 = self.fig.add_subplot(3, 3, i+2)

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

def main():
    ins = DataVisualization()
    file_path = sys.argv[1]
    dir_name = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    #file_path = "sample_plc_data.csv"
    #print(file_path)
    ins.read_csv(file_path)

    target_first_index = ins.extract_target_index('D410')
    ins.drop_df(0, target_first_index)
    target_end_index = ins.extract_target_index('D410')
    ins.drop_df(target_end_index, ins.get_size())

    ins.insert(0, 'eTime', [n / 1000000 for n in range(0, 2000*ins.get_size(), 2000)])
    ins.update('D16', lambda x: x / 10000)
    ins.update('D22', lambda x: x / 10)
    ins.update('D66', lambda x: x / 10000)
    ins.update('D72', lambda x: x / 10)
    ins.update('D116', lambda x: x / 10000)
    ins.update('D122', lambda x: x / 10)
    ins.update('D166', lambda x: x / 100000)
    ins.update('D172', lambda x: x / 10)
    ins.update('D216', lambda x: x / 100000)
    ins.update('D222', lambda x: x / 10)
    ins.update('D266', lambda x: x / 10000)
    ins.update('D272', lambda x: x / 10)
    ins.update('D316', lambda x: x / 100000)
    ins.update('D322', lambda x: x / 10)

    ins.set_text()
    ins.set_graph_config(config.plc_graph_config)

    plt.subplots_adjust(wspace=0.5, hspace=0.4)
    plt.savefig(dir_name + "/PLC_log.png", facecolor="azure", bbox_inches='tight', pad_inches=0.1)
    plt.show()

if __name__ == '__main__':
    main()

