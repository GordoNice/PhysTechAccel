#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Ivan Gordeev, 2021

# With the use of information from
# https://towardsdatascience.com/simple-physics-animations-using-vpython-1fce0284606

# Visualization for lecture 1 (Movement of particle in electromagnetic field)
# GlowScript 3.1 VPython

# import vpython as vp
from vpython import canvas, vector, rate, cos, sin, arrow, label,\
    color, cross, slider, button, sphere, wtext, pi, cylinder, pow, sqrt

# Create scene
scene = canvas(
    width=800, height=400,
    caption="Movement of particle in electromagnetic field")


# Pipe
pipe = cylinder(
    pos=vector(0, 0, 0), axis=vector(200, 0, 0), opacity=0.1, radius=100)

dt = 0.001  # time step


# Create class for proton
class Particle:
    def __init__(self):  # v is a vector representing velocity

        # starting position vector of proton
        self.position = vector(pipe.pos.x + 10, pipe.pos.y, pipe.pos.z)
        self.moving = False  # state to close loops
        self.theta = 0  # 0 .. 180
        self.phi = 0  # 0 ... 360

        self.q = 0.5  # charge of particle in arbitrary units
        self.m = 1  # particle mass in arbitrary units
        self.v_mag = 10  # # velocity magnitude
        self.e_mag = 0  # strength of electric field
        self.b_mag = 0  # strength of magnetic field

        # Vectors
        self.v_vec = vector(
            self.v_mag*cos(self.theta),
            self.v_mag*sin(self.theta)*sin(self.phi),
            self.v_mag*sin(self.theta)*cos(self.phi))  # velocity
        self.b_vec = vector(-self.b_mag, 0, 0)  # magnetic field
        self.e_vec = vector(self.e_mag, 0, 0)  # electric field
        self.a = vector(0, 0, 0)  # acceleration from electromagnetic field

        self.body = sphere(
            pos=self.position, color=color.blue,
            radius=2, make_trail=True, trail_type="curve")

        # Draw vectors as arrows
        self.v_arrow = arrow(
            pos=self.body.pos, axis=self.v_vec,
            shaftwidth=0.4, color=color.yellow, opacity=0.6)
        self.b_arrow = arrow(
            pos=self.body.pos, axis=self.b_vec,
            shaftwidth=0.4, color=color.cyan, opacity=0.6)
        self.e_arrow = arrow(
            pos=self.body.pos, axis=self.q * self.e_vec,
            shaftwidth=0.4, color=color.orange, opacity=0.6)
        self.f_arrow = arrow(
            pos=self.body.pos, axis=cross(self.v_vec, self.b_vec),
            shaftwidth=0.4, color=color.white, opacity=0.6)

        self.v_arrow.label = label(
            pos=self.v_arrow.pos+self.v_arrow.axis,
            text='Velocity', xoffset=20,
            yoffset=50, space=5,
            height=16, border=4,
            font='sans', color=self.v_arrow.color)
        self.b_arrow.label = label(
            pos=self.b_arrow.pos+self.b_arrow.axis,
            text='Magnetic', xoffset=20,
            yoffset=50, space=5,
            height=16, border=4,
            font='sans', color=self.b_arrow.color)
        self.e_arrow.label = label(
            pos=self.e_arrow.pos+self.e_arrow.axis,
            text='Electric', xoffset=20,
            yoffset=50, space=5,
            height=16, border=4,
            font='sans', color=self.e_arrow.color)
        self.f_arrow.label = label(
            pos=self.f_arrow.pos+self.f_arrow.axis,
            text='EM force', xoffset=20,
            yoffset=50, space=5,
            height=16, border=4,
            font='sans', color=self.f_arrow.color)

    def move(self):  # moves proton by small step dx
        # electric + magnetic field forces F = ma = q (E + v x B)
        self.a = self.q * (self.e_vec + cross(self.v_vec, self.b_vec))
        self.a /= self.m

        self.v_vec += self.a * dt  # a = dv/dt
        self.v_arrow.axis = self.v_vec  # a = dv/dt

        self.f_arrow.axis = self.a

        # Move body of particle and vectors by dx: v = dx/dt
        self.body.pos += self.v_vec * dt
        for vec in [self.v_arrow, self.b_arrow, self.e_arrow, self.f_arrow]:
            vec.pos = self.body.pos
            vec.label.pos = vec.pos + vec.axis

        # for vec in []

    def reset(self):  # resets particle position and path
        self.body.pos = self.position
        self.v_vec = vector(
            self.v_mag*cos(self.theta),
            self.v_mag*sin(self.theta)*sin(self.phi),
            self.v_mag*sin(self.theta)*cos(self.phi))
        self.body.clear_trail()
        self.a = vector(0, 0, 0)

        for vec in [self.v_arrow, self.b_arrow, self.e_arrow, self.f_arrow]:
            vec.pos = self.body.pos
            vec.label.pos = vec.pos + vec.axis

        self.v_arrow.axis = self.v_vec
        self.b_arrow.axis = self.b_vec

    def check_collision(self):  # checks for boundaries
        if sqrt(
                pow(self.body.pos.z, 2) + pow(self.body.pos.y, 2)) < pipe.radius \
                and pipe.length > self.body.pos.x > 0:
            return True
        else:
            return False


