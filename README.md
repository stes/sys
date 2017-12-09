# ml-system-identification

## Data recording for roboy

For recording data, first use `rosbag` to record the data from a collection of topics:

```
rosbag record -O recording_file /roboy/middleware/MotorStatus
```

This creates a file `recording_file.bag` which can then be converted into json by calling

```
python recording_file.py first_record.bag /roboy/middleware/MotorStatus output_file.json
```

To loop over all `.bag` files in a directory, use something like

```
for fp in $(ls *.bag); do python convert_bag.py $fp /roboy/middleware/MotorStatus $fp.json; done
```

## Data loading into numpy

To load the generated files into a numpy array, follow the steps in the notebook `Roboy Data Loading`.
