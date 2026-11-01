
# a
class ParkingPermit:

    def __init__(self, owner: str, months: int, fee_schedule: dict):
        """Initializes the owner, purchased months, and fee schedule."""
        self.owner = owner
        self.months = months
        self.fee_schedule = fee_schedule

    def cost(self) -> float:
        """Returns the permit cost"""
        raise NotImplementedError("Subclasses must implement cost()")

    # d
    def __str__(self) -> str:
        """Returns a  description of the permit."""
        return f"Owner: {self.owner}, Months: {self.months}"

    def __repr__(self) -> str:
        """Returns a representation of the permit."""
        return (f"ParkingPermit(owner={self.owner!r}, "
                f"months={self.months!r}, "
                f"fee_schedule={self.fee_schedule!r})")

# b
class StudentPermit(ParkingPermit):
    """Represents a student parking permit."""

    def __init__(self, owner: str, months: int,
                 fee_schedule: dict, vehicles: int):
        """Initializes a student permit and registered vehicle count."""
        super().__init__(owner, months, fee_schedule)
        self.vehicles = vehicles

# c
    def cost(self) -> float:
        """Calculates monthly fees plus one-time fees for extra vehicles."""
        return (self.months * self.fee_schedule["student_monthly"]
                + max(0, self.vehicles - 1)
                * self.fee_schedule["extra_vehicle"])
# d
    def __str__(self) -> str:
        """Returns a readable student permit description."""
        return (f"StudentPermit: {super().__str__()}, "
                f"Vehicles: {self.vehicles}, Cost: ${self.cost():.2f}")

    def __repr__(self) -> str:
        """Returns a detailed student permit representation."""
        return (f"StudentPermit({self.owner!r}, {self.months!r}, "
                f"{self.fee_schedule!r}, {self.vehicles!r})")

# b
class FacultyPermit(ParkingPermit):
    """Represent a faculty parking permit."""

    def __init__(self, owner: str, months: int,
                 fee_schedule: dict, garage_access: bool):
        """Initialize a faculty permit and garage access status."""
        super().__init__(owner, months, fee_schedule)
        self.garage_access = garage_access
# c
    def cost(self) -> float:
        """Calculates monthly fees including optional garage access."""
        monthly = self.fee_schedule["faculty_monthly"]

        if self.garage_access:
            monthly += self.fee_schedule["garage_monthly"]

        return self.months * monthly
# d
    def __str__(self) -> str:
        """Returns a readable faculty permit description."""
        return (f"FacultyPermit: {super().__str__()}, "
                f"Garage Access: {self.garage_access}, "
                f"Cost: ${self.cost():.2f}")

    def __repr__(self) -> str:
        """Returns a detailed faculty permit representation."""
        return (f"FacultyPermit({self.owner!r}, {self.months!r}, "
                f"{self.fee_schedule!r}, {self.garage_access!r})")

# e
def summarize_list(permits: list[ParkingPermit]) -> float:
    """Prints each owner's name and cost, then return total revenue."""
    total = 0.0

    for permit in permits:
        price = permit.cost()
        print(f"{permit.owner}: ${price:.2f}")
        total += price

    return total

# f
def main() -> None:
    """Shows permit creation, printing, and revenue calculation."""

    fees = {
        "student_monthly": 25,
        "extra_vehicle": 10,
        "faculty_monthly": 40,
        "garage_monthly": 15
    }

    permits = [
        StudentPermit("Alice", 4, fees, 2),
        StudentPermit("Bob", 3, fees, 1),
        FacultyPermit("Charlie", 6, fees, True),
        FacultyPermit("Diana", 2, fees, False)
    ]

    print("Parking Permit Objects")
    for permit in permits:
        print(permit)
        print(repr(permit))

    print("\nPermit Revenue Summary")
    total = summarize_list(permits)

    print(f"\nTotal Revenue: ${total:.2f}")


if __name__ == "__main__":
    main()
