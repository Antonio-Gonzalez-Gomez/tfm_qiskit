#IMPLEMENTACIÓN DE LA SUBRUTINA CUÁNTICA DEL ALGORITMO DE SHOR
#DE BÚSQUEDA DE ORDEN PARA A = 7, N = 15

#Importaciones
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit_ibm_runtime import SamplerV2 as Sampler

#Puerta que calcula 7 * k modulo 15
def ak_mod_N(exp):
    uGate = QuantumCircuit(4, name='Ua^' + str(exp))
    #Se repite varias veces en función del exponente
    for _ in range(exp):
        #LEFT SHIFT X3
        uGate.swap(1, 0)
        uGate.swap(2, 1)
        uGate.swap(3, 2)
        #INVERTIR QUBITS
        uGate.x(range(4))
    return uGate.to_gate()

#3 qubits en el registro de arriba, 4 qubits en el de abajo
qc = QuantumCircuit(7, 3)
#Se invierte el último qubit para obtener 0001
qc.x(6)
#Se crea una puerta para cada qubit del primer registro
for i in range(3):
    repeticiones = 2**i
    #Se añade un qubit de control a la puerta
    uGate = ak_mod_N(repeticiones).control(1)
    #Los qubits de control van de abajo (2) a arriba (0)
    qc.append(uGate, [2 - i,3,4,5,6])
#Se añade la transformada inversa de Fourier
iqft = QFT(3, inverse=True)
qc.compose(iqft, inplace=True)
qc.measure(range(3), range(3))
qc.draw(output="mpl", style="iqp")

#Se instancia un simulador
aersim = AerSimulator()
trans_qc = transpile(qc, aersim)
sampler = Sampler(backend=aersim)
#Solo es necesario ejecutar el circuito una vez
sampler.options.default_shots = 1
result = list(sampler.run([trans_qc]).result()._pub_results[0].data.c.get_counts())[0]
print("RESULTADO:", result)
#Resultado esperado: 100 -> 4 => 7^4 = 1 mod 15
plt.show()