import matplotlib.pyplot as plt
import numpy as np
from pyscript import display
from js import document
from pyodide.ffi import create_proxy

largo_element = document.getElementById("largo")
a1pos_element = document.getElementById("a1pos")
a1res_element = document.getElementById("a1res")
a2pos_element = document.getElementById("a2pos")
a2res_element = document.getElementById("a2res")
c1tipo_element = document.getElementById("c1tipo")
c1muli_element = document.getElementById("c1muli")
c1ini_element = document.getElementById("c1ini")
c1fin_element = document.getElementById("c1fin")
c2tipo_element = document.getElementById("c2tipo")
c2muli_element = document.getElementById("c2muli")
c2ini_element = document.getElementById("c2ini")
c2fin_element = document.getElementById("c2fin")
c3tipo_element = document.getElementById("c3tipo")
c3muli_element = document.getElementById("c3muli")
c3ini_element = document.getElementById("c3ini")
c3fin_element = document.getElementById("c3fin")

output = document.getElementById("output")

async def plot_it_wrapper():
    fig = await plot_it()
    display(fig, target="output", append=False)

class Singularity:
    def __init__(self,w0, a, order, coeff = 1):
        self.w0 = w0
        self.a = a
        self.order = order
        self.coeff = coeff
    def __call__(self, x):
        if self.order >= 0:
            return self.w0*(x-self.a)**self.order*(x>self.a)*self.coeff 
        else:
            return np.zeros_like(x)
    def integrate(self):
        if self.order < 0:
            return Singularity(self.w0, self.a, self.order + 1)
        else:
            return Singularity(self.w0, self.a, self.order + 1, coeff = 1.0/(self.order + 1))

async def plot_it(*args, **kwargs):
    L = float(largo_element.value)
    a11 = int(a1res_element.value)
    a12 = float(a1pos_element.value)
    a21 = int(a2res_element.value)
    a22 = float(a2pos_element.value)
    c11 = float(c1muli_element.value)
    c12 = float(c1ini_element.value)
    c13 = int(c1tipo_element.value)
    c23 = int(c2tipo_element.value)
    c33 = int(c3tipo_element.value)
    A1 = [a11,a12]
    A2 = [a21,a22]
    print("Se ejecutó plot_it()") 
    x = np.linspace(0,L, 1000)
    qs = []
    if c13 == 0:
        c14 = float(c1fin_element.value)
        qs.append([c11,c12,c13])
        qs.append([-c11,c14,c13])
    else:
        qs.append([c11,c12,c13])

    if c23 == 0:
        c21 = float(c2muli_element.value)
        c22 = float(c2ini_element.value)
        c24 = float(c2fin_element.value)
        qs.append([c21,c22,c23])
        qs.append([-c21,c24,c23])
    elif c23 != 1:
        c21 = float(c2muli_element.value)
        c22 = float(c2ini_element.value)
        qs.append([c21,c22,c23])
            
    if c33 == 0:
        c31 = float(c3muli_element.value)
        c32 = float(c3ini_element.value)
        c34 = float(c3fin_element.value)
        qs.append([c31,c32,c33])
        qs.append([-c31,c34,c33])
    elif c33 != 1:
        c31 = float(c3muli_element.value)
        c32 = float(c3ini_element.value)
        qs.append([c31,c32,c33])
        
    Qs = [Singularity(q[0],q[1],q[2]) for q in qs]

    A=np.zeros((2,2))
    A[0,0 if A1[0]==1 else 1] = 1
    A[1,0] = A1[1] if A1[0]==1 else 1
    A[0,1 if A2[0]==1 else 1] = 1
    A[1,1] = A2[1] if A2[0]==1 else 1

    w = sum(q.integrate()(L) - q.integrate()(0) for q in Qs)
    wx = sum(np.trapz(x*q(x),x) if q.order >= 0 else (-q.w0 if q.order==-2 else q.a*q.w0) for q in Qs)
    f = np.array([w, wx])
    R=np.linalg.solve(A,f)

    Qs += [
        Singularity(-R[0], A1[1], -A1[0]),
        Singularity(-R[1], A2[1], -A2[0])
    ]

    V = sum(q.integrate()(x) for q in Qs)
    M = -sum(q.integrate().integrate()(x) for q in Qs)

    fig, axs = plt.subplots(3, 1, figsize=(8, 6), height_ratios=[1, 2, 2])

    # === Visualización de cargas en axs[0] ===
    ax_cargas = axs[0]
    ax_cargas.set_xlim(0, L)
    ax_cargas.set_ylim(-2, 2)
    ax_cargas.axis("off")
    ax_cargas.hlines(0, 0, L, linewidth=10, color="gray")

    if A1[0] == 1:
        ax_cargas.arrow(A1[1], 0, 0, 0.8, head_width=0.2, head_length=0.3, fc="blue", ec="blue")
    if A2[0] == 1:
        ax_cargas.arrow(A2[1], 0, 0, 0.8, head_width=0.2, head_length=0.3, fc="blue", ec="blue")

    for q in qs:
        w0, a, orden = q
        if orden == -1:
            ax_cargas.arrow(a, 1.5, 0, -1.5, head_width=0.2, head_length=0.3, fc="red", ec="red")
        elif orden == 0:
            idx = qs.index(q)
            if idx + 1 < len(qs) and qs[idx + 1][0] == -w0 and qs[idx + 1][2] == 0:
                a_fin = qs[idx + 1][1]
                n = 8
                for xi in np.linspace(a, a_fin, n):
                    ax_cargas.arrow(xi, 1.5, 0, -1.5, head_width=0.15, head_length=0.2, fc="crimson", ec="crimson")
        elif orden == -2:
            ax_cargas.plot(a, 0.7, marker="o", markersize=12, color="orange")
            ax_cargas.plot(a, 0.7, marker=".", markersize=4, color="black")

    axs[1].plot(x, V, linestyle='-', color='g', label='Corte')
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("Corte")
    axs[1].grid()

    axs[2].plot(x, M, linestyle='-', color='r', label='Momento')
    axs[2].set_ylabel("Momento")
    axs[2].set_xlabel("x")
    axs[2].grid()

    plt.tight_layout()
    return fig
async def plot_it_wrapper():
    fig = await plot_it()
    display(fig, target="output", append=False)

from js import console
from pyodide.ffi import create_proxy
import asyncio

# Exponer función a PyScript
import pyodide
pyodide.code.run_globals["plot_it_wrapper"] = plot_it_wrapper
import pyodide
pyodide.code.run_globals["plot_it_wrapper"] = plot_it_wrapper



    