def to_start():
    particle.moving = False
    particle.reset()


def launch():
    particle.moving = True
    while particle.check_collision() and particle.moving:
        rate(1/dt)  # basically a delay function
        particle.move()


def stop():
    particle.moving = False


def showVectors():
    for vec in [
            particle.v_arrow,
            particle.b_arrow, particle.e_arrow, particle.f_arrow]:
        if vec.opacity != 0:
            vec.opacity = 0
        else:
            vec.opacity = 0.7


def showLabels():
    for vec in [
            particle.v_arrow,
            particle.b_arrow, particle.e_arrow, particle.f_arrow]:
        if vec.label.visible:
            vec.label.visible = False
        else:
            vec.label.visible = True


def adjustBfield():
    particle.b_mag = BfieldSlider.value
    particle.b_vec = vector(-BfieldSlider.value, 0, 0)  # B directed downwards
    particle.b_arrow.axis = particle.b_vec
    particle.b_arrow.label.pos = particle.b_arrow.pos + particle.b_arrow.axis
    BfieldSliderReadout.text = f"{BfieldSlider.value} Tesla"

    particle.a = particle.q * (
            particle.e_vec + cross(particle.v_vec, particle.b_vec))
    particle.a /= particle.m
    particle.f_arrow.axis = particle.a
    particle.f_arrow.label.pos = particle.f_arrow.pos + particle.f_arrow.axis


def adjustEfield():
    particle.e_mag = EfieldSlider.value
    particle.e_vec = vector(EfieldSlider.value, 0, 0)
    particle.e_arrow.axis = particle.q * particle.e_vec
    particle.e_arrow.label.pos = particle.e_arrow.pos + particle.e_arrow.axis
    EfieldSliderReadout.text = f"{EfieldSlider.value} V"

    particle.a = \
        particle.e_arrow.axis + particle.q * cross(
            particle.v_vec, particle.b_vec)
    particle.a /= particle.m
    particle.f_arrow.axis = particle.a
    particle.f_arrow.label.pos = particle.f_arrow.pos + particle.f_arrow.axis


def adjustQ():
    particle.q = QSlider.value
    particle.e_arrow.axis = particle.q * particle.e_vec
    particle.e_arrow.label.pos = particle.e_arrow.pos + particle.e_arrow.axis
    QSliderReadout.text = f"{QSlider.value} Coulumbs"

    particle.a = particle.q * (
            particle.e_vec + cross(particle.v_vec, particle.b_vec))
    particle.a /= particle.m
    particle.f_arrow.axis = particle.a
    particle.f_arrow.label.pos = particle.f_arrow.pos + particle.f_arrow.axis


def adjustM():
    particle.m = MSlider.value
    MSliderReadout.text = f"{MSlider.value} units"
    particle.body.radius = 2 * particle.m

    particle.a = particle.q * (
            particle.e_vec + cross(particle.v_vec, particle.b_vec))
    particle.a /= particle.m
    particle.f_arrow.axis = particle.a
    particle.f_arrow.label.pos = particle.f_arrow.pos + particle.f_arrow.axis


