#IMPLEMENTACIÓN DE LA TRANSFORMADA CUÁNTICA DE FOURIER

#Importaciones
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_bloch_multivector

#Numero a codificar
input = "101"
num_qubits = len(input)

#Creación del circuito
qc = QuantumCircuit(num_qubits)
#Se prepara el estado inicial invirtiendo los qubits que tengan que estar a 1
uno_inds = [ind for ind in range(num_qubits) if input.startswith("1", ind)]
if (uno_inds):
    qc.x(uno_inds)
#Se añade el operador de Fourier
qc.compose(QFT(num_qubits, do_swaps=False), inplace=True)
qc.decompose(gates_to_decompose=["QFT"]).draw(output="mpl", style="iqp")

#Se instancia un simulador
aersim = AerSimulator()
trans_qc = transpile(qc, aersim)
#Se guarda la salida sin medirla para apreciar la fase
trans_qc.save_statevector()
statevector = aersim.run(trans_qc).result().get_statevector()
#Las fases de los qubits son: PI, PI/2, 5PI/4
plot_bloch_multivector(statevector, title="Resultado QFT(" + str(input) + ")")
plt.show()

