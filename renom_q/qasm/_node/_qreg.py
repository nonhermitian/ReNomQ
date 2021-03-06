# -*- coding: utf-8 -*-


"""
Node for an OPENQASM qreg statement.
"""
from ._node import Node


class Qreg(Node):
    """Node for an OPENQASM qreg statement.

    children[0] is an indexedid node.
    """

    def __init__(self, children):
        """Create the qreg node."""
        Node.__init__(self, 'qreg', children, None)
        # This is the indexed id, the full "id[n]" object
        self.id = children[0]
        # Name of the qreg
        self.name = self.id.name
        # Source line number
        self.line = self.id.line
        # Source file name
        self.file = self.id.file
        # Size of the register
        self.index = self.id.index

    def to_string(self, indent):
        """Print the node data, with indent."""
        ind = indent * ' '
        print(ind, 'qreg')
        self.children[0].to_string(indent + 3)

    def qasm(self, prec=15):
        """Return the corresponding OPENQASM string."""
        return "qreg " + self.id.qasm(prec) + ";"
