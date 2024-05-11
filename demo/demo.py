from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
 
# Create a new circuit with two qubits (first argument) and two classical
# bits (second argument)
qc = QuantumCircuit(2, 2)
 
# Add a Hadamard gate to qubit 0
qc.h(0)
 
# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(0, 1)
 
# Measure qubit 0 to cbit 0, and qubit 1 to cbit 1
qc.measure(0, 0)
qc.measure(1, 1)
 
# Return a drawing of the circuit using MatPlotLib ("mpl"). This is the
# last line of the cell, so the drawing appears in the cell output.
# Remove the "mpl" argument to get a text drawing.
qc.draw("mpl")


 
service = QiskitRuntimeService(name="Antonio Gonzalez")
# Run on a simulator
backend = service.get_backend("ibmq_qasm_simulator")
# Create a Sampler object
sampler = Sampler(backend)
# Submit the circuit to the sampler
job = sampler.run(qc)
# Once the job is complete, get the result
job.result()