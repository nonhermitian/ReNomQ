# -*- coding: utf-8 -*-


"""
S=diag(1,i) Clifford phase gate or its inverse.
"""
from renom_q.circuit import Gate
from renom_q.circuit import QuantumCircuit
from renom_q.circuit import QuantumRegister
from renom_q.circuit.decorators import _1q_gate
from renom_q.qasm import pi
from renom_q.converters.dagcircuit import DAGCircuit
from . import header  # pylint: disable=unused-import
from .u1 import U1Gate


class SGate(Gate):
    """S=diag(1,i) Clifford phase gate."""

    def __init__(self, qubit, circ=None):
        """Create new S gate."""
        super().__init__("s", [], [qubit], circ)

    def _define_decompositions(self):
        """
        gate s a { u1(pi/2) a; }
        """
        decomposition = DAGCircuit()
        q = QuantumRegister(1, "q")
        decomposition.add_qreg(q)
        decomposition.add_basis_element("u1", 1, 0, 1)
        rule = [
            U1Gate(pi / 2, q[0])
        ]
        for inst in rule:
            decomposition.apply_operation_back(inst)
        self._decompositions = [decomposition]

    def reapply(self, circ):
        """Reapply this gate to corresponding qubits in circ."""
        self._modifiers(circ.s(self.qargs[0]))

    def inverse(self):
        """Invert this gate."""
        inv = SdgGate(self.qargs[0])
        self.circuit.data[-1] = inv  # replaces the gate with the inverse
        return inv


class SdgGate(Gate):
    """Sdg=diag(1,-i) Clifford adjoin phase gate."""

    def __init__(self, qubit, circ=None):
        """Create new Sdg gate."""
        super().__init__("sdg", [], [qubit], circ)

    def _define_decompositions(self):
        """
        gate sdg a { u1(-pi/2) a; }
        """
        decomposition = DAGCircuit()
        q = QuantumRegister(1, "q")
        decomposition.add_qreg(q)
        decomposition.add_basis_element("u1", 1, 0, 1)
        rule = [
            U1Gate(-pi / 2, q[0])
        ]
        for inst in rule:
            decomposition.apply_operation_back(inst)
        self._decompositions = [decomposition]

    def reapply(self, circ):
        """Reapply this gate to corresponding qubits in circ."""
        self._modifiers(circ.sdg(self.qargs[0]))

    def inverse(self):
        """Invert this gate."""
        inv = SGate(self.qargs[0])
        self.circuit.data[-1] = inv  # replaces the gate with the inverse
        return inv


@_1q_gate
def s(self, q):
    """Apply S to q."""
    self._check_qubit(q)
    return self._attach(SGate(q, self))


@_1q_gate
def sdg(self, q):
    """Apply Sdg to q."""
    self._check_qubit(q)
    return self._attach(SdgGate(q, self))


QuantumCircuit.s = s
QuantumCircuit.sdg = sdg
