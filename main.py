import matplotlib.pyplot as plt
import numpy as np
import asyncio
from pyodide import create_proxy

## INPUTS HTML ##
largo_element = Element("largo")
a1pos_element = Element("a1pos")
a1res_element = Element("a1res") 
a2pos_element = Element("a2pos")
a2res_element = Element("a2res")
c1tipo_element = Element("c1tipo")
c1muli_element = Element("c1muli")
c1ini_element = Element("c1ini")
c1fin_element = Element("c1fin")
c2tipo_element = Element("c2tipo")
c2muli_element = Element("c2muli")
c2ini_element = Element("c2ini")
c2fin_element = Element("c2fin")
c3tipo_element = Element("c3tipo")
c3muli_element = Element("c3muli")
c3ini_element = Element("c3ini")
c3fin_element = Element("c3fin")
output = Element("output")
  
## BOTÓN ##
def Setup_Button_Listeners():
    btnList = document.querySelectorAll(".button")
    for i in range(len(btnList)):
        e = document.getElementById(btnList[i].id)
        btn_event = create_proxy(Process_Button)
        e.addEventListener("click", btn_event)
#
#        
async def Process_Button(event):
    if document.getElementById("evtMsg").innerHTML == '100':        #   button plot_it
        fig = await plot_it()
        output.write(fig)

## CLASES ##
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
            return np.zeros_like(x) # functions of negative order can only be integrated
    def integrate(self):
        if self.order < 0:
            return Singularity(self.w0, self.a, self.order + 1)
        else:
            return Singularity(self.w0, self.a, self.order + 1, coeff = 1.0/(self.order + 1))

## FUNCIÓN ##
async def plot_it(*args, **kwargs):

    L = int(largo_element.value)
    a11 = int(a1res_element.value)
    a12 = int(a1pos_element.value)
    a21 = int(a2res_element.value)
    a22 = int(a2pos_element.value)
    c11 = int(c1muli_element.value)
    c12 = int(c1ini_element.value)
    c13 = int(c1tipo_element.value)
    c23 = int(c2tipo_element.value)
    c33 = int(c3tipo_element.value)
    A1 = [a11,a12]
    A2 = [a21,a22]
        
    x = np.linspace(0,L, 1000)
    qs = []
    if c13 == 0:
      c14 = int(c1fin_element.value)
      qs.append([c11,c12,c13])
      qs.append([-c11,c14,c13])
    else:
      qs.append([c11,c12,c13])

    if c23 == 0:
      c21 = int(c2muli_element.value)
      c22 = int(c2ini_element.value)
      c24 = int(c1fin_element.value)
      qs.append([c21,c22,c23])
      qs.append([-c21,c24,c23])

    elif c23 == 1:
      pass

    else:
      c21 = int(c2muli_element.value)
      c22 = int(c2ini_element.value)
      qs.append([c21,c22,c23])

    if c33 == 0:
      c31 = int(c3muli_element.value)
      c32 = int(c3ini_element.value)
      c34 = int(c3fin_element.value)
      qs.append([c31,c32,c33])
      qs.append([-c31,c34,c33])

    elif c33 == 1:
      pass

    else:
      c31 = int(c3muli_element.value)
      c32 = int(c3ini_element.value)
      qs.append([c31,c32,c33])
      
        
    Qs = []

    for q in qs:
        Qs.append(Singularity(q[0],q[1],q[2]))

    A=np.zeros((2,2))
    
    if A1[0]==1:
        A[0,0]=1
        A[1,0]=A1[1]
    else:
        A[1,0]=1
    
    if A2[0]==1:
        A[0,1]=1
        A[1,1]=A2[1]
    else:
        A[1,1]=1

    w = 0
    wx = 0
    for qi in Qs:
        qi_int = qi.integrate()
        w += qi_int(L) - qi_int(0)
        wx += np.trapz(x*qi(x),x)
    f = np.array([w, wx])
    R=np.linalg.solve(A,f)

    qA1 = Singularity(-R[0], A1[1], -A1[0])
    qA2 = Singularity(R[1], A2[1], -A2[0])
    Qs.append(qA1)
    Qs.append(qA2)
    Vs = []
    Ms = []

    for qi in Qs:
        Vs.append(qi.integrate())
        Ms.append(Vs[-1].integrate())

    V = 0
    M = 0
    for vi in Vs:
        V += vi(x)
        
    for mi in Ms:
        M -= mi(x)


    fig, ax = plt.subplots()

    ax.plot(x, V, linestyle='-', color='g', label='Corte')
    ax.set_xlabel("x")
    ax.set_ylabel("Corte")

    ax2=ax.twinx()
    ax2.plot(x, M, linestyle='-', color='r', label='Momento')
    ax2.set_ylabel("momento")

    plt.title('Corte y Momento en vigas')
    plt.legend()
    fig
    return fig
    
Setup_Button_Listeners()