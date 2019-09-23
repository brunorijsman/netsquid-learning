import netsquid as ns

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

def pick_random_state_description():
    return random.choice(ALL_STATES)

def create_qubit_for_chose_state(state):
    q, = ns.qubits.create_qubits(1)
    if state == STATE_ZERO:
        pass
    elif state == STATE_ONE:
        ns.qubits.operate(q, ns.NOT)
    elif state == STATE_PLUS:
        ns.qubits.operate(q, ns.H)
    elif state == STATE_MINUS:
        ns.qubits.operate(q, ns.NOT)
        ns.qubits.operate(q, ns.H)
    elif state == STATE_PLUS_I:
        pass
    elif state == STATE_MINUS_I:
        pass
        


def create_two_identical_random_qubits():
    q1, q2 = ns.qubits.create_qubits(2)
    return q1, q2, "|0>"

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

def qubits_have_same_state(q1, q2):
    # Note: this is impossible to check in real life, but we are doing a simulation, so we can peek
    # under the hood.
    print(f"q2.qstate = {q2.qstate}")
    fidelity = ns.qubits.fidelity(q1, q2.qstate)
    print(f"fidelity: {fidelity}")
    return fidelity > 0.999

def teleport_one_qubit():
    # Create a random source qubit. Also create a copy of this random source qubit to have something
    # to compare the destination qubit with after the teleportation is complete, to check whether
    # the teleportation was succesful. Note that we are not violating the no-cloning theorem here:
    # we are not really copying any qubits, we are simply preparing two qubits in exactly the same
    # way.
    source_qubit, source_qubit_copy, source_qubit_description = create_two_identical_random_qubits()
    print(f"source qubit: {source_qubit.qstate}")
    print(f"source qubit copy: {source_qubit_copy.qstate}")
    print(f"source qubit description: {source_qubit_description}")

    # Create a |Φ+> Bell pair. One qubit is used as the destination qubit, and the other as a
    # helper qubit.
    helper_qubit, destination_qubit = create_phi_plus_bell_pair()
    print(f"destination qubit: {destination_qubit.qstate}")
    print(f"helper qubit: {helper_qubit.qstate}")

    # Perform a Bell State Measurement (BSM) on the source and helper qubits. This yields two
    # classical bits b1 and b2.
    b1, b2 = bell_state_measurement(source_qubit, helper_qubit)
    print("After Bell State Measurement:")
    print(f"classical bits b1 b2: {b1} {b2}")
    print(f"source qubit: {source_qubit.qstate}")
    print(f"helper qubit: {helper_qubit.qstate}")

    # Perform a Bell State Correction on the destination qubit, based on the values of classical
    # bits b1 and b2.
    bell_state_correction(destination_qubit, b1, b2)
    print("After Bell State Correction:")
    print(f"destination qubit: {destination_qubit.qstate}")

    # Check whether the destination qubit has the same ket state as the copy of the source qubit, to
    # check whether the teleportation was succesful. Note: this is impossible to check in real life,
    # but we are doing a simulation, so we can peek under the hood.
    success = qubits_have_same_state(source_qubit_copy, destination_qubit)
    print(f"success: {success}")

if __name__ == "__main__":
    ns.set_qstate_formalism(ns.QFormalism.KET)
    teleport_one_qubit()