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

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

    def as_html(self, env):
        return f'{self.left.as_html()} {self.op.as_html()} {self.right.as_html()}'


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
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

    def as_html(self):
        return f'{self.left.as_html()} {self.op.as_html()} {self.right.as_html()}'


class AndBooleanExpression(BooleanExpression):
    def __init__(self, left: BooleanExpression, right: BooleanExpression):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value

    def as_html(self):
        return f'{self.left.as_html()} {self.op.as_html()} {self.right.as_html()}'



class OrBooleanExpression(BooleanExpression):
    def __init__(self, left: BooleanExpression, right: BooleanExpression):
        self.left = left
        self.right = right

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value

    def as_html(self):
        return f'{self.left.as_html()} {self.op.as_html()} {self.right.as_html()}'


class NotBooleanExpression(BooleanExpression):
    def __init__(self, exp: BooleanExpression):
        self.exp = exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value

    def as_html(self):
        return 'not'

###################################################################################################


class Statement(Equality):
    """Handle core features of the language."""
    pass


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def eval(self, env):
        value = self.aexp.eval(env)
        env[self.name] = value

    def as_html(self):
        return f'{self.name.as_html()} = {self.aexp.as_html()}'


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

    def as_html(self):
        return f'{self.first.as_html()} {self.second.as_html()}'


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)

    def as_html(self):
        output = f'if {self.condition.as_html()} {self.true_stmt.as_html()}'
        if self.false_stmt:
            output += f'else: {self.false_stmt.as_html()}'
        return


class LoopStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)

    def as_html(self):
        return f'while ({self.condition.as_html()}) {self.body.as_html()}'
