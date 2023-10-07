# Muse_2 Classification Project
This repo contains all the coding part related to the work of my Diploma thesis: __*Detection of eye and head movements via EEG and gyroscope signals & Classification with supervised deep learning methods*__, during the last year of my undergraduate studies at the *Computer Science and Engineering Department of University of Ioannina*. 
________________________________________________________________
#### HI-BI-BI / ASONAM 2023
A (4 page) research paper was developed based on this project, whose submission to the 
__HI-BI-BI/ASONAM 2023__ conference was accepted and will be published on *06-09/11/2023*:<br>
<sup>*N. Amvazas, S. Moschopoulos, K. Koritsoglou, G. Tatsis, I. Fudos, D. Tzovaras, <br>Introducing a highaccuracy brain-computer interface (BCI) for intelligent wheelchairs, Aug-Sept 2023.*<sup>

# Muse 2 Device
<img src="/Images/readme/Muse_2.png" style="display: inline-block; margin: 0 auto; max-width: 300px"><br>
- __Bluetooth Connectivity__: It connects to pc, smartphone or tablet (*iOS, Android*) via __Bluetooth__, enabling seamless data transfer and synchronization with the app.
- __Portable & Comfortable__: Lightweight and comfortable to wear during recording sessions.
- __EEG Sensors__: The device is equipped with __4 EEG__ (electroencephalogram) sensors (__*AF7,AF8,TP9,TP10*__) strategically placed on the headband, *based on the 10-20 system*, using the __Referential montage__ with __FPz__ as the Reference electrode. These sensors are designed to measure and record electrical activity from the user's brain. EEG sensors have a sampling rate of __256 Hz__, which means that they capture 256 data points (samples) per second from each sensor.<br> 
<img src="/Images/readme/Muse_10-20.png" style="display: inline-block; margin: 0 auto; max-width: 300px">
<sup>*Also Muse 2 has two micro-USB ports on the back of the ear pods where two auxiliary electrodes can be attached. These electrodes can be used to measure EMG, ECG, or EEG on other areas of the head or body.*<sup>
- __Gyroscope & Accelerometer Sensors__: The device is equipped with Gyroscope & Accelerometer sensors giving data in 3-axis __X,Y,Z__ with sampling rate of __52 Hz__.<br>
<sup> You can find more technical specifications about Muse 2 devices at [Muse_Technical_Specs](https://www.eegsales.com/Shared/images/General%20Use/PDF%20Files/Muse_Technical_Specs.pdf), [Muse 2](https://choosemuse.com/products/muse-2).<sup>
________________________________________________________________
## Requirements

- __Python__ _3.6 - 3.10_ <br>
- __MuseLSL__ *(Used for the signal recordings during the experimental procedure)*
- __pandas__ _v.2.0.2_ <br>
- __matplotlib__ _v.3.7.1_ <br>
- __numpy__ _v.1.24.3_ <br>
- __scipy__ _v.1.10.1_ <br>
- __mne__ _v.1.4.0_ <br>
- __sklearn__ _v.1.2.2_ <br>
- __tensorflow (keras)__ _v.2.10.0_

# Workflow Diagram

<img src="/Images/readme/Workflow.png" style="display: inline-block; margin: 0 auto; max-width: 700px"><br>
________________________________________________________________

# Files
- __RAW_MUSE_DATA:__ Contains raw signals, from recordings during the experimental procedure.Each session is stored as a separate *.csv* file.
<img src="/Images/readme/csv.png" style="display: inline-block; margin: 0 auto; max-width: 700px"><br>
- __MY_DATA:__ 
-- __Labeled_fragments__: Contains pickle *(.pkl)* files with Panda dataframes. Each dataframe corresponds to a specific movement extracted during the segmentation process (*segmentation_tool.py*).
-- __Split_Data__: Contains data that has been split into *train* & *test* sets and includes folds for cross-validation.
-- __Keras_Models__: Houses the __4__ *(deep learning)* trained models (__*MLP, LSTM, CNN, CNN-LSTM*__) *(for each iteration from cross validation)*.
- __*segmentation_tool.py*:__ The tool we designe to extract movements *(data)*, from each session of the experimental procedure.
- __*EEG_GS_Classification.ipynb*:__ Contains all the steps of the workflow (Preprocessing, Feature Extraction, Data Splitting, Model Training and Results).
________________________________________________________________

# Eye & Head Movements Categories with Labels
<table>
  <tr>
    <th>Labels</th>
    <th>Movements</th>
  </tr>
  <tr>
    <td>0</td>
    <td>Inactivity</td>
  </tr>
    <tr>
    <td>1</td>
    <td>Double Blink (Eyes)</td>
  </tr>
    <tr>
    <td>2</td>
    <td>Look Left (Eyes)</td>
  </tr>
    <tr>
    <td>3</td>
    <td>Look Right (Eyes)</td>
  </tr>
    <tr>
    <td>4</td>
    <td>Look Down (Eyes)</td>
  </tr>
    <tr>
    <td>5</td>
    <td>Look Up (Eyes)</td>
  </tr>
    <tr>
    <td>6</td>
    <td>Rotate Head Left (Head)</td>
  </tr>
    <tr>
    <td>7</td>
    <td>Rotate Head Right (Head)</td>
  </tr>
    <tr>
    <td>8</td>
    <td>Unknown</td>
  </tr>
</table>
________________________________________________________________

# Dataset
-Total Movements: __1098__
-Training Set: __80%__
-Test Set: __20%__
-Cross Validation: *k=__6__* folds *(from training set)*
<img src="/Images/readme/Dataset.png" style="display: inline-block; margin: 0 auto; max-width: 700px"><br>

________________________________________________________________

# Models
<img src="/Images/readme/models.png" style="display: inline-block; margin: 0 auto; max-width: 700px"><br>

________________________________________________________________

# Results
<img src="/Images/readme/Results.png" style="display: inline-block; margin: 0 auto; max-width: 900px"><br>
