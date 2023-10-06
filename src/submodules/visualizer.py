import math
import os

import numpy as np

from submodules.data import DataHolder


def animate(
    dh: DataHolder,
    frames: int,
    alpha: float,
    L: float | None = None,
):
    # https://stackoverflow.com/questions/51464455/how-to-disable-welcome-message-when-importing-pygame/51470016#51470016
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

    import pygame as pg

    pg.init()
    pg.display.set_caption("Visualization")
    pg.display.set_mode((500, 500), pg.SCALED | pg.RESIZABLE)

    R_min = dh.data["R"].iloc[0]
    R_max = dh.data["R"].iloc[-1]

    if L:
        th_start = dh.data["th"].iloc[0]
        th_end = dh.data["th"].iloc[-1]
        costh_start = math.cos(th_start)
        costh_end = math.cos(th_end)
        sinth_start = math.sin(th_start)
        sinth_end = math.sin(th_end)

    running = True
    clock = pg.time.Clock()

    i = 0
    radius = 5
    end_size = np.array(((300 - 2 * radius), (300 - 2 * radius)))
    cosalpha = math.cos(alpha)
    sinalpha = math.sin(alpha)

    if L:  # flip alpha if it's the more complex model per definition.
        sinalpha = -sinalpha

    R0 = dh.data["R"].iloc[0]
    
    if not L:
        x_min = cosalpha * R_min
        y_min = sinalpha * R_min
        x_max = cosalpha * R_max
        y_max = sinalpha * R_max
    else:
        x_min = cosalpha * R_min + min(sinth_start * L,0)
        y_min = sinalpha * R_min + min(costh_start * L,0)
        x_max = cosalpha * R_max + max(sinth_end * L,0)
        y_max = sinalpha * R_max + max(costh_end * L,0)
    
    x_diff = x_max - x_min
    y_diff = y_max - y_min
    
    first_pos = (100, 100) + end_size * (
        (cosalpha * R0 - x_min) / x_diff,
        (sinalpha * R0 - x_min) / y_diff,
    )
    R1 = dh.data["R"].iloc[-1]
    last_pos = (100, 100) + end_size * (
        (cosalpha * R1 - x_min) / x_diff,
        (sinalpha * R1 - x_min) / y_diff,
    )

    surface = pg.display.get_surface()
    while running:
        clock.tick(frames)

        R = dh.get_val(i, "R")
        
        pos1 = (100, 100) + end_size * (
            (cosalpha * R - x_min) / x_diff,
            (sinalpha * R - y_min) / y_diff,
        )
        if L:
            theta = dh.get_val(i, "th")
            costheta = math.cos(theta)
            sintheta = math.sin(theta)
            pos2 = pos1 + end_size * (
                (sintheta * L-x_min) / x_diff,
                (costheta * L-y_min) / y_diff,
            )
        i += 1
        if i == dh.length:
            i = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        surface.fill((255, 255, 255))
        pg.draw.circle(surface, (0, 0, 0), pos1, radius)
        if L:
            pg.draw.circle(surface, (0, 0, 0), pos2, radius)
            pg.draw.line(surface, (0, 0, 0), pos1, pos2, width=2)
        pg.draw.line(surface, (0, 0, 0), first_pos + (0, radius), last_pos+(0, radius), width=2)
        pg.display.flip()
