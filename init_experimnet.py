from config import settings
import math
import numpy as np
import pandas as pd
import random


def get_fog_node(zone_length, communication_range):
    number = math.floor(zone_length / (2 * communication_range))
    id = 0
    fog_node = []
    for i in range(number):
        x = communication_range + i * 2 * communication_range
        for j in range(number):
            id += 1
            y = communication_range + j * 2 * communication_range
            fog_node.append({"id": id, "x": x, "y": y})
    return fog_node


def get_vehicle_number_under_fog(fog_node, data_frame, communication_range):
    vehicle_number_under_fog = []
    for node in fog_node:
        vehicle_number = 0
        node_id = node["id"]
        node_x = node["x"]
        node_y = node["y"]
        x = data_frame["x"].tolist()
        y = data_frame["y"].tolist()
        for i in range(len(x)):
            if np.sqrt(np.square(x[i] - node_x) + np.square(y[i] - node_y)) <= communication_range:
                vehicle_number += 1
        vehicle_number_under_fog.append({"node_id": node_id, "vehicle_number": vehicle_number})
    return vehicle_number_under_fog


def get_tasks_in_time_slots(csv_file, time_slot, time_length, vehicle_task_number):
    df = pd.read_csv(csv_file)
    time = []
    fog_id = []
    v_number = []
    fog_node = get_fog_node(settings.zone_length, settings.communication_range)
    for i in range(1, time_length, time_slot):
        df_second = df[df['time'] == i]
        vehicle_number = get_vehicle_number_under_fog(fog_node,
                                     df_second,
                                     settings.communication_range)
        for number in vehicle_number:
            time.append(i)
            fog_id.append(number["node_id"])
            v_number.append(number["vehicle_number"])
    init_df = pd.DataFrame({"time": time, "fog_id": fog_id, "vehicle_number": v_number})
    init_df.to_csv(settings.init_csv_name, index=False)
    task_fog_id = []
    task_time = []
    required_rate = []
    required_sinr = []
    for j in range(1, len(fog_node) + 1):
        init_df_id = init_df[init_df["fog_id"] == j]
        time = init_df_id["time"].tolist()
        num = init_df_id["vehicle_number"].tolist()
        for k in range(len(time)):
            now_time = time[k]
            for l in range(num[k] * vehicle_task_number):
                task_required_rate = random.randint(settings.task_request_rate_min,
                                                    settings.task_request_rate_max)
                task_required_sinr = random.randint(settings.task_request_SINR_min,
                                                    settings.task_request_SINR_max)
                task_fog_id.append(j)
                task_time.append(now_time)
                required_rate.append(task_required_rate)
                required_sinr.append(task_required_sinr)
    task_df = pd.DataFrame({"fog_id": task_fog_id, "time": task_time, "required_rate": required_rate, "required_sinr": required_sinr})
    task_df.to_csv(settings.task_csv_name, index=False)


if __name__ == '__main__':
    # for node in get_fog_node(settings.zone_length, settings.communication_range):
    #     print(node)
    get_tasks_in_time_slots(settings.fill_xy_csv_name,
                            settings.time_slot,
                            settings.time_length,
                            settings.vehicle_task_number)
