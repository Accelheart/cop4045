"""Predator-prey-human island simulation."""
import random
import matplotlib.pyplot as plt
# Lance Van Z23504457

class Island:
    """A square grid containing prey, predators, and humans."""

    def __init__(self, n: int, prey_count: int = 0,
                 predator_count: int = 0, human_count: int = 0) -> None:
        """Create an island with initial populations."""
        if n <= 0 or min(prey_count, predator_count, human_count) < 0:
            raise ValueError("Grid size must be positive and counts nonnegative")
        if prey_count + predator_count + human_count > n * n:
            raise ValueError("More animals than available grid cells")
        self.grid_size = n
        self.grid: list[list[Animal | int]] = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, human_count)

    def init_animals(self, prey_count: int, predator_count: int,
                     human_count: int) -> None:
        """Place each animal in a random empty cell."""
        positions = [(x, y) for x in range(self.grid_size)
                     for y in range(self.grid_size)]
        random.shuffle(positions)
        for cls, count in ((Prey, prey_count), (Predator, predator_count),
                           (Human, human_count)):
            for _ in range(count):
                x, y = positions.pop()
                self.register(cls(self, x, y))

    def clear_all_moved_flags(self) -> None:
        """allows all living animals to act during the next tick."""
        for animal in self.animals():
            animal.clear_moved_flag()

    def animals(self) -> list['Animal']:
        """Returns a snapshot of all currently registered animals."""
        return [cell for row in self.grid for cell in row if isinstance(cell, Animal)]

    def size(self) -> int:
        """Returns the island's width and height."""
        return self.grid_size

    def register(self, animal: 'Animal') -> None:
        """Places an animal at its current coordinates."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: 'Animal') -> None:
        """Removes an animal if it still occupies its recorded position."""
        if self.animal(animal.x, animal.y) is animal:
            self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> 'Animal | int':
        """Returns a cell occupant, or -1 when coordinates are out of bounds."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        """Renders the grid with its origin at the lower left."""
        return '\n'.join(' '.join(str(self.grid[x][y]) if self.grid[x][y] else '.'
                                   for x in range(self.grid_size))
                         for y in range(self.grid_size - 1, -1, -1))

    def count_prey(self) -> int:
        """Returns the number of living prey."""
        return sum(type(a) is Prey for a in self.animals())

    def count_predators(self) -> int:
        """Return the number of predators, excluding humans."""
        return sum(type(a) is Predator for a in self.animals())

    def count_humans(self) -> int:
        """Returns the number of living humans."""
        return sum(isinstance(a, Human) for a in self.animals())


class Animal:
    """A character capable of movement and reproduction."""

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'A') -> None:
        """Stores the animal's island, coordinates, and display symbol."""
        self.island = island
        self.name = s
        self.x = x
        self.y = y
        self.moved = False

    def position(self) -> tuple[int, int]:
        """Returns the animal's current coordinates."""
        return self.x, self.y

    def __str__(self) -> str:
        """Returns the animal's one-character display symbol."""
        return self.name

    def check_grid(self, type_looking_for: type = int) -> 'tuple[int, int] | int':
        """Finds the first neighboring cell containing the requested type."""
        offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0),
                   (-1, -1), (0, -1), (1, -1)]
        for dx, dy in offsets:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < self.island.size() and 0 <= y < self.island.size():
                if type(self.island.animal(x, y)) is type_looking_for:
                    return x, y
        return 0

    def move(self) -> None:
        """Moves once per tick into the first available neighboring cell."""
        if not self.moved:
            location = self.check_grid(int)
            if location:
                self.island.remove(self)
                self.x, self.y = location
                self.island.register(self)
                self.moved = True

    def breed(self) -> None:
        """Creates an offspring in an empty neighbor when breeding is due."""
        if self.breed_clock <= 0:
            location = self.check_grid(int)
            if location:
                self.breed_clock = self.breed_time
                self.island.register(type(self)(self.island, *location))

    def clear_moved_flag(self) -> None:
        """Resets movement eligibility for the next tick."""
        self.moved = False


class Prey(Animal):
    """An animal that moves and breeds without hunting."""
    breed_time: int = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'O') -> None:
        """Initializes prey and its breeding clock."""
        super().__init__(island, x, y, s)
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Decreases the prey's breeding countdown by one."""
        self.breed_clock -= 1


class Predator(Animal):
    """An animal that hunts prey and can breed or starve."""
    breed_time: int = 6
    starve_time: int = 3
    food_type: type = Prey

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'X') -> None:
        """Initializes a hunter with breeding and starvation clocks."""
        super().__init__(island, x, y, s)
        self.starve_clock = self.starve_time
        self.breed_clock = self.breed_time

    def clock_tick(self) -> None:
        """Advances both clocks and removes this hunter if it starves."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Consumes adjacent food, move into its cell, and reset starvation."""
        if not self.moved:
            location = self.check_grid(self.food_type)
            if location:
                victim = self.island.animal(*location)
                self.island.remove(victim)
                self.island.remove(self)
                self.x, self.y = location
                self.island.register(self)
                self.starve_clock = self.starve_time
                self.moved = True


# Human class: inherits hunting, movement, breeding, and starvation behavior.
class Human(Predator):
    """A hunter of predators that does not eat prey."""
    breed_time: int = 8
    starve_time: int = 5
    food_type: type = Predator

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 s: str = 'H') -> None:
        """Initializes a human with independent breed and starvation clocks."""
        super().__init__(island, x, y, s)


def main(predator_breed_time: int = 6, predator_starve_time: int = 3,
         initial_predators: int = 10, prey_breed_time: int = 3,
         initial_prey: int = 50, size: int = 10, ticks: int = 1000,
         human_breed_time: int = 4, human_starve_time: int = 12,
         initial_humans: int = 10) -> None:
    """Simulates up to 1000 ticks or until all populations become constant."""
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time

    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print('Initial island:')
    print(isle)

    populations = [(isle.count_prey(), isle.count_predators(), isle.count_humans())]
    stable_ticks = 0
    for tick in range(1, min(ticks, 1000) + 1):
        isle.clear_all_moved_flags()
        # Snapshot ensures offspring do not act during the tick of their birth.
        for animal in isle.animals():
            if isle.animal(*animal.position()) is not animal:
                continue
            if isinstance(animal, Predator):
                animal.eat()
            animal.move()
            animal.breed()
            animal.clock_tick()

        counts = (isle.count_prey(), isle.count_predators(), isle.count_humans())
        populations.append(counts)
        stable_ticks = stable_ticks + 1 if counts == populations[-2] else 0
        if tick % 10 == 0:
            print(f'Tick {tick}: Prey={counts[0]}, Predator={counts[1]}, Human={counts[2]}')
        # A sustained constant population is treated as convergence.
        if stable_ticks >= 20:
            print(f'Populations remained constant for 20 ticks; stopping at tick {tick}.')
            break

    print('\nFinal island:')
    print(isle)
    print(f'Final populations: Prey={counts[0]}, Predator={counts[1]}, Human={counts[2]}')
    times = range(len(populations))
    plt.plot(times, [p[0] for p in populations], label='Prey')
    plt.plot(times, [p[1] for p in populations], label='Predator')
    plt.plot(times, [p[2] for p in populations], label='Human')
    plt.xlabel('Time (ticks)')
    plt.ylabel('Population')
    plt.title('Prey, Predator, and Human Populations Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()