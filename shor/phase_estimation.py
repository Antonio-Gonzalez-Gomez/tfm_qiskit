#IMPLEMENTACIÓN DEL ALGORITMO DE ESTIMACIÓN DE FASE CUÁNTICA

#Importaciones
from math import pi
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit_ibm_runtime import SamplerV2 as Sampler

num_qubits = 3
#Fase esperada (autovalor)
theta = pi * 5/4

#El último qubit no se mide, por lo que se especifica el número de bits clásicos
qc = QuantumCircuit(num_qubits + 1, num_qubits)
#Se inicializa el último qubit a 1 (autovector de la puerta P)
qc.x(num_qubits)
#Se prepara la superposición con puertas Hadamard
qc.h(range(num_qubits))
for i in range(num_qubits):
    repeticiones = 2 ** i #U, U^2, U^4, etc
    #Se repite la puerta CP las veces necesarias
    for r in range(repeticiones):
        qc.cp(theta, i, num_qubits)
#Se añade la transformada inversa de Fourier
qc.compose(QFT(num_qubits, inverse=True), inplace=True)
qc.measure(range(num_qubits), range(num_qubits))
qc.draw(output="mpl", style="iqp")

#Se instancia un simulador
aersim = AerSimulator()
trans_qc = transpile(qc, aersim)
sampler = Sampler(backend=aersim)
#Solo es necesario ejecutar el circuito una vez
sampler.options.default_shots = 1
result = list(sampler.run([trans_qc]).result()._pub_results[0].data.c.get_counts())[0]
#Resultado esperado: 101 -> pi * 5/4
print("RESULTADO:", result)
plt.show()