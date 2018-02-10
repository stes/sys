import json
import numpy as np
import pandas as pd
import os

from collections import OrderedDict

import scipy.interpolate

def get_extract_dict():
    """ Topics and keys to extract """

    # specify the ROS topic keys to extract here.
    # it might helpful to consider these:
    #
    # "/roboy/middleware/MotorStatus/displacement/3"
    # "/roboy/middleware/MotorStatus/position/3"

    extract = [
        "/roboy/middleware/MotorStatus/displacement/3",
        "/roboy/middleware/MotorStatus/displacement/5",
        "/roboy/middleware/MotorStatus/displacement/6",
        "/roboy/middleware/MotorStatus/displacement/10",
        "/roboy/middleware/MotorStatus/displacement/12",
        "/roboy/middleware/MotorStatus/displacement/13",
        "/roboy/middleware/MotorStatus/position/3",
        "/roboy/middleware/MotorStatus/position/5",
        "/roboy/middleware/MotorStatus/position/6",
        "/roboy/middleware/MotorStatus/position/10",
        "/roboy/middleware/MotorStatus/position/12",
        "/roboy/middleware/MotorStatus/position/13",
        '/mocap/MarkerPose/position/x',
        '/mocap/MarkerPose/position/y',
        '/mocap/MarkerPose/position/z',
        ]

    return extract

def load_data(fname):
    """ Load a json file with recordings

    The file is converted into multiple pandas dataframes
    """
    with open(fname, 'r') as fp:
        data = json.load(fp)

    topics = []
    dfs = []
    for topic in data.keys():
        df = pd.DataFrame()
        df = df.from_dict(data[topic], orient="index")
        topics.append(topic)
        dfs.append(df)
        for key in df.columns:
            if isinstance(df[key][0], list):
                vals = df[key].values.tolist()
                topics.append(os.path.join(topic, key))
                dfs.append(pd.DataFrame(vals, index=df.index))

    return topics, {t : df for t,df in zip(topics,dfs)}

def interpolate(df_dict, extract):
    """ Merge dataframes for different topics and interpolate in time

    df_dict:
        dictionary mapping topic names to topic dataframes.
        the index is interpreted as the timestamp.
    extract:
        dictionary mapping topic names to column names that should be extracted

    returns:
        A single array containing the merged data frame

    """

    start, stop = [],[]
    n_timepoints = []
    for topic in extract:
        time = np.array(df_dict[topic].index).astype(int)
        start += [time.min()]
        stop  += [time.max()]
        n_timepoints += [len(time)]
    start = max(start)
    stop  = min(stop)

    n_timepoints = min(n_timepoints)
    t = np.linspace(start, stop, n_timepoints)

    data = []
    for topic in extract:
        X    = df_dict[topic].as_matrix()
        time = np.array(df_dict[topic].index).astype(int)

        f  = scipy.interpolate.interp1d(time, X, axis=0)
        X_ = f(t)

        data.append(X_)

    return np.concatenate(data, axis=1)

if __name__ == '__main__':
    import glob
    import os
    import h5py
    import sys

    if not len(sys.argv) >= 3:
        print("Usage: python {} [output file] [input files ...]".format(__file__))
        sys.exit(1)

    fname = sys.argv[1]
    files = sys.argv[2:]
    extract_dict = get_extract_dict()

    if os.path.exists(fname):
        print("File exists: {}".format(fname))

    with h5py.File(fname) as ds:
        for pattern in files:
            for f in glob.glob(pattern):
                name = os.path.basename(f).split('.')[0]
                print("Processing {}".format(name))
                topics, dfs = load_data(f)
                ds[name] = interpolate(dfs, extract_dict)
