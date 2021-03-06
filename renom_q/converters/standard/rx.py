# -*- coding: utf-8 -*-


"""
Rotation around the x-axis.
"""
from renom_q.circuit import Gate
from renom_q.circuit import QuantumCircuit
from renom_q.circuit import QuantumRegister
from renom_q.circuit.decorators import _1q_gate
from renom_q.qasm import pi
from renom_q.converters.dagcircuit import DAGCircuit
from . import header  # pylint: disable=unused-import
from .u3 import U3Gate


class RXGate(Gate):
    """rotation around the x-axis."""

    def __init__(self, theta, qubit, circ=None):
        """Create new rx single qubit gate."""
        super().__init__("rx", [theta], [qubit], circ)

    def _define_decompositions(self):
        """
        gate rx(theta) a {u3(theta, -pi/2, pi/2) a;}
        """
        decomposition = DAGCircuit()
        q = QuantumRegister(1, "q")
        decomposition.add_qreg(q)
        decomposition.add_basis_element("u3", 1, 0, 3)
        rule = [
            U3Gate(self.params[0], -pi / 2, pi / 2, q[0])
        ]
        for inst in rule:
            decomposition.apply_operation_back(inst)
        self._decompositions = [decomposition]

    def inverse(self):
        """Invert this gate.

        rx(theta)^dagger = rx(-theta)
        """
        self.params[0] = -self.params[0]
        self._decompositions = None
        return self

    def reapply(self, circ):
        """Reapply this gate to corresponding qubits in circ."""
        self._modifiers(circ.rx(self.params[0], self.qargs[0]))


@_1q_gate
def rx(self, theta, q):
    """Apply Rx to q."""
    self._check_qubit(q)
    return self._attach(RXGate(theta, q, self))


QuantumCircuit.rx = rx
