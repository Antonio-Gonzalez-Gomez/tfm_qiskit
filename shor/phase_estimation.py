#IMPLEMENTACIÓN DEL ALGORITMO DE ESTIMACIÓN DE FASE CUÁNTICA

#Importaciones
from math import pi
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit_ibm_runtime import SamplerV2 as Sampler

#PARÁMETROS DE ENTRADA
num_qubits = 3      #Número de qubits
theta = pi * 5/4    #Fase esperada (autovalor)
######################

#El último qubit no se mide, por lo que se especifica el número de bits clásicos
qc = QuantumCircuit(num_qubits + 1, num_qubits)
#Se inicializa el último qubit a 1 (autovector de la puerta P)
qc.x(num_qubits)
#Se prepara la superposición con puertas Hadamard
qc.h(range(num_qubits))
for i in range(num_qubits):
    exp = 2 ** i #U, U^2, U^4, etc
    #Se instancia un circuito para albergar la puerta CP
    cp = QuantumCircuit(num_qubits + 1, name="CP")
    cp.cp(theta, i, num_qubits)
    #Se repite el circuito las veces necesarias
    qc.compose(cp.power(exp), inplace=True)
#Se añade la transformada inversa de Fourier
qc.compose(QFT(num_qubits, inverse=True), inplace=True)
qc.measure(range(num_qubits), range(num_qubits))
#Los circuitos se nombraron para poder descomponerlos en puertas CP
qc.decompose(gates_to_decompose=["CP"]).draw(output="mpl", style="iqp")

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