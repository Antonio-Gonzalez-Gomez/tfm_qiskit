#EJEMPLO DE USO DE QISKIT MEDIANTE CIRCUITO DE TRASLADO DE FASE

#Importaciones
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector

#Circuito cuántico con 2 qubits
qc = QuantumCircuit(2)
#Se aplica una puerta de Hadamard al primer qubit
qc.h(0)
#Se aplica una puerta de Pauli-X al segundo qubit
qc.x(1)
#Se aplica una puerta S sobre el segundo qubit usando el primero de control
qc.cs(0,1)
#Comando para dibujar el circuito
qc.draw(output="mpl", style="iqp")

#Se instancia un simulador
aersim = AerSimulator()
#Se transforman las puertas en otras equivalentes que el simulador reconozca
trans_qc = transpile(qc, aersim)
#Se guarda la salida sin medirla para apreciar la fase (estado del vector)
trans_qc.save_statevector()
statevector = aersim.run(trans_qc).result().get_statevector()
#Comando para representar los estados de los qubits
plot_bloch_multivector(statevector)
#Se imprimen los gráficos
plt.show()