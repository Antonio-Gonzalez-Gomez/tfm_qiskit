#IMPLEMENTACIÓN DE LA SUBRUTINA CUÁNTICA DEL ALGORITMO DE SHOR
#DE BÚSQUEDA DE ORDEN PARA A = 7, N = 15

#Importaciones
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2 as Sampler

#Puerta que calcula 7 * k modulo 15
def ak_mod_N(exp):
    #Se crea un circuito para albergar la puerta
    uGate = QuantumCircuit(4, name='Ua^' + str(exp))
    #Se repite varias veces en función del exponente
    for _ in range(exp):
        #Desplazamiento de qubits
        uGate.swap(1, 0)
        uGate.swap(2, 1)
        uGate.swap(3, 2)
        #Inversión
        uGate.x(range(4))
        if (exp == 1):
            uGate.draw(output="mpl", style="iqp")
    #Se devuelve el circuito como puerta
    return uGate.to_gate()

#Circuito con 3 qubits en el registro de arriba, 4 qubits en el de abajo
qc = QuantumCircuit(7, 3)
#Se invierte el último qubit para obtener 0001
qc.x(6)
#Se prepara la superposición con puertas Hadamard
qc.h(range(3))
#Se crea una puerta para cada qubit del primer registro
for i in range(3):
    repeticiones = 2**i
    #Se añade la puerta U_a^k con un qubit de control
    uGate = ak_mod_N(repeticiones).control(1)
    qc.append(uGate, [i,3,4,5,6])
#Se añade la transformada inversa de Fourier
iqft = QFT(3, inverse=True)
qc.compose(iqft, inplace=True)
#Se mide el primer registro
qc.measure(range(3), range(3))
qc.draw(output="mpl", style="iqp")

#Se instancia un simulador
aersim = AerSimulator()
trans_qc = transpile(qc, aersim)
sampler = Sampler(backend=aersim)
#Se ejecuta 5000 veces el algoritmo para obtener todos los resultados
sampler.options.default_shots = 5000
#Histograma con los resultados (000, 010, 100, 110)
distribucion = sampler.run([trans_qc]).result()._pub_results[0].data.c.get_counts()
plot_histogram(distribucion)
plt.show()