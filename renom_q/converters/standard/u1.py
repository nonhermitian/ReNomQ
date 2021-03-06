# -*- coding: utf-8 -*-


"""
Diagonal single qubit gate.
"""
from renom_q.circuit import Gate
from renom_q.circuit import QuantumCircuit
from renom_q.circuit import QuantumRegister
from renom_q.circuit.decorators import _1q_gate
from renom_q.converters.dagcircuit import DAGCircuit
from . import header  # pylint: disable=unused-import
from .ubase import UBase


class U1Gate(Gate):
    """Diagonal single-qubit gate."""

    def __init__(self, theta, qubit, circ=None):
        """Create new diagonal single-qubit gate."""
        super().__init__("u1", [theta], [qubit], circ)

    def _define_decompositions(self):
        decomposition = DAGCircuit()
        q = QuantumRegister(1, "q")
        decomposition.add_qreg(q)
        decomposition.add_basis_element("U", 1, 0, 3)
        rule = [
            UBase(0, 0, self.params[0], q[0])
        ]
        for inst in rule:
            decomposition.apply_operation_back(inst)
        self._decompositions = [decomposition]

    def inverse(self):
        """Invert this gate."""
        self.params[0] = -self.params[0]
        self._decompositions = None
        return self

    def reapply(self, circ):
        """Reapply this gate to corresponding qubits in circ."""
        self._modifiers(circ.u1(self.params[0], self.qargs[0]))


@_1q_gate
def u1(self, theta, q):
    """Apply u1 with angle theta to q."""
    self._check_qubit(q)
    return self._attach(U1Gate(theta, q, self))


QuantumCircuit.u1 = u1
