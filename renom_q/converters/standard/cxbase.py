# -*- coding: utf-8 -*-


"""
Fundamental controlled-NOT gate.
"""
from renom_q.circuit import Gate
from renom_q.circuit import QuantumCircuit
from renom_q.circuit.decorators import _control_target_gate
from . import header  # pylint: disable=unused-import


class CXBase(Gate):  # pylint: disable=abstract-method
    """Fundamental controlled-NOT gate."""

    def __init__(self, ctl, tgt, circ=None):
        """Create new CX instruction."""
        super().__init__("CX", [], [ctl, tgt], circ)

    def inverse(self):
        """Invert this gate."""
        return self  # self-inverse

    def reapply(self, circ):
        """Reapply this gate to corresponding qubits in circ."""
        self._modifiers(circ.cx_base(self.qargs[0], self.qargs[1]))


@_control_target_gate
def cx_base(self, ctl, tgt):
    """Apply CX ctl, tgt."""
    self._check_qubit(ctl)
    self._check_qubit(tgt)
    self._check_dups([ctl, tgt])
    return self._attach(CXBase(ctl, tgt, self))


QuantumCircuit.cx_base = cx_base
