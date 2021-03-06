# -*- coding: utf-8 -*-


"""
controlled-Phase gate.
"""
from renom_q.circuit import Gate
from renom_q.circuit import QuantumCircuit
from renom_q.circuit import QuantumRegister
from renom_q.circuit.decorators import _control_target_gate
from renom_q.converters.dagcircuit import DAGCircuit
from . import header  # pylint: disable=unused-import
from .h import HGate
from .cx import CnotGate


class CzGate(Gate):
    """controlled-Z gate."""

    def __init__(self, ctl, tgt, circ=None):
        """Create new CZ gate."""
        super().__init__("cz", [], [ctl, tgt], circ)

    def _define_decompositions(self):
        """
        gate cz a,b { h b; cx a,b; h b; }
        """
        decomposition = DAGCircuit()
        q = QuantumRegister(2, "q")
        decomposition.add_qreg(q)
        decomposition.add_basis_element("h", 1, 0, 0)
        decomposition.add_basis_element("cx", 2, 0, 0)
        rule = [
            HGate(q[1]),
            CnotGate(q[0], q[1]),
            HGate(q[1])
        ]
        for inst in rule:
            decomposition.apply_operation_back(inst)
        self._decompositions = [decomposition]

    def inverse(self):
        """Invert this gate."""
        return self  # self-inverse

    def reapply(self, circ):
        """Reapply this gate to corresponding qubits in circ."""
        self._modifiers(circ.cz(self.qargs[0], self.qargs[1]))


@_control_target_gate
def cz(self, ctl, tgt):
    """Apply CZ to circuit."""
    self._check_qubit(ctl)
    self._check_qubit(tgt)
    self._check_dups([ctl, tgt])
    return self._attach(CzGate(ctl, tgt, self))


QuantumCircuit.cz = cz
