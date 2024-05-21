#IMPLEMENTACIÓN DEL ALGORITMO DE GROVER

#Importaciones
import math
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import SamplerV2 as Sampler

#PARÁMETROS DE ENTRADA
omega = "010"       #Estado solución, bitstring de longitud cualquiera
iteraciones = -1    #Numero de iteraciones, dejar a -1 para usar el valor óptimo
######################

num_qubits = len(omega)
if (iteraciones == -1):
    #Valor óptimo del número de iteraciones
    iteraciones = math.floor(math.pi * math.sqrt(2**num_qubits)/ 4)

#Definición de la función oráculo
def oraculo(omega):
    qc = QuantumCircuit(num_qubits)
    #Se invierten los bits de entrada porque la ordenación de Qiskit va al revés
    rev_omega = omega[::-1]
    #Se añaden puertas Pauli-X a los bits que estén a 0
    zero_inds = [ind for ind in range(num_qubits) if rev_omega.startswith("0", ind)]
    if (zero_inds):
        qc.x(zero_inds)
    #Puerta CZ con n-1 qubits de control y 1 qubit objetivo
    qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
    #Se vuelven a usar puertas Pauli-X para volver al estado original
    if (zero_inds):
        qc.x(zero_inds)
    return qc

#Inicialización de la función oráculo
oraculo = oraculo(omega)
oraculo.draw(output="mpl", style="iqp")

#Inicialización del operador de Grover (oráculo y difusión)
grover = GroverOperator(oraculo)
#Se descompone el operador para poder representarlo
grover.decompose().draw(output="mpl", style="iqp")
qc = QuantumCircuit(num_qubits)
#Puertas hadamard previas al oráculo para definir la superposición s
qc.h(range(num_qubits))
#Se itera sobre el operador de Grover las veces necesarias
qc.compose(grover.power(iteraciones), inplace=True)
#Se añade la operación de medida en todos los qubits
qc.measure_all()

#Se instancia un simulador
aersim = AerSimulator()
trans_qc = transpile(qc, aersim)
#Se ejecuta 5000 veces el algoritmo ya que puede fallar
sampler = Sampler(backend=aersim)
sampler.options.default_shots = 5000
result = sampler.run([trans_qc]).result()
distribucion = result[0].data.meas.get_counts()
#Histograma con los resultados (la mayoría de ejecuciones devolverá omega)
plot_histogram(distribucion)
print("RESULTADOS PARA", str(iteraciones), "ITERACIONES:", distribucion)
plt.show()