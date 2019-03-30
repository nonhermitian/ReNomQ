# -*- coding: utf-8 -*-


"""
Node for an OPENQASM if statement.
"""
from ._node import Node


class If(Node):
    """Node for an OPENQASM if statement.

    children[0] is an id node.
    children[1] is an integer node.
    children[2] is quantum operation node, including U, CX, custom_unitary,
    measure, reset, (and BUG: barrier, if).
    """

    def __init__(self, children):
        """Create the if node."""
        Node.__init__(self, 'if', children, None)

    def qasm(self, prec=15):
        """Return the corresponding OPENQASM string."""
        return "if(" + self.children[0].qasm(prec) + "==" \
               + str(self.children[1].value) + ") " + \
               self.children[2].qasm(prec)
