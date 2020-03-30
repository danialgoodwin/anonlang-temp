from src.equality import Equality


class ArithmeticExpression(Equality):
    """Handle arithmetic expressions, for example:
    - 42
    - myVariable
    - myVariable + 42
    """
    pass


class NumberArithmeticExpression(ArithmeticExpression):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return f'NumberAexp({self.i})'

    def eval(self, env):
        return self.i

    def as_html(self, env):
        return self.i


class VarArithmeticExpression(ArithmeticExpression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'VarAexp({self.name})'

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0

    def as_html(self, env):
        return self.name


class BinaryOpArithmeticExpression(ArithmeticExpression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return f'BinaryOpAexp({self.op}, {self.left}, {self.right})'


###################################################################################################


class BooleanExpression(Equality):
    """Handle boolean expressions, for example:
    - myVariable < 42
    - myVariable < 42 and foo > 12
    - myVariable < 42 or foo > 12
    - not myVariable
    """
    pass


class RelationalOpBooleanExpression(BooleanExpression):
    def __init__(self, op, left: ArithmeticExpression, right: ArithmeticExpression):
        ...


class AndBooleanExpression(BooleanExpression):
    def __init__(self, left: BooleanExpression, right: BooleanExpression):
        ...


class OrBooleanExpression(BooleanExpression):
    def __init__(self, left: BooleanExpression, right: BooleanExpression):
        ...


class NotBooleanExpression(BooleanExpression):
    def __init__(self, exp: BooleanExpression):
        ...


###################################################################################################


class Statement(Equality):
    """Handle core features of the language."""
    pass


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        ...


class CompoundStatement(Statement):
    def __init__(self, first, second):
        ...


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        ...


class LoopStatement(Statement):
    def __init__(self, condition, body):
        ...
