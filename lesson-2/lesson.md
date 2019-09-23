# Qubits

NetSquid simulates physical quantum information processing systems: quantum computers and quantum
networks.

NetSquid contains various generalized classes to represent and manipulate qubits. These generalized
classes are used as building blocks to implement simulations of specific quantum technologies, such
as nitrogen vacancy centers (NV), atomic ensembles, ion traps, etc.

NetSquid supports three quantum formalisms to internally represent the state of a single or a group
of entangled qubits:
 
 * Ket state formalism
 
 * Density Matrix (DM) state formalism
 
 * Stabilizer state formalism

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
The initialization state is randomly selected from a set of candidate states, namely |0>, |1>, |+>,
|->, |i>, or |-i>.

Teleportation doesn't actually require that the source bit **qs** is in some known state.
Teleportation can teleport a source qubit **qs** in any unknown state.

But for the purpose of this example, we set the state of the source qubit **qs** to a known state.
This allows us the compare the state of the destination qubit **qd** after teleportation with the
original state of the source qubit **qs** and verify that they are the same (i.e. that the
teleportation worked correctly).

Of course, in real life, we cannot determine the state of the destination qubit **qd**.
In real life, we can only _measure_ **qd** in some basis which does not (in general) determine it's
full state.
But not to worry, we are doing a simulation here, and we can look "under the hood" of the simulation
and determine the full state of **qd**.

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

# Density matrix state formalism examle

TODO

# Stabilizer state formalism example

TODO

