
import turtle


def draw_leaf_straight(level: int, length: float) -> None:
    """Draw a recursive tree with smaller branches.

    Parameters:
        level: Number of recursive levels.
        length: Length of the main stem.

    Preconditions:
        level must be nonnegative.
        length must be positive.

    Postconditions:
        Draws a branching tree and restores the turtle's
        original position and direction.
    """
    if level == 0:
        return

    turtle.forward(length)

    turtle.left(30)
    draw_leaf_straight(level - 1, length * 0.7)

    turtle.right(60)
    draw_leaf_straight(level - 1, length * 0.7)

    turtle.left(30)
    turtle.backward(length)
    
def draw_leaf_curved(level: int, length: float) -> None:
    """Draw a recursive leaf with curved branches.

    Parameters:
        level: Number of recursive levels.
        length: Length of the main stem.

    Preconditions:
        level must be nonnegative.
        length must be positive.

    Postconditions:
        Draws a curved recursive tree and restores
        the turtle's original position and heading.
    """
    if level == 0:
        return

    steps = 5
    step_length = length / steps

    for i in range(steps):
        turtle.forward(step_length)
        turtle.left(3)

    turtle.left(25)
    draw_leaf_curved(level - 1, length * 0.65)

    turtle.right(50)
    draw_leaf_curved(level - 1, length * 0.65)

    turtle.left(25)

    for i in range(steps):
        turtle.right(3)
        turtle.backward(step_length)






# b)
def strB(n: int, base: int = 10) -> str:
    """Convert a nonnegative integer to a string in the given base.

    Parameters:
        n: Nonnegative integer to convert.
        base: Number base between 2 and 26.

    Preconditions:
        n must be a nonnegative integer.
        base must be an integer between 2 and 26.

    Postconditions:
        Returns the converted number as a string.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    if n < 0:
        raise ValueError("n cannot be negative")

    if not isinstance(base, int):
        raise TypeError("base must be an integer")

    if base < 2 or base > 26:
        raise ValueError("base must be between 2 and 26")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if n < base:
        return digits[n]

    return strB(n // base, base) + digits[n % base]


def testif(condition: bool, success: str, failure: str) -> None:
    """Print a message depending on whether a test passes."""
    if condition:
        print(success)
    else:
        print(failure)


def test_strB() -> None:
    """Run four unit tests for the recursive strB function."""

    testif(strB(1234, 10) == "1234",
           "Base 10 test passed",
           "Base 10 test failed")

    testif(strB(100, 8) == "144",
           "Base 8 test passed",
           "Base 8 test failed")

    testif(strB(1234, 16) == "4D2",
           "Base 16 test passed",
           "Base 16 test failed")

    testif(strB(100, 2) == "1100100",
           "Base 2 test passed",
           "Base 2 test failed")



def main() -> None:
    """Display a menu to select which function to run."""
    while True:
        print("\n=== Homework 3 Problem 5 ===")
        print("1. Draw Straight Leaf")
        print("2. Draw Curved Leaf")
        print("3. Base X Conversion")
        print("4. Run strB Tests")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1" or choice == "2":
            turtle.reset()
            turtle.setup(800, 800)
            turtle.speed(0)
            turtle.hideturtle()
            turtle.tracer(0, 0)

            turtle.penup()
            turtle.goto(0, -300)
            turtle.setheading(90)
            turtle.pendown()

            if choice == "1":
                draw_leaf_straight(8, 120)
            else:
                draw_leaf_curved(6, 120)

            turtle.update()
            print("Close the turtle window to return to the menu.")
            turtle.done()

        elif choice == "3":
            n = int(input("Enter a nonnegative integer: "))
            base = int(input("Enter a base (2-26): "))
            print("Result:", strB(n, base))

        elif choice == "4":
            test_strB()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
