# Generalized Seismic Phase Detection with Deep Learning [Modified by Akshay] 

This is a fork of the implementation of the Generalized Phase Detection (GPD) framework for seismic phase detection with deep learning: https://github.com/interseismic/generalized-phase-detection

GPD uses deep convolutional networks to learn generalized representations of millions of P-wave, S-wave, and noise seismograms that can be used for phase detection and picking. The framework is described in
```
Ross, Z. E., Meier, M.-A., Hauksson, E., and T. H. Heaton (2018). Generalized Seismic Phase Detection with Deep Learning, Bull. Seismol. Soc. Am., doi: 10.1785/0120180080 [arXiv:1805.01075]
```
The original authors have provided training datasets consisting of millions of seismograms at the Southern California Earthquake Data Center <http://scedc.caltech.edu/research-tools/deeplearning.html>. The authors welcome others to download these datasets and improve upon our model architecture as described in the paper.

## Requirements
- The models provided here require keras and tensorflow. You will need the two model files included here (`model_pol.json` and `model_pol_best.hdf5`) in order to run the script. Note that in order to use the trained model it is necessary to set up a Python 3.6 environment. Any other version of Python will result in errors when attempting to load the trained model.
- The authors recommended the use of GPUs to speed up computation. From my (Akshay's) experience, this is not necessary since only inference (and no training) is carried out.

## The gpd_predict script
This script is a very simple implementation of GPD for detection and picking of seismic waves in continuous data. The generic command for executing this script is,
```
python gpd_predict.py -V -I <input-file> -O <output file>
```
This will write a set of phase picks for the seismic traces specified in the `<input-file>` to `<output-file>`. Note that the script will create the output file if it does not exist. The script will also generate a plot of the three component traces, plot the picks, and the P- and S-wave probability streams.

The input file, specified with the -I flag, has an arbitrary number of rows and three columns. The columns correspond to the North, East, and Vertical channel filenames for a given chunk of 3-c data. Each row corresponds to the data for a different station. The files can be of arbitrary duration. All three components are necessary because GPD is a three-component detection framework.

gpd_predict has a few hyperparameters that can be adjusted to suit specific goals. They are all documented in the script (`gpd_predict.py`). Please see the BSSA paper to understand how the min_proba parameter works.

The model is trained assuming the data are 100 Hz sampling rate. The authors mention that it is best to run tests with data sampled at the same rate. That said, the script includes a flag to interpolate the data should you not want to experiment with these out of the box scenarios.

## Enhancements (by Akshay)

### New Test Data

The test data provided by the authors was a simple and not varied enought to showcase the capabilities of the trained model. New test data has been added to this repository. All of the data comes from a subset of 15 seismic stations which are part of the Canadian National Seismograph Network (CNSN). The data is organized as `data/Demo-event-{x}`.

Each folder consist of seismic traces (mseed files, 3 per station corresponding to each channel) in addition to Input files (one per station) which can be used to directly call the `gpd_predict.py` script. There is also text file which provides some basic information about the corresponding seismic event.

- `data/Demo-event-1` : Velocity data related to a 6 Magnitude earthquake which occurred off the coast of Vancouver Island on 2019-12-23T20:56:23.55 (UTC)
- `data/Demo-event-2` : Velocity data related to a 6.5 Magnitude earthquake which occurred off the coast of Vancouver Island on 2018-10-22T06:22:45.00 (UTC)
- `data/Demo-event-3` : Acceleration data related to a 6 Magnitude earthquake which occurred off the coast of Vancouver Island on 2019-12-23T20:56:23.55 (UTC)

### Improved Phase Picks

The trained CNN model produces a lot of false positives when making predictions about P and S picks. The `gpd_predict.py` script has been modified to include a simple heuristic based algorithm to produce better results. The flag `-C` can be added when running the script to turn on this enhancement.

### New Option to Store an Image of the Plot

The `-S` option can be used with the `gpd_predict.py` script to store the output graph at a location specified by the user.

### New Script for Bulk Processing Demo Data

An additional helper script called `gpd_predict_batch.py` has been created to run the model on multiple seismic streams and store the outputs in an organized manner. The script can be invoked in the following way.

```
python .\gpd_predict_batch.py -C -M <custom-output-directory> -I <input-data-folder>
```

- `-C` is an optional flag that can be passed in. When present, it turns on the enhancements which will reduce the false positives and improve results.
- `-M` is an optional flag that can be used to specify a custom output directory name. In the absence of this, the script will create a directory called `output` in the current working directory to store the results.
- `-I` is a mandatory flag that is used to specify the input directory containing the seismic traces and input files.

To run `gpd_predict_batch.py` on the new Demo data please run one of the following commands,

- `python .\gpd_predict_batch.py -C -M dm1-vel-clean -I .\data\Demo-event-1\`
- `python .\gpd_predict_batch.py -C -M dm2-vel-clean -I .\data\Demo-event-2\`
- `python .\gpd_predict_batch.py -C -M dm3-vel-clean -I .\data\Demo-event-3\`

The `-C` flag can be omitted to generate outputs without enhancements applied. Please also provide a different value with the `-M` flag in order to store outputs in easily identifiable folders.