def adjustPhi():
    particle.phi = phiSlider.value * pi / 180  # degree - radian conversion
    particle.v_vec = vector(
        particle.v_mag * cos(particle.theta),
        particle.v_mag * sin(particle.theta) * sin(particle.phi),
        particle.v_mag * sin(particle.theta) * cos(particle.phi))
    particle.v_arrow.axis = particle.v_vec
    particle.v_arrow.label.pos = particle.v_arrow.pos + particle.v_arrow.axis
    phiSliderReadout.text = f"{phiSlider.value} degrees"

    particle.a = particle.q * (
            particle.e_vec + cross(particle.v_vec, particle.b_vec))
    particle.a /= particle.m
    particle.f_arrow.axis = particle.a
    particle.f_arrow.label.pos = particle.f_arrow.pos + particle.f_arrow.axis


def adjustTheta():
    theta = thetaSlider.value * pi / 180  # degree - radian conversion
    particle.theta = theta
    particle.v_vec = vector(
        particle.v_mag * cos(particle.theta),
        particle.v_mag * sin(particle.theta) * sin(particle.phi),
        particle.v_mag * sin(particle.theta) * cos(particle.phi))
    particle.v_arrow.axis = particle.v_vec
    particle.v_arrow.label.pos = particle.v_arrow.pos + particle.v_arrow.axis
    thetaSliderReadout.text = f"{thetaSlider.value} degrees"

    particle.a = particle.q * (
            particle.e_vec + cross(particle.v_vec, particle.b_vec))
    particle.a /= particle.m
    particle.f_arrow.axis = particle.a
    particle.f_arrow.label.pos = particle.f_arrow.pos + particle.f_arrow.axis


particle = Particle()  # creates the 'particle' object

# Adjust initial camera
scene.camera.pos = vector(7.6, 0.5, 67)
scene.camera.axis = vector(0, 0, -67)
scene.camera.follow(particle.body)

scene.append_to_caption("\n\n")  # newlines for aesthetics
button(text="To start", bind=to_start)  # link the button and function
button(text="Launch!", bind=launch)  # link the button and function
button(text="Stop!", bind=stop)  # link the button and function
button(text="Show Vectors", bind=showVectors)  # link the button and function
button(text="Show Labels", bind=showLabels)  # link the button and function

scene.append_to_caption("\n\n")  # newlines for aesthetics
BfieldSlider = slider(
    min=0, max=20, step=0.5, value=0, bind=adjustBfield)
scene.append_to_caption(" B-field (magnetic) Strength = ")
BfieldSliderReadout = wtext(text=f"{BfieldSlider.value} Tesla")

scene.append_to_caption("\n\n")  # newlines for aesthetics
EfieldSlider = slider(
    min=-50, max=50, step=1, value=0, bind=adjustEfield)
scene.append_to_caption(" E-field (electric) Strength = ")
EfieldSliderReadout = wtext(text=f"{EfieldSlider.value} V")

# Adjust charge Q
scene.append_to_caption("\n\n")
QSlider = slider(
    min=0, max=1, step=0.1, value=0.5, bind=adjustQ)
scene.append_to_caption(" Q (charge) = ")
QSliderReadout = wtext(text=f"{QSlider.value} Coulumbs")

# Adjust mass M
scene.append_to_caption("\n\n")
MSlider = slider(
    min=0.1, max=1, step=0.1, value=1, bind=adjustM)
scene.append_to_caption(" M (mass) = ")
MSliderReadout = wtext(text=f"{MSlider.value} units")

# Adjust angle theta
scene.append_to_caption("\n\n")
thetaSlider = slider(
    min=0, max=180, step=30, value=0, bind=adjustTheta)
scene.append_to_caption(" Theta angle = ")
thetaSliderReadout = wtext(text=f"{thetaSlider.value} degrees")

# Adjust angle phi
scene.append_to_caption("\n\n")
phiSlider = slider(
    min=0, max=360, step=30, value=0, bind=adjustPhi)
scene.append_to_caption(" Phi angle = ")
phiSliderReadout = wtext(text=f"{phiSlider.value} degrees")
