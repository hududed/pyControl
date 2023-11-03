import pandas as pd
import numpy as np
import os, csv
from pathlib import Path
from random import randrange
from datetime import date


def create_new_path(path: Path, series: int, batch: bool = False) -> Path:
    """Creates a new path for the campaign
    path: Path of the campaign
    series: Campaign number
    """
    if batch:
        p = str(date.today()) + "-BATCH-" + str(series)
    else:
        p = str(date.today()) + "-Series-" + str(series)

    os.chdir(path)
    if os.path.exists(p):
        raise FileExistsError(f"Directory {p} already exists")
    os.mkdir(p)
    os.chdir(p)

    return Path(os.getcwd())


def write_data_files(
    path: Path,
    series: int,
    nr_random_lines: int = 7,
    param1_range: tuple = (1, 10),
    param2_range: tuple = (1, 10),
    param3_range: tuple = (1, 100),
    batch: bool = True,
) -> Path:
    param1 = []
    param2 = []
    param3 = []
    output = []

    print("TODAY's DATE:", str(date.today()))

    for x in range(nr_random_lines):
        param1_value = randrange(param1_range[0], param1_range[1], 1)
        param2_value = randrange(param2_range[0], param2_range[1], 1)
        param3_value = randrange(param3_range[0], param3_range[1], 1)

        param1.append(param1_value)
        param2.append(param2_value)
        param3.append(param3_value)
        output.append(None)

    # Create a DataFrame with 'param1', 'param2', 'param3', and 'output' as columns
    df = pd.DataFrame(
        {"param1": param1, "param2": param2, "param3": param3, "output": output}
    )

    # Write the DataFrame to 'data.csv'
    df.to_csv("data.csv", index=False)

    return path


