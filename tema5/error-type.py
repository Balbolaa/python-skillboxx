# Import the BlockErrors class (assumed it exists in a module called block_errors)
from block_errors import BlockErrors

# Example 1: Suppressing both ZeroDivisionError and TypeError
err_types = {ZeroDivisionError, TypeError}
with BlockErrors(err_types):
    # This will raise a ZeroDivisionError because of division by zero
    a = 1 / 0
# Since ZeroDivisionError is being suppressed, the error is ignored and this message is printed
print('Выполнено без ошибок')  # Expected output: Выполнено без ошибок

# Example 2: Suppressing only ZeroDivisionError
err_types = {ZeroDivisionError}
with BlockErrors(err_types):
    # This will raise a TypeError because of attempting to divide an int by a string
    a = 1 / '0'
# TypeError is not being suppressed, so the error is raised and this line won't be printed
print('Выполнено без ошибок')  # Expected output: TypeError: unsupported operand type(s) for /: 'int' and 'str'

# Example 3: Nested blocks - inner block suppresses ZeroDivisionError, outer block suppresses TypeError
outer_err_types = {TypeError}
with BlockErrors(outer_err_types):
    inner_err_types = {ZeroDivisionError}
    with BlockErrors(inner_err_types):
        # This will raise a TypeError because of attempting to divide an int by a string
        a = 1 / '0'
    # The inner block does not suppress TypeError, so it bubbles up to the outer block
    # Outer block will suppress the TypeError, so this line will be printed
    print('Внутренний блок: выполнено без ошибок')  # Expected output: Внутренний блок: выполнено без ошибок
# Since TypeError is suppressed by the outer block, this line is also printed
print('Внешний блок: выполнено без ошибок')  # Expected output: Внешний блок: выполнено без ошибок

# Example 4: Suppressing all exceptions (since Exception is the base class for most errors)
err_types = {Exception}
with BlockErrors(err_types):
    # This will raise a TypeError because of attempting to divide an int by a string
    a = 1 / '0'
# Since Exception is being suppressed (and TypeError is a subclass of Exception), this line will be printed
print('Выполнено без ошибок')  # Expected output: Выполнено без ошибок
