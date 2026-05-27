import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

from netCDF4 import Dataset
from os import listdir
from os.path import isfile, isdir, join, normpath
import sys

class case_creator():
    '''
    Class to set up Aspire cases in a nicer interface
    '''
    def __init__(self, rootDir):
        print("\x1b[1;30;41 !! Class is NOT a minimal working example !! \x1b[00m")
        self.rootDir = rootDir
    
class case_reader():
    '''
    Class to read out and postprocess Aspire case results
    '''
    def __init__(self, out_dir):
        print("\x1b[1;30;41 !! Class is NOT a minimal working example !! \x1b[00m")
        self.out_dir = out_dir

        # Collect output files
        self.outFiles = [f for f in listdir(normpath(self.out_dir)) if isfile(join(normpath(self.out_dir), f)) and "Out" in f]
        self.outPaths = [join(normpath(self.out_dir), f) for f in listdir(normpath(self.out_dir)) if isfile(join(normpath(self.out_dir), f)) and "Out" in f]
        print("\x1b[1;6;46m Found files: \x1b[0m")
        [print(f"\x1b[1;6;46m     {f} \x1b[0m") for f in self.outFiles]
    
    def print_outfile_summary(self):
        print("Output files summary")
        for p, f in zip(self.outPaths, self.outFiles):
            print(f"\x1b[95m {f}\x1b[00m")
            rootgrp = Dataset(p, "r", format="NETCDF4")
            print(f"{rootgrp}")

    def write_flowfield_video(self, ZIDX = 1):
        ## Get data
        ff_file = [(p, f) for p, f in zip(self.outPaths, self.outFiles) if "Slice" in f][0]
        print(f"Reading animation data from {ff_file[1]}...")
        rootgrp = Dataset(ff_file[0], "r", format="NETCDF4")

        print(f"Animating height {rootgrp['height_above_ground_level'][ZIDX]} m")

        ## Base plot
        fig, ax = plt.subplots(figsize=[12,4])
        title = ax.set_title("t = not started")
        ax.set( aspect='equal', xlabel="x", ylabel="y")

        ## Writer
        metadata = dict(title=f'Aspire animation from {self.out_dir}', artist='SA Umans')
        writer = anim.FFMpegWriter(fps=1, metadata=metadata)

        ## Loop
        K = rootgrp['time'].size
        X, Y = rootgrp['xf'][:], rootgrp['yf'][:]
        VEL = np.sqrt(rootgrp['u'][:,ZIDX,:-1,:-1]**2 + rootgrp['v'][:,ZIDX,:-1,:-1]**2 )
        # with writer.saving(fig, "animation.mp4",100):
        #     for k in range(K):
        k=20
        pcol = ax.pcolorfast(X,Y , VEL[k,:,:])
        title.set_text(f"t = {rootgrp['time'][k]:n}")

                # writer.grab_frame()
                # pcol.remove()

                # prog = (k*10) // K +1
                # sys.stdout.flush()
                # sys.stdout.write(f"\rProgress : |{"\x1b[0;30;47m \x1b[0m" * prog}{" " * (10 - prog)}| {(k*100)//K+1:3d}%")

        fig.savefig("dump/plot1.png")

def show_ansi_table():
    for style in range(5):  # 0: normal, 1: bold/bright
        for fg in list(range(30, 38))+list(range(90, 98)): 
            for bg in list(range(40, 48))+list(range(100, 108)):
                code = f"{style};{fg};{bg}"
                print(f"\x1b[{code}m {code} \x1b[0m", end=" ")
            print()  # Newline after each row
        print()  # Extra newline between normal and bold

if __name__=="__main__":
    cr = case_reader(out_dir = r"/home/sachinumans/02_Code/220113_2WF/2022/01/13/00/")
    # cr.print_outfile_summary()
    # cr.write_flowfield_video()

    # show_ansi_table()
    