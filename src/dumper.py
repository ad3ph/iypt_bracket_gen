import pickle
import datetime

class Dumper:
    def __init__(self):
        self.X_storage = []
        self.y_storage = []
        

    def write_x(self, x):
        self.X_storage.append(x)
    
    def write_y(self, y):
        self.y_storage.append(y)

    def dump_pkl(self, file_suffix=None):
        self.file_name = {'x': f'./dumps/dump_x_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}', 
                          'y': f'./dumps/dump_y_{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}'}
        
        if file_suffix:
            self.file_name['x'] += file_suffix
            self.file_name['y'] += file_suffix

        with open(self.file_name['x']+'.pkl', 'wb') as f_x:
            pickle.dump(self.X_storage, f_x)
        with open(self.file_name['y']+'.pkl', 'wb') as f_y:
            pickle.dump(self.y_storage, f_y)