import os, pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import Tk, Text, TOP, BOTH, INSERT
from scipy import signal

"""---------------------------------------------------------------------SETUP------------------------------------------------------------------------"""

HEADER_NUM = 0
MODE = "EEG-GS"                                                         # Set the file type (Can be "EEG" or "GYROSCOPE" or "EEG-GS").
                                                                        # Set the EEG channels u want to use.                                      
CHANNELS = ['AF7', 'AF8', 'TP9', 'TP10','X', 'Y', 'Z']
#CHANNELS = ['AF7', 'AF8', 'TP9', 'TP10'] 
#CHANNELS = ['X', 'Y', 'Z']            

FS = 256                                                                # Set Sample Rate (Hz) || If APPLY_RESAMPLING = True then FS is the new FS.
WINDOW_LENGHT = 3                                                       # Set Segmentation Window Lenght (sec).
APPLY_DETRENDING = False
USER_SETS_FILENAME = True

# Set the path & name of the folder in which the fragments of the signals will be stored.
FRAGMENTS_FOLDER_NAME = 'Epochs'

#FRAGMENTS_FOLDER_NAME = "set file path"
"""--------------------------------------------------------------------------------------------------------------------------------------------------"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

"""--------------------------------------------------------------------------------------------------------------------------------------------------"""

def show_description_window(event):
    my_text = ("Info:\n" + "FS = " + str(FS) + " Hz" + "\nWINDOW_LENGHT = " + str(WINDOW_LENGHT) + " sec" + "\n\nHelp:"+
                "\n<Right Click> : Create fragment window" +
                "\n<Backspace> : Delete last window" +
                "\n<Enter> or <Esc> : Submit windows & Close\n\n")
    root = Tk()
    root.geometry("470x300")
    root.title("Description")
    text = Text(root, background="lightyellow")
    text.tag_configure("black", foreground="black")
    text.tag_configure("darkgrey", foreground="darkgrey")
    text.tag_configure("red", foreground="red")
    text.tag_configure("green", foreground="green")
    text.tag_configure("blue", foreground="blue")
    text.tag_configure("orange", foreground="orange")
    text.tag_configure("teal", foreground="teal")
    text.tag_configure("cyan", foreground="cyan")
    text.tag_configure("purple", foreground="purple")
    text.tag_configure("magenta", foreground="magenta")
    text.insert(INSERT, my_text,"black")
    text.insert(INSERT, "• <0> : Label 0: Ιnactivity (default)\n", "darkgrey")
    text.insert(INSERT, "• <1> : Label 1\n", "red")
    text.insert(INSERT, "• <2> : Label 2\n", "green")
    text.insert(INSERT, "• <3> : Label 3\n", "blue")
    text.insert(INSERT, "• <4> : Label 4\n", "orange")
    text.insert(INSERT, "• <5> : Label 5\n", "teal")
    text.insert(INSERT, "• <6> : Label 6\n", "cyan")
    text.insert(INSERT, "• <7> : Label 7\n", "purple")
    text.insert(INSERT, "• <8> : Label 8\n", "magenta")
    text.config(state="disabled")
    text.pack(side=TOP, fill=BOTH, expand=True)
    root.mainloop()


def on_right_click(event,fig,ax_list,signals,movements_list,points,windows,label_id,sample_rate,window_lenght) -> None:
    """
    Function to handle right click events.    
    """
    # Set label ID
    if label_id[0] == 0 : color = "darkgrey"
    elif label_id[0] == 1 : color = "red"
    elif label_id[0] == 2 : color = "green"
    elif label_id[0] == 3 : color = "blue"
    elif label_id[0] == 4 : color = "orange"
    elif label_id[0] == 5 : color = "teal"
    elif label_id[0] == 6 : color = "cyan"
    elif label_id[0] == 7 : color = "purple"
    elif label_id[0] == 8 : color = "magenta"
    # Check if the event was a right click
    if event.button == 3:
        # Get the x-axis position of the right click
        x = int(event.xdata)
        # Create window borders
        span_start = x - (window_lenght/2)*sample_rate
        span_end = x + (window_lenght/2)*sample_rate
        # Check if window borders are correct
        if(span_start>=0 and span_end<=len(signals[0])):
            # Add movement
            movements_list[0].append(label_id[0]), movements_list[1].append(x)
            # Add a colored dot to each signal plot
            for i in range(len(ax_list)):
                points[i].append(ax_list[i].scatter(x, signals[i][x], c=color, zorder=2))
            # Add a vertical span to each signal plot
            for i in range(len(ax_list)):
                windows[i].append(ax_list[i].axvspan(span_start, span_end, color=color, alpha=0.4))
            # Print message to console
            print("\tSignal Fragment Added")
            # Update plots
            fig.canvas.draw()
        else: print(f"\t{bcolors.WARNING}WARNING ---> The window you define is out of the signal borders. Please re-define your window.{bcolors.ENDC}")


def on_key_press(event,fig,movements_list,points,windows,label_id) -> None:
    """
    Connect the key press event to the function.
    Keyboard buttons description:
        - Backspace: Erase last segmentation
        - ESC or Enter: Close plot / Submit your signal windows
        - Numbers 0-4: Set label    
    """
    if event.key == 'backspace':
        if len(points[0])>0:
            for i in range(len(points)):
                point = points[i].pop()
                point.remove()
                window = windows[i].pop()
                window.remove()
            movements_list[0].pop(), movements_list[1].pop()
            print("\tLast Signal Fragment Erased")
        else:
            print("\tEmpty - No fragment to delete")
        fig.canvas.draw()
    elif event.key == 'escape' or event.key == 'enter':
        plt.close()
    elif event.key == '0':
        label_id.pop()
        label_id.append(0)
    elif event.key == '1':
        label_id.pop()
        label_id.append(1)
    elif event.key == '2':
        label_id.pop()
        label_id.append(2)
    elif event.key == '3':
        label_id.pop()
        label_id.append(3)
    elif event.key == '4':
        label_id.pop()
        label_id.append(4)
    elif event.key == '5':
        label_id.pop()
        label_id.append(5)
    elif event.key == '6':
        label_id.pop()
        label_id.append(6)
    elif event.key == '7':
        label_id.pop()
        label_id.append(7)
    elif event.key == '8':
        label_id.pop()
        label_id.append(8)
    

def create_figure(signals, mode, Fs, window_lenght):
    # Set the style to use a gray background and gridlines
    plt.style.use('default')

    if(mode == "EEG" and len(signals) == 4):
        # Create a figure and axes
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)
        #fig.subplots_adjust(left=0.25), fig.subplots_adjust(right=0.975)
        fig.subplots_adjust(top=0.93), fig.subplots_adjust(bottom=0.09)
        fig.text(0.5, 0.02, 'Samples', ha='center', fontsize=10)
        fig.text(0.05, 0.5, 'Amplitude (Voltage [$\mu V$]) ', va='center', rotation='vertical',fontsize=10)
        fig.suptitle('EEG Signals Segmentation/Labeling', fontsize=16)
        axs = [ax1,ax2,ax3,ax4]
        # Plot signals
        ax1.plot(signals[0],label=CHANNELS[0],color="blue")
        ax2.plot(signals[1],label=CHANNELS[1],color="red")
        ax3.plot(signals[2],label=CHANNELS[2],color="green")
        ax4.plot(signals[3],label=CHANNELS[3],color="black")
    elif((mode == "GYROSCOPE") and len(signals) == 3):
        # Create a figure and axes
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        fig.subplots_adjust(top=0.93), fig.subplots_adjust(bottom=0.09)
        fig.text(0.5, 0.02, 'Samples', ha='center', fontsize=10)
        fig.text(0.05, 0.5, 'Amplitude (Voltage [$\mu V$]) ', va='center', rotation='vertical',fontsize=10)
        fig.suptitle('Gyroscope Signals Segmentation/Labeling', fontsize=16)
        axs = [ax1,ax2,ax3]
        # Plot signals
        ax1.plot(signals[0],label=CHANNELS[0],color="darkcyan")
        ax2.plot(signals[1],label=CHANNELS[1],color="purple")
        ax3.plot(signals[2],label=CHANNELS[2],color="orange")
    elif((mode == "EEG-GS") and len(signals) == 7):
        # Create a figure and axes
        fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7, 1)
        fig.subplots_adjust(top=0.93), fig.subplots_adjust(bottom=0.09)
        fig.text(0.5, 0.02, 'Samples', ha='center', fontsize=10)
        fig.text(0.05, 0.5, 'Amplitude (Voltage [$\mu V$]) ', va='center', rotation='vertical',fontsize=10)
        fig.suptitle('EEG & Gyroscope Signals Segmentation/Labeling', fontsize=16)
        axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7]
        # Plot signals
        ax1.plot(signals[0],label=CHANNELS[0],color="blue")
        ax2.plot(signals[1],label=CHANNELS[1],color="red")
        ax3.plot(signals[2],label=CHANNELS[2],color="green")
        ax4.plot(signals[3],label=CHANNELS[3],color="black")
        ax5.plot(signals[4],label=CHANNELS[4],color="darkcyan")
        ax6.plot(signals[5],label=CHANNELS[5],color="purple")
        ax7.plot(signals[6],label=CHANNELS[6],color="orange")
    else:
        print("\tERROR in creating figure!")
        return [-1],[-1]
    
    # Set legend and grid
    for ax in axs: 
        ax.legend(loc='upper right')
        ax.grid()
    # Initialize lists of points and windows for each axis
    points = [[] for _ in range(len(axs))]
    windows = [[] for _ in range(len(axs))]

    # Init movements list
    movements_list = [[],[]]
    # Init label ID
    label_id = [0]

    # Create Description Button
    plt.subplots_adjust(top=0.945,bottom=0.055,left=0.080,right=0.970,hspace=0.255)
    callback = show_description_window
    ax_button = plt.axes([0.01, 0.9, 0.05, 0.05])
    button = Button(ax_button, 'Description')
    button.on_clicked(callback)

    # Connect the keyboard events to the function
    fig.canvas.mpl_connect('key_press_event', lambda event: on_key_press(event,fig,movements_list,points,windows,label_id))
    # Connect the right click event to the function
    fig.canvas.mpl_connect("button_press_event", lambda event: on_right_click(event,fig,axs,signals,movements_list,points,windows,label_id, Fs, window_lenght))

    # Show the plot
    plt.show()
    
    # Return movements list
    return movements_list[0], movements_list[1] 


def create_dataframe(dataframe, movement_marker_list, movement_label_list, fs, window_lenght):
    df_columns = ['Sample_Counter'] + CHANNELS + ['Label']
    df = pd.DataFrame(columns = df_columns)
    row = 0
    for i in range(len(movement_marker_list)):
        left_window_border = movement_marker_list[i] - ((fs * (window_lenght/2)) - 1)
        signal_window = [left_window_border]
        for j in range((fs * window_lenght) - 1):
            left_window_border = left_window_border + 1
            signal_window.append(left_window_border)
        data_window = dataframe.take(signal_window)

        for sample in range(len(data_window)): # len(data_window) = 512 samples (if fs=128 and window_size = 4sec) 
            
            info = [sample, *data_window.iloc[sample], movement_label_list[i]]
            """
            if(muse_mode=="EEG"):
                info = [sample, data_window.iloc[sample][0], data_window.iloc[sample][1],data_window.iloc[sample][2],data_window.iloc[sample][3], movement_label_list[i]]
            elif(muse_mode=="GYROSCOPE"):
                info = [sample, data_window.iloc[sample][0], data_window.iloc[sample][1],data_window.iloc[sample][2], movement_label_list[i]]
            """
            df.loc[row] = info
            row += 1
    return df

"""--------------------------------------------------------------------------------------------------------------------------------------------------"""

def signal_Segmentation(signal_df:pd, channels, Fs=128, window_lenght = 4):

    """
    Description
    ----------
    A tool that splits the given signal dataframe into labeled fragments based on markers you set.

    Parameters
    ----------
    signal_df : pandas.DataFrame
        The signal dataframe must containing exactly 
            4 columns: EEG signals or 
            3 columns: Gyroscope signals
    *Fs : int
        Sample rate (128 Hz by default).
    *window_lenght : int
        The length of each window in seconds (4 sec by default)

    Returns
    -------
    pandas.DataFrame
        1 dataFrame which contains each window/fragment and its label.
        
    Notes
    -----
    - Depending on the dataframe structure that is imported the mode can be: EEG (4 signals) or Gyroscope(3 signals).

    """
    print(f"{bcolors.OKBLUE}Segmentation Tool Started.{bcolors.ENDC}")
    signals = signal_df.transpose().values
    
    # Checking if Num of Channels is right
    if (MODE == "EEG" and len(signals)==4): mode = "EEG"   
    elif (MODE == "GYROSCOPE" and len(signals)==3) : mode = "GYROSCOPE"
    elif (MODE == "EEG-GS" and len(signals)==7) : mode = "EEG-GS"
    else:
        empty_df = pd.DataFrame() 
        print(f"{bcolors.FAIL}\tWARNING ---> The dataframe structure being imported is incorrect.\n\t" +
                "The dataframe must have:\n\t" +
                "Exactly 4 columns/signals in EEG mode or\n"+
                "\tExactly 3 columns/signals (X,Y,Z) in Gyroscope mode or\n" +
                "\tExactly 7 columns/signals 4 EEG and 3 Gyroscope (X,Y,Z) in EEG-GS mode.\n" +
                "\tPlease check if you have given the correct arguments to SETUP section of the segmentation_tool.py." + f"{bcolors.ENDC}"
            )
        return empty_df
    print("\tSegmentation tool Mode: " + f"{bcolors.OKGREEN}"  + mode + f"{bcolors.ENDC}")

    labels_list, window_markers_list = create_figure(signals, mode, Fs, window_lenght)

    if (labels_list and window_markers_list):
        # Combine the two lists into a list of tuples
        zipped_lists = list(zip(labels_list, window_markers_list))
        # Sort the list of tuples based on the first element of each tuple
        zipped_lists.sort(key=lambda x: x[0])
        # Unpack the sorted list of tuples back into two separate lists
        labels_list, window_markers_list = zip(*zipped_lists)

    print(f"{bcolors.OKBLUE}Segmentation Tool Terminated ---> {bcolors.OKCYAN}" + str(len(window_markers_list)) + f" signal fragment/s created. {bcolors.ENDC}")
    return create_dataframe(signal_df, window_markers_list, labels_list,Fs,window_lenght)

"""--------------------------------------------------------------------------------------------------------------------------------------------------"""

def load_file():
    # User enters the file path
    file_path = input('Enter a file path: ')
    if(USER_SETS_FILENAME): filename = input('Name the .pkl file before saving. Enter filename: ')
    else: filename = os.path.splitext(os.path.basename(file_path))[0]
    try:
        dataframe = pd.read_csv(file_path, header = HEADER_NUM, usecols = CHANNELS) 
        dataframe = dataframe.loc[:, CHANNELS]
        return dataframe, filename
    except ValueError:
        print(f"{bcolors.FAIL}Oops! There was a problem loading this file.\n" +
                "Please check if you have given the correct arguments to SETUP section of the segmentation_tool.py.\n"
                "If everything is correct then your file structure is probably not correct." + f"{bcolors.ENDC}"
            )
        exit()

def detranding(signals_dataset:pd):
    """
    Description
    ----------
    Using SciPy's signal.detrend function to detrend (Remove the DC offset) each EEG/Gyroscope signal fragmnet.
    
    Parameters
    ----------
    fragment_dataset (pandas.DataFrame): A dataframe containing signals.
    
    Returns
    -------
    pandas.DataFrame: A new dataframe with the DC offset removed from each signal.
    """
    detrended = signal.detrend(signals_dataset, axis=0)
    detrended_df = pd.DataFrame(detrended, columns=signals_dataset.columns)
    return detrended_df

"""--------------------------------------------------------------------------------------------------------------------------------------------------"""

def main():
    # Load the channels you choose from Raw File
    raw_signal_dataframe, filename = load_file()
    
    # Signal Segmantation
    if(APPLY_DETRENDING): fragments_dataset = signal_Segmentation(detranding(raw_signal_dataframe), CHANNELS, Fs=FS,window_lenght=WINDOW_LENGHT)
    else: fragments_dataset = signal_Segmentation(raw_signal_dataframe, CHANNELS, Fs=FS,window_lenght=WINDOW_LENGHT)
    if(fragments_dataset.empty): 
        print("No Signal Fragments - Exit.")
        exit()
    else: print("Signal Segmentation applied") #, print(fragments_dataset)

    # Split the dataframe into windows
    window_size = FS * WINDOW_LENGHT
        
    fragment_dfs, labels = [], []
    for i in range(0, len(fragments_dataset), window_size):
            window_label = fragments_dataset['Label'].iloc[i]
            window_df = fragments_dataset.iloc[i:i+window_size].drop(['Sample_Counter','Label'],axis=1).reset_index(drop=True)
            fragment_dfs.append(window_df)
            labels.append(window_label)

    # Save Fragments
    data = {"df_lsit" : fragment_dfs , "df_labels" : labels}
    if not os.path.exists(FRAGMENTS_FOLDER_NAME):
        os.makedirs(FRAGMENTS_FOLDER_NAME)
        print(f"Folder '{FRAGMENTS_FOLDER_NAME}' created.")
    file_path = FRAGMENTS_FOLDER_NAME + "//" + filename + ".pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(data,f)

if __name__ == "__main__":
    main()