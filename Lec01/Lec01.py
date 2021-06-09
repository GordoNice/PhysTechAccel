#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ivan Gordeev, 2021

# Based on
# https://towardsdatascience.com/simple-physics-animations-using-vpython-1fce0284606

# Visualization for lection 1 ()
# GlowScript 3.1 VPython

import vpython as vp

# Create scene
scene = vp.canvas(width=1400, height=600)

# Create box
xlen, ylen, zlen = 100, 100, 100
boundaries =\
    [
        vp.box(pos=vp.vector(0, -ylen/2, 0), size=vp.vector(xlen, 0.2, zlen)),
        vp.box(pos=vp.vector(0, ylen/2, 0), size=vp.vector(xlen, 0.2, zlen)),
        vp.box(pos=vp.vector(-xlen/2, 0, 0), size=vp.vector(0.2, ylen, zlen)),
        vp.box(pos=vp.vector(xlen/2, 0, 0), size=vp.vector(0.2, ylen, zlen)),
        vp.box(pos=vp.vector(0, 0, -zlen/2), size=vp.vector(xlen, ylen, 0.2))
    ]

dt = 0.00001  # time step

start_vec = vp.vector(0, -ylen/2+1, 0)  # starting position vector of proton


# Create class for proton
class Proton:
    def __init__(self, start):  # v is a vector representing velocity

        # velocity
        self.start_vec = start
        self.v_mag = 20
        self.q = 0.5  # charge of proton in arbitrary units
        self.b_mag = 5  # strength of magnetic field
        self.theta = vp.pi/4  # angle of launch of proton

        self.v_vec = vp.vector(
            self.v_mag*vp.cos(self.theta), self.v_mag*vp.sin(self.theta), 0)
        self.b_vec = vp.vector(0, -self.b_mag, 0)

        self.proton = vp.sphere(
            pos=start, color=vp.color.red,
            radius=1, make_trail=True, trail_type="curve")
        self.a = vp.vector(0, 0, 0)

    def move(self):  # moves proton by small step
        self.a = self.q * vp.cross(self.v_vec, self.b_vec)  # F = ma = q v x B
        self.v_vec += self.a * dt  # a = dv/dt
        self.proton.pos += self.v_vec * dt  # v = dx/dt

    def reset_proton(self):  # resets proton position and path
        self.proton.pos = self.start_vec
        self.v_vec = vp.vector(
            self.v_mag*vp.cos(self.theta), self.v_mag*vp.sin(self.theta), 0)
        self.proton.clear_trail()
        self.a = vp.vector(0, 0, 0)

    def check_collision(self):  # checks for boundaries
        if ylen / 2 > self.proton.pos.y > -ylen / 2 \
                and xlen / 2 > self.proton.pos.x > -xlen / 2 \
                and -zlen / 2 < self.proton.pos.z < zlen / 2:
            return True
        else:
            return False


def launch():
    proton.reset_proton()
    while proton.check_collision():
        vp.rate(1/dt)  # basically a delay function
        proton.move()


def adjustBfield():
    proton.b_mag = BfieldSlider.value
    proton.b_vec = vp.vector(0, -BfieldSlider.value, 0)  # B directed downwards
    BfieldSliderReadout.text = f"{BfieldSlider.value} Tesla"


def adjustQ():
    proton.q = QSlider.value
    QSliderReadout.text = f"{QSlider.value} Coulumbs"


def adjustAngle():
    theta = angleSlider.value * vp.pi/180  # degree - radian conversion
    proton.theta = theta
    proton.v_vec = vp.vector(
        proton.v_mag*vp.cos(theta), proton.v_mag * vp.sin(theta), 0)
    angleSliderReadout.text = f"{angleSlider.value} degrees"
    # proton.v = vp.vector(v_mag*vp.cos(theta), v_mag*vp.sin(theta), 0)


proton = Proton(start_vec)  # creates the 'proton' object

vp.button(text="Launch!", bind=launch)  # link the button and function

scene.append_to_caption("\n\n")  # newlines for aesthetics
BfieldSlider = vp.slider(
    min=0, max=10, step=.5, value=5, bind=adjustBfield)
scene.append_to_caption(" B-field Strength = ")
BfieldSliderReadout = vp.wtext(text="5 Tesla")

# Adjust charge Q
scene.append_to_caption("\n\n")
QSlider = vp.slider(
    min=0, max=1, step=0.1, value=0.5, bind=adjustQ)
scene.append_to_caption(" Q = ")
QSliderReadout = vp.wtext(text="0.5 Coulumbs")

# Adjust angle theta
scene.append_to_caption("\n\n")
angleSlider = vp.slider(
    min=0, max=90, step=1, value=45, bind=adjustAngle)
scene.append_to_caption(" Angle = ")
angleSliderReadout = vp.wtext(text="45 degrees")