def write_laser_data_files(
    path: Path,
    series: int,
    nr_random_lines: int = 7,
    power_range: set = (5, 1190),
    time_range: set = (1050, 5000),
    pressure_range: set = (100, 350),
    batch: bool = False,
    passes_range: set = np.arange(1, 10),
    defocus_range: set = (-3, 0),
) -> Path:
    """Writes data files with the parameter design at path:
    path: Path of the campaign
    series: Campaign number
    nr_random_lines: Number of starting lines, defaults at 7
    power_range: set of minPower, maxPower, default (5, 1190)
    time_range: set of minTime, maxTime, default (1050, 5000)
    pressure_range: set of minPressure, maxPressure, default (100,350)
    """
    power = []
    line_time = []
    pressure = []
    line_passes = []
    defocus = []

    print("TODAY's DATE:", str(date.today()))

    for x in range(nr_random_lines):
        powr = randrange(power_range[0], power_range[1], 1)  # in mW
        tm = randrange(time_range[0], time_range[1], 1)  # in ms
        pr = randrange(pressure_range[0], pressure_range[1], 10)  # in psi
        passes = randrange(passes_range[0], passes_range[1], 1)  # passes
        defoc = (
            randrange(int(defocus_range[0] * 100), int(defocus_range[1] * 100), 1) / 100
        )
        for i in range(9):
            power.append(powr)
            line_time.append(tm)
            pressure.append(pr)
            line_passes.append(passes)
            defocus.append(defoc)

    print(
        f"POWER: {power_range}\n",
        f"TIME: {time_range}\n",
        f"PRESSURE: {pressure_range}",
    )

    data_header = [
        "power",
        "time",
        "pressure",
        "passes",
        "defocus",
        "ratio",
        "resistance",
    ]
    plot_header = [
        "power",
        "time",
        "pressure",
        "passes",
        "defocus",
        "dummy_ratio",
        "pred_mean",
        "pred_upper",
        "ei",
    ]

    # rename this to raw_post_processed.csv
    with open("dataset.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data_header)
        writer.writerows(zip(power, line_time, pressure, line_passes, defocus))

    # rename this to raw_pre-patterning.csv
    with open("dataset-pre.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data_header)
        writer.writerows(zip(power, line_time, pressure, line_passes, defocus))

    # THIS HAS THREE ADDITIONAL COLUMNS
    with open("plot_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(plot_header)

    # THIS HAS THREE ADDITIONAL COLUMNS
    with open("fit_results.csv", "w", newline="") as f:
        fit_header = [
            "D",
            "PD",
            "WD",
            "FD",
            "D1",
            "PD1",
            "WD1",
            "FD1",
            "G",
            "PG",
            "WG",
            "FG",
            "2D",
            "P2D",
            "W2D",
            "F2D",
            "GD",
            "2DG",
            "file",
        ]
        writer = csv.writer(f)
        writer.writerow(fit_header)

    df2 = pd.read_csv("dataset.csv")
    df2 = df2.drop_duplicates()  # keep only the unique rows
    df2.to_csv(
        "data.csv", index=False
    )  # this is what will be read by mlrMBO in th R code

    return Path(os.getcwd())


# def write_data_files(path: Path, series: int, nr_random_lines: int = 7, \
#     power_range: set = (5,1190), time_range: set = (1050,5000), pressure_range: set = (100,350), \
#      batch: bool = False, passes_range: set = np.arange(1,10),
#      defocus_range: set = (-3,0)) -> None:
#         """ Writes data files with the parameter design at path:
#             path: Path of the campaign
#             series: Campaign number
#             nr_random_lines: Number of starting lines, defaults at 7
#             power_range: set of minPower, maxPower, default (5, 1190)
#             time_range: set of minTime, maxTime, default (1050, 5000)
#             pressure_range: set of minPressure, maxPressure, default (100,350)
#         """
#         power=[]
#         line_time=[]
#         pressure=[]
#         line_passes=[]
#         defocus = []

#         print("TODAY's DATE:",str(date.today()))

#         for x in range(nr_random_lines):
#             powr = randrange(power_range[0], power_range[1], 1) # in mW
#             tm = randrange(time_range[0], time_range[1], 1) # in ms
#             pr = randrange(pressure_range[0], pressure_range[1], 10) # in psi
#             passes = randrange(passes_range[0], passes_range[1], 1) #passes
#             defoc = randrange(int(defocus_range[0]*100), int(defocus_range[1]*100),1)/100
#             for i in range(9):
#                 power.append(powr)
#                 line_time.append(tm)
#                 pressure.append(pr)
#                 line_passes.append(passes)
#                 defocus.append(defoc)

#         print(f"POWER: {power_range}\n",
#               f"TIME: {time_range}\n",
#               f"PRESSURE: {pressure_range}")

#         if batch:
#             p = str(date.today()) + "-BATCH-" + str(series)
#             data_header=['power','time','pressure','passes','defocus','ratio','resistance']
#             plot_header=['power','time','pressure','passes','defocus','dummy_ratio', 'dummy_resistance', \
#                          'pred_mean', 'pred_upper', 'ei']
#         else:
#             p = str(date.today()) + "-Series-" + str(series)
#             data_header=['power','time','pressure','passes','defocus','ratio']
#             plot_header=['power','time','pressure','passes','defocus','dummy_ratio', \
#                         'pred_mean', 'pred_upper', 'ei']

#         print(f"Here is the new Campaign Folder:{p}")
#         # path = Path(r'c:\\Users\\UWAdmin\\Desktop\\_pyControl\\campaigns')
#         os.chdir(path)
#         os.mkdir(p)
#         os.chdir(p)

#         fit_header=['D','PD','WD','FD','D1','PD1','WD1','FD1',\
#                     'G','PG','WG','FG','2D','P2D','W2D','F2D','GD','2DG','file']
#         #rename this to raw_post_processed.csv
#         with open('dataset.csv', 'w', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(data_header)
#                 writer.writerows(zip(power, line_time, pressure,line_passes,defocus))

#         #rename this to raw_pre-patterning.csv
#         with open('dataset-pre.csv', 'w', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(data_header)
#                 writer.writerows(zip(power, line_time, pressure,line_passes,defocus))

#         # THIS HAS THREE ADDITIONAL COLUMNS
#         with open('plot_data.csv', 'w', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(plot_header)
#                 # writer.writerows(zip(power, line_time, pressure))

#          # THIS HAS THREE ADDITIONAL COLUMNS
#         with open('fit_results.csv', 'w', newline='') as f:
#                 writer = csv.writer(f)
#                 writer.writerow(fit_header)
#                 # writer.writerows(zip(power, line_time, pressure))

#         df2=pd.read_csv('dataset.csv')
#         df2=df2.drop_duplicates() #keep only the unique rows
#         df2.head()
#         df2.to_csv('data.csv',index=False) #this is what will be read by mlrMBO in th R code


def duplicate_to_dataset(
    nr_proposed_lines: int = 1, prepattern: bool = False, rep: int = 9
) -> None:
    data = pd.read_csv("data.csv")
    dataset = pd.read_csv("dataset.csv")

    proposed = data.iloc[-nr_proposed_lines:]
    repeated_data = pd.DataFrame(np.repeat(proposed.values, rep, axis=0))
    repeated_data.columns = proposed.columns
    new_dataset = pd.concat([dataset, repeated_data])
    new_dataset.to_csv("dataset.csv", index=False)
    if prepattern:
        dataset_pre = pd.read_csv("dataset-pre.csv")
        new_dataset_pre = pd.concat([dataset_pre, repeated_data])
        new_dataset_pre.to_csv("dataset-pre.csv", index=False)


def write_more() -> None:
    """
    Used after doing the AI stuff
    """
    d = pd.read_csv("data.csv")
    ln = d.shape[0]

    vpower = d["power"][ln - 1]
    vtime = d["time"][ln - 1]
    vpressure = d["pressure"][ln - 1]

    d1 = pd.read_csv("dataset.csv")
    ln = d1.shape[0]
    d1.loc[ln, "power"] = vpower
    d1.loc[ln, "time"] = vtime
    d1.loc[ln, "pressure"] = vpressure
    d1.to_csv("dataset.csv", index=False)
    d1.to_csv("dataset-pre.csv", index=False)


def repeats() -> None:
    # d1 = pd.read_csv('data.csv')
    df2 = pd.read_csv("dataset.csv")
    ln = len(df2["power"])
    m = ln
    print(f"DATASET LENGTH: {ln}")
    counter = m
    for i in range(8):
        toAdd = [df2["power"][m - 1], df2["time"][m - 1], df2["pressure"][m - 1]]
        filename = "dataset.csv"
        with open(filename, "r") as infile:
            reader = list(csv.reader(infile))
            reader.insert(counter + 1, toAdd)

        with open(filename, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            for line in reader:
                writer.writerow(line)

    for i in range(8):
        toAdd = [df2["power"][m - 1], df2["time"][m - 1], df2["pressure"][m - 1]]
        filename = "dataset-pre.csv"
        with open(filename, "r") as infile:
            reader = list(csv.reader(infile))
            reader.insert(counter + 1, toAdd)

        with open(filename, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            for line in reader:
                writer.writerow(line)


def get_mean(
    steps: int, save_line: int, spots_measured: int, target: str = "ratio"
) -> float:
    """Extracts the mean of the last 'steps' lines of the dataset.csv file
    to data.csv
    """

    print(os.getcwd())
    df = pd.read_csv("dataset.csv")
    # spots_measured = save_line/steps
    result = df[target].iloc[steps : steps + spots_measured].mean()
    print(f"Filling nans with 0")
    df[target][steps : steps + spots_measured].fillna(0, inplace=True)
    df.to_csv("dataset.csv", index=False)

    df2 = pd.read_csv("data.csv")
    print(f"saving mean {result} to data.csv")
    df2.loc[save_line, target] = result
    df2.to_csv("data.csv", index=False)
    return result


def get_move_y(lines: int, start_y: int, step_y: int = 1) -> list:
    move_y = [0 for i in range(int(lines))]
    for i in range(int(lines)):
        #     print(i)
        if i == 0:
            move_y[i] = float(start_y)
        if i > 0:
            move_y[i] = float(move_y[i - 1]) + float(step_y)
    return move_y
