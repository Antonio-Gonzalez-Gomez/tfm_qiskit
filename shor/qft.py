#IMPLEMENTACIÓN DE LA TRANSFORMADA CUÁNTICA DE FOURIER

#Importaciones
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_bloch_multivector


#PARÁMETROS DE ENTRADA
input = "11111"     #Número a codificar
######################

num_qubits = len(input)

#Creación del circuito
qc = QuantumCircuit(num_qubits)
#Se prepara el estado inicial invirtiendo los qubits que tengan que estar a 1
uno_inds = [ind for ind in range(num_qubits) if input.startswith("1", ind)]
if (uno_inds):
    qc.x(uno_inds)
#Se añade el operador de Fourier
qc.compose(QFT(num_qubits, do_swaps=False), inplace=True)
#Al dibujar el circuito, se descompone la función QFT para que sea visible sus componentes
qc.decompose(gates_to_decompose=["QFT"]).draw(output="mpl", style="iqp")

#Se instancia un simulador
aersim = AerSimulator()
#Se transforman las puertas en otras equivalentes que el simulador reconozca
trans_qc = transpile(qc, aersim)
#Se guarda la salida sin medirla para apreciar la fase
trans_qc.save_statevector()
#Se guarda la salida sin medirla para apreciar la fase (estado del vector)
statevector = aersim.run(trans_qc).result().get_statevector()
#Comando para representar los estados de los qubits
#Las fases de los qubits son: PI, PI/2, 5PI/4
plot_bloch_multivector(statevector)
plt.show()

