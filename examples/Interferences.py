#!/usr/bin/python3
# encoding: utf-8

# Berreman4x4 example
# Author: O. Castany

# The simplest example: a homogeneous glass layer in air

import numpy, Berreman4x4
from Berreman4x4 import c, pi
import matplotlib.pyplot as pyplot

print("\n*** Air / glass / air ***\n")

# Materials:
air = Berreman4x4.IsotropicNonDispersiveMaterial(1.0)
glass = Berreman4x4.IsotropicNonDispersiveMaterial(1.5)

# Layer and half-spaces:
layer = Berreman4x4.HomogeneousIsotropicLayer(glass)
front = back = Berreman4x4.IsotropicHalfSpace(air)

# Structure:
s = Berreman4x4.Structure(front, [layer], back)

# Wavelength and wavenumber:
lbda = 1e-6
k0 = 2*pi/lbda

# Incidence angle (Kx = n sin(Φ):
Kx = 0.5
angle = front.get_Phi_from_Kx(Kx) * 180/pi

# Variation of the reflexion and transmission coefficients with the
# thickness of the glass layer:
h_list = numpy.linspace(0, 1.0e-6)
data = Berreman4x4.DataList()
for h in h_list:
    layer.setThickness(h)
    data.append(s.evaluate(Kx,k0))

# Extract the power coefficients
coeff_names = ("T_pp","T_ss","R_ss","R_pp")
values = [data.get(name) for name in coeff_names]

# Prepare plot...
d = numpy.vstack(values).T
fig = pyplot.figure()
ax = fig.add_subplot(
        title="Glass layer at {:.1f}° incidence angle".format(angle),
        xlabel=r"Glass layer thickness, $h$ (m)",
        ylabel=r"Reflexion and transmission coefficients $R$, $T$")

lines = ax.plot(h_list, d)
ax.legend(lines, coeff_names)
fmt = ax.xaxis.get_major_formatter()
fmt.set_powerlimits((-3,3))
pyplot.show()

