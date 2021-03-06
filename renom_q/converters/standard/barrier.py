# -*- coding: utf-8 -*-


"""
Barrier instruction.
"""
from renom_q.circuit import QuantumCircuit
from renom_q.circuit import QuantumRegister
from renom_q.circuit import Instruction
from . import header  # pylint: disable=unused-import


class Barrier(Instruction):
    """Barrier instruction."""

    def __init__(self, qubits, circ=None):
        """Create new barrier instruction."""
        super().__init__("barrier", [], list(qubits), [], circ)

    def inverse(self):
        """Special case. Return self."""
        return self

    def reapply(self, circ):
        """Reapply this instruction to corresponding qubits in circ."""
        self._modifiers(circ.barrier(*self.qargs))


def barrier(self, *qargs):
    """Apply barrier to circuit.
    If qargs is None, applies to all the qbits.
    Args is a list of QuantumRegister or single qubits.
    For QuantumRegister, applies barrier to all the qbits in that register."""
    qubits = []

    if not qargs:  # None
        for qreg in self.qregs:
            for j in range(qreg.size):
                qubits.append((qreg, j))

    for qarg in qargs:
        if isinstance(qarg, (QuantumRegister, list)):
            if isinstance(qarg, QuantumRegister):
                qubits.extend([(qarg, j) for j in range(qarg.size)])
            else:
                qubits.extend(qarg)
        else:
            qubits.append(qarg)

    self._check_dups(qubits)
    for qubit in qubits:
        self._check_qubit(qubit)
    return self._attach(Barrier(qubits, self))


QuantumCircuit.barrier = barrier
