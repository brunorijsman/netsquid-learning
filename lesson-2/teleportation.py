import netsquid as ns
import random

VERBOSE = False

STATE_ZERO = "|0>"
STATE_ONE = "|1>"
STATE_PLUS = "|+>"
STATE_MINUS = "|->"
STATE_PLUS_I = "|i>"
STATE_MINUS_I = "|-i>"

ALL_STATES = [
    STATE_ZERO,
    STATE_ONE,
    STATE_PLUS,
    STATE_MINUS,
    STATE_PLUS_I,
    STATE_MINUS_I]

def report(message):
    if VERBOSE:
        print(message)

def create_random_state_and_qubit():
    state = random.choice(ALL_STATES)
    q, = ns.qubits.create_qubits(1)
    if state == STATE_ZERO:
        pass
    elif state == STATE_ONE:
        ns.qubits.operate(q, ns.X)
    elif state == STATE_PLUS:
        ns.qubits.operate(q, ns.Ry90)
    elif state == STATE_MINUS:
        ns.qubits.operate(q, ns.Ry270)
    elif state == STATE_PLUS_I:
        ns.qubits.operate(q, ns.Rx270)
    elif state == STATE_MINUS_I:
        ns.qubits.operate(q, ns.Rx90)
    else:
        assert False, "Unexpected values for state"
    return state, q

def qubits_has_state(q, state):
    # Note: this is impossible to check in real life, but we are doing a simulation, so we can peek
    # under the hood.
    if state == STATE_ZERO:
        expected_ket_state = ns.qubits.ketstates.s0
    elif state == STATE_ONE:
        expected_ket_state = ns.qubits.ketstates.s1
    elif state == STATE_PLUS:
        expected_ket_state = ns.qubits.ketstates.h0
    elif state == STATE_MINUS:
        expected_ket_state = ns.qubits.ketstates.h1
    elif state == STATE_PLUS_I:
        expected_ket_state = ns.qubits.ketstates.y0
    elif state == STATE_MINUS_I:
        expected_ket_state = ns.qubits.ketstates.y1
    else:
        assert False, "Unexpected values for state"
    fidelity = ns.qubits.fidelity(q, expected_ket_state)
    return fidelity > 0.9999

def create_phi_plus_bell_pair():
    q1, q2 = ns.qubits.create_qubits(2)
    ns.qubits.operate(q1, ns.H)
    ns.qubits.operate([q1, q2], ns.CNOT)
    return q1, q2

def bell_state_measurement(q1, q2):
    ns.qubits.operate([q1, q2], ns.CNOT)
    ns.qubits.operate(q1, ns.H)
    b1, _ = ns.qubits.measure(q1)
    b2, _ = ns.qubits.measure(q2)
    return b1, b2

def bell_state_correction(q, b1, b2):
    if (b1, b2) == (0, 0):
        pass
    elif (b1, b2) == (0, 1):
        ns.qubits.operate(q, ns.X)
    elif (b1, b2) == (1, 0):
        ns.qubits.operate(q, ns.Z)
    elif (b1, b2) == (1, 1):
        ns.qubits.operate(q, ns.Y)
    else:
        assert False, "Unexpected values for classical bits"

def teleport_one_qubit():
    # Pick a random state from a limited set of candidate states (ALL_STATES), remember what state
    # we chose, and create a source qubit in that state.
    source_state, source_qubit = create_random_state_and_qubit()
    # Create a |Φ+> Bell pair. One qubit is used as the destination qubit, and the other as a
    # helper qubit.
    helper_qubit, destination_qubit = create_phi_plus_bell_pair()
    # Perform a Bell State Measurement (BSM) on the source and helper qubits. This yields two
    # classical bits b1 and b2.
    b1, b2 = bell_state_measurement(source_qubit, helper_qubit)
    # Perform a Bell State Correction on the destination qubit, based on the values of classical
    # bits b1 and b2.
    bell_state_correction(destination_qubit, b1, b2)
    # Check whether the destination qubit has ket state that was chosed for the source qubit, to
    # check whether the teleportation was succesful. Note: this is impossible to check in real life,
    # but we are doing a simulation, so we can peek under the hood.
    success = qubits_has_state(destination_qubit, source_state)
    # Report result
    report(f"Teleportation of qubit {source_state}: {'success' if success else 'FAILURE'}")
    return success

if __name__ == "__main__":
    ns.set_qstate_formalism(ns.QFormalism.KET)
    success_count = 0
    fail_count = 0
    for _ in range(1000):
        if teleport_one_qubit():
            success_count += 1
        else:
            fail_count += 1
    print(f"{success_count} teleportations succeeded, {fail_count} teleportations failed")
