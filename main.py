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

def Setup_Button_Listeners():
    btnList = document.querySelectorAll(".button")
    for i in range(len(btnList)):
        e = document.getElementById(btnList[i].id)
        btn_event = create_proxy(Process_Button)
        e.addEventListener("click", btn_event)

async def Process_Button(event):
    if document.getElementById("evtMsg").innerHTML == '100': 
        await plot_it()


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

    # Colores personalizados
    color_v = "#7e57c2"    # Morado oscuro
    color_m = "#d81b60"    # Rosado oscuro
    
    # ---------- GRÁFICO DE CORTE ----------
    fig_corte, ax1 = plt.subplots()
    ax1.plot(x, V, color=color_v, linewidth=2)
    ax1.fill_between(x, V, 0, color=color_v, alpha=0.3)
    ax1.set_xlabel("x")
    ax1.set_ylabel("V(x)")
    ax1.set_title("Esfuerzo de Corte")
    
    # Ejes tipo plano cartesiano
    ax1.spines['left'].set_position('zero')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['bottom'].set_linewidth(2)
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')
    ax1.tick_params(left=True, bottom=True)
    ax1.grid(True, linestyle='--', linewidth=0.5)
    
    # Flechas para ejes
    ax1.annotate("", xy=(x[-1], 0), xytext=(x[0], 0),
                 arrowprops=dict(arrowstyle="->", linewidth=1.5, color='black'))
    ax1.annotate("", xy=(0, max(V)*1.1 if max(V) > 0 else 1), xytext=(0, min(V)*1.1 if min(V) < 0 else -1),
                 arrowprops=dict(arrowstyle="->", linewidth=1.5, color='black'))
    
    # ---------- GRÁFICO DE MOMENTO ----------
    fig_momento, ax2 = plt.subplots()
    ax2.plot(x, M, color=color_m, linewidth=2)
    ax2.fill_between(x, M, 0, color=color_m, alpha=0.3)
    ax2.set_xlabel("x")
    ax2.set_ylabel("M(x)")
    ax2.set_title("Momento Flector")
    
    ax2.spines['left'].set_position('zero')
    ax2.spines['bottom'].set_position('zero')
    ax2.spines['left'].set_linewidth(2)
    ax2.spines['bottom'].set_linewidth(2)
    ax2.spines['right'].set_color('none')
    ax2.spines['top'].set_color('none')
    ax2.tick_params(left=True, bottom=True)
    ax2.grid(True, linestyle='--', linewidth=0.5)
    
    # Extender un poco los límites para asegurar espacio a la flecha
    ax2.set_xlim(x[0] - 0.5, x[-1] + 0.5)
    y_margin = max(abs(max(M)), abs(min(M))) * 1.2 or 1
    ax2.set_ylim(-y_margin, y_margin)
    
    # Flecha eje X
    ax2.annotate("", xy=(x[-1] + 0.4, 0), xytext=(x[0], 0),
                 arrowprops=dict(arrowstyle="->", linewidth=1.5, color='black'))
    
    # Flecha eje Y
    ax2.annotate("", xy=(0, y_margin - 0.1), xytext=(0, -y_margin + 0.1),
                 arrowprops=dict(arrowstyle="->", linewidth=1.5, color='black'))

    
    # Mostrar
    display(fig_corte, target="output", append=False)
    display(fig_momento, target="output", append=True)
    return None



Setup_Button_Listeners()


    
