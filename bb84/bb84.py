#IMPLEMENTACIÓN DEL PROTOCOLO CUÁNTICO DE COMPARTICIÓN DE CLAVE BB84

#Importaciones
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler

#Imponer un ataque en el protocolo (hará que falle)
ataqueEve = False

#Numero de qubits enviados y reservados para seguridad
nQubits = 100
nSeguridad = 10

#Se inicializa el estado de los qubits y las bases en las que se miden
basesAlice = np.random.randint(2, size=nQubits).tolist()
basesBob = np.random.randint(2, size=nQubits).tolist()
estadosAlice = np.random.randint(2, size=nQubits).tolist()
estadosBob = []

basesEve = np.random.randint(2, size=nQubits).tolist()

#Se instancia un simulador
aersim = AerSimulator()
sampler = Sampler(backend=aersim)
#Solo es necesario enviar cada qubit una vez
sampler.options.default_shots = 1

for i in range(nQubits):
    qc = QuantumCircuit(1)
    #Si el bit vale 0, el qubit será |0> o |+>
    #Si el bit vale 1, el qubit será |1> o |->
    if (estadosAlice[i] == 1):
        qc.x(0)
    #Si el bit vale 0, se mide en la base computacional (|0> o |1>)
    #Si el bit vale 1, se mide en la base de Hadamard (|+> o |->)
    if (basesAlice[i] == 1):
        qc.h(0)

    #Si se produce un ataque, Eve mide los qubits y los reenvia
    if (ataqueEve):
        if (basesEve[i] == 1):
            qc.h(0)
            qc.measure_all()
            ejecucion = sampler.run([qc]).result()
            estEve = list(ejecucion[0].data.meas.get_counts())[0]

            #Eve manda el qubit que acaba de medir
            qc = QuantumCircuit(1)
            if (estEve == 1):
                qc.x(0)
            if (basesEve[i] == 1):
                qc.h(0)

    #El qubit llega a Bob
    if (basesBob[i] == 1):
        qc.h(0)
    qc.measure_all()
    ejecucion = sampler.run([qc]).result()
    estBob = list(ejecucion[0].data.meas.get_counts())[0]
    #Bob va apuntando los estados que recibe
    estadosBob.append(int(estBob))

index = 0
while index < nQubits:
    #Se purgan los qubits donde Alice y Bob hayan usado diferentes bases
    if (basesAlice[index] != basesBob[index]):
        del basesAlice[index]
        del basesBob[index]
        del estadosAlice[index]
        del estadosBob[index]
        nQubits -= 1
    else:
        index += 1

claveValida = True
for i in range(nSeguridad):
    #Si algun qubit difiere, se cancela el protocolo
    if (estadosAlice[i] != estadosBob[i]):
        claveValida = False
        break

if claveValida:
    print("PROTOCOLO EXITOSO")
    #La clave son los qubits que no se han usado en seguridad
    print("CLAVE:", estadosBob[nSeguridad:])
else:
    print("PROTOCOLO FALLIDO")
