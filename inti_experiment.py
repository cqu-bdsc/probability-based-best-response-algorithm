#!./venv python
# -*- encoding: utf-8 -*-
"""
@File    :   inti_experiment.py    
@Contact :   neard.ws@gmail.com
@Github  :   neardws

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/7/29 下午4:04   neardws      1.0         None
"""

from config import settings
import math
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plot


def get_fog_node(zone_length, communication_range):
    """

    Args:
        zone_length:
        communication_range:

    Returns:

    """
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
    """

    Args:
        fog_node:
        data_frame:
        communication_range:

    Returns:

    """
    vehicle_number_under_fog = []
    for node in fog_node:
        vehicle_number = 0
        node_id = node["id"]
        node_x = node["x"]
        node_y = node["y"]
        x = data_frame["x"].tolist()
        y = data_frame["y"].tolist()
        vehicle_under_fog = []
        for i in range(len(x)):
            if np.sqrt(np.square(x[i] - node_x) + np.square(y[i] - node_y)) <= communication_range:
                vehicle_number += 1
                vehicle_under_fog.append({"x": x[i], "y": y[i]})
        vehicle_number_under_fog.append({"node_id": node_id,
                                         "vehicle_number": vehicle_number,
                                         "vehicle_under_fog": vehicle_under_fog})
    return vehicle_number_under_fog


def get_tasks_in_time_slots(fog_node, csv_file, time_slot, time_length, vehicle_task_number):
    """

    Args:
        fog_node:
        csv_file:
        time_slot:
        time_length:
        vehicle_task_number:
    """
    df = pd.read_csv(csv_file)
    time = []
    fog_id = []
    v_number = []
    vehicles_under_fog = []
    for i in range(1, time_length, time_slot):
        df_second = df[df['time'] == i]
        vehicle_number = get_vehicle_number_under_fog(fog_node,
                                                      df_second,
                                                      settings.communication_range)
        for number in vehicle_number:
            time.append(i)
            fog_id.append(number["node_id"])
            v_number.append(number["vehicle_number"])
            vehicles_under_fog.append(number["vehicle_under_fog"])
    init_df = pd.DataFrame({"time": time, "fog_id": fog_id, "vehicle_number": v_number, "vehicles": vehicles_under_fog})
    init_df.to_csv(settings.init_csv_name, index=False)
    task_fog_id = []
    task_time = []
    required_rate = []
    required_sinr = []
    task_x = []
    task_y = []
    for j in range(1, len(fog_node) + 1):
        init_df_id = init_df[init_df["fog_id"] == j]
        time = init_df_id["time"].tolist()
        num = init_df_id["vehicle_number"].tolist()
        vehicles = init_df_id["vehicles"]
        for k in range(len(time)):
            now_time = time[k]
            now_vehicles = vehicles.tolist()[k]
            for l in range(num[k]):
                for n in range(vehicle_task_number):
                    task_required_rate = random.randint(settings.task_request_rate_min,
                                                        settings.task_request_rate_max)
                    task_required_sinr = random.randint(settings.task_request_SINR_min,
                                                        settings.task_request_SINR_max)
                    task_fog_id.append(j)
                    task_time.append(now_time)
                    required_rate.append(task_required_rate)
                    required_sinr.append(task_required_sinr)
                    vehicle = now_vehicles[l]
                    task_x.append(vehicle["x"])
                    task_y.append(vehicle["y"])
    task_df = pd.DataFrame(
        {"fog_id": task_fog_id, "time": task_time, "required_rate": required_rate, "required_sinr": required_sinr, "x": task_x, "y": task_y})
    task_df.to_csv(settings.task_csv_name, index=False)


def draw_round(round_x, round_y, radius, width):
    theta = np.arange(0, 2 * np.pi, 0.01)
    x = round_x + radius * np.cos(theta)
    y = round_y + radius * np.sin(theta)
    plot.plot(x, y, color="gray", linestyle="--", linewidth=width)


def draw_fog_task_in_the_map(fog_node, time, zone_length, communication_range):
    plot.xlim(0, zone_length)
    plot.ylim(0, zone_length)
    for node in fog_node:
        node_x = node["x"]
        node_y = node["y"]
        plot.plot(int(node_x), int(node_y), color="black", marker="^", markersize=10, label="fog node")
        draw_round(node_x, node_y, communication_range, 1)
    df = pd.read_csv(settings.task_csv_name)
    df = df[df["time"] == time]
    task_x = df["x"].tolist()
    task_y = df["y"].tolist()
    for i in range(len(task_x)):
        plot.plot(int(task_x[i]), int(task_y[i]), color="darkred", marker="o", label="task", markersize=3)
    plot.show()


if __name__ == '__main__':
    fog_node = get_fog_node(settings.zone_length, settings.communication_range)
    # #     print(node)
    # get_tasks_in_time_slots(fog_node,
    #                         settings.fill_xy_csv_name,
    #                         settings.time_slot,
    #                         settings.time_length,
    #                         settings.vehicle_task_number)

    draw_fog_task_in_the_map(fog_node=fog_node, time=1, zone_length=settings.zone_length, communication_range=settings.communication_range)
