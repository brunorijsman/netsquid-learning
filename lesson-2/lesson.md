# Qubits

NetSquid simulates physical quantum information processing systems: quantum computers and quantum
networks.
So, it is not surprising that NetSquid contains various classes to represent and manipulate qubits,
including:

 * Class 
   [*Qubit*](https://docs.netsquid.org/latest-release/netsquid.qubits.html#netsquid.qubits.qubit.Qubit)
   represents an idealized qubit.

 * Class
   [*Operator*](https://docs.netsquid.org/latest-release/netsquid.qubits.html#netsquid.qubits.operators.Operator)
   represents a quantum operator (e.g. a CNOT gate).

 * Class
   [*QState*](https://docs.netsquid.org/latest-release/netsquid.qubits.html#netsquid.qubits.qstate.QState)
   represents the state of a qubit. 
   In real life we cannot access the state of a qubit, we can only measure a qubit (which collapses
   the state).
   But in simulations we can "peek under the hood" and look at the state, which is very useful for
   debugging our algorithms.
   The internal representation of the state depends on the formalism.

NetSquid supports three quantum formalisms to internally represent the state of a single or a group
of entangled qubits:
 
 * Ket state formalism
 
 * Density Matrix (DM) state formalism
 
 * Stabilizer state formalism
 
All of these classes are idealized representations, as opposed to accurate simulations of real
quantum devices.
For example, all operations (e.g. a CNOT gate) on a qubit take zero time, always succeed, and have
perfect results (i.e. no noise).

These idealized representations are used as building blocks for simulating actual quantum devices.
The density matrix formalism is used to model the fact that real devices are imperfect (have noise). 
And discrete event simulation (discussed earlier in lesson 1) is used to model the fact that in the
real world operations are not instantaneous but take some finite amount of time.

A brief introduction to qubit state representation and manipulation in NetSquid is provided at
https://docs.netsquid.org/latest-release/overview.qubits.html (login required).

# Ket state formalism example: teleportation

The ket state formalism is used to represent the pure state of a qubit or a group of qubits.

As an example of how to use ket states, we will implement a simulation of teleportation: we are
going to teleport the state of a source qubit **qs** to a destination qubit **qd**.

We first create a Bell pair of qubits **qd** and **qh** in state |&#x3a6;+>.
Qubit **qd** is the destination qubit to which the state of the source qubit **qs** will be
teleported.
Qubit **qh** is a helper qubit.

Normally (e.g. in a quantum network), after the creation of qubits **qd** and **qh**, they would be
physically distributed: **qd** would be sent to the destination location, and qubit **qh** would be
sent to the source location (where **qs** resides).
This would happen a-priori before the teleportation takes place.

However, in this example we skip this step and do the teleportation locally in a single location.
In other words, the source qubit **qs** and the destination qubit **qd** are at the same location,
and we are only interested in transferring the state from one qubit **qs** to another qubit **qd**.

We then create the source qubit **qs** and initialize it to some state that is known to us. 
The initialization state is randomly selected from a set small of candidate states, namely |0>, |1>,
|+>, |->, |i>, or |-i>.
After we create the source qubit, we remember the state that was chosen for it.

Teleportation doesn't actually require that the source bit **qs** is in some known state.
Teleportation can teleport a source qubit **qs** in any unknown state.

But for the purpose of this example, we set the state of the source qubit **qs** to a known state.
This allows us the compare the state of the destination qubit **qd** after teleportation with the
chosen state for the source qubit **qs** and verify that they are the same (i.e. that the
teleportation worked correctly).

Of course, in real life, we cannot determine the state of the destination qubit **qd** after the 
teleportation.
In real life, we can only _measure_ **qd** in some basis which does not (in general) determine it's
full state.
But not to worry, we are doing a simulation here, and we can look "under the hood" of the simulation
and determine the full state of **qd**.
More specifically, we use the fidelity as a measure of how close the destination qubit **qd** is to
the chosen and hence expected state. The fidelity should be exactly 1.0 (allowing for some rounding
errors in the floating point calculations)

The steps for actually performing the teleportation are as follows:

 * Perform a Bell State Measurement (BSM) on qubits **qs** and **qh** to produce two classical bits.
   The exact steps are as follows:

   * CNOT(**qs**, **qh**)

   * H(**qs**)

   * **b1** = MEASURE(**qs**)

   * **b2** = MEASURE(**qh**)

 * At this point, normally the two classical bits **b1** and **b2** would be transmitted from one
   location to another location, but since we are doing everyting in one location, this step is
    skipped.

 * Apply local corrections to **qd**:

   * If **b1** **b2** = 00 then do nothing (no correction is needed)

   * If **b1** **b2** = 01 then X(**bd**)

   * If **b1** **b2** = 10 then Z(**bd**)

   * If **b1** **b2** = 11 then Y(**bd**)

 * At this point the destination qubit **qd** has the state that source qubit **qs** used to have
   before the teleportation. Also the state of source qubit **qs** has collapsed to |0> or |1>,
   which means we did not violate the no-cloning theorem.

Since our implementation of teleportation (file teleportation.py) uses the ket state formalism,
it is (as discussed before) an idealized simulation. 
It does not take into account that in real implementations operations would take some finite amount
of time, that qubits would decohere during those time intervals, that operations are imperfect due
to noise etc.
Hence, in this implementation the teleportation always succeeds and the fidelity of the destination
qubit is always 1.00.

# Density matrix state formalism examle

TODO

# Stabilizer state formalism example

TODO

