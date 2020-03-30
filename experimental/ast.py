


class Number:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)

    def as_html(self) -> str:
        return self.value


class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()

    def as_html(self) -> str:
        return self.left.as_html() + ' + ' + self.right.as_html()


class Subtract(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()

    def as_html(self) -> str:
        return self.left.as_html() + ' - ' + self.right.as_html()


class Multiply(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()

    def as_html(self) -> str:
        return self.left.as_html() + ' * ' + self.right.as_html()


class Divide(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()

    def as_html(self) -> str:
        return self.left.as_html() + ' / ' + self.right.as_html()


class Print:
    def __init__(self, value):
        self.value = value

    def eval(self):
        print(self.value.eval())

    # noinspection PyMethodMayBeStatic
    def as_html(self) -> str:
        return ''


class View:
    def __init__(self, name, attributes, contents):
        self.name = name
        self.attributes = attributes
        self.contents = contents

    def as_html(self) -> str:
        return f'<{self.name} {self.attributes.as_html()}>{self.contents.as_html()}</{self.name}>'


class ViewAttribute:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def as_html(self):
        return f'{self.key}={self.value.as_html}'
