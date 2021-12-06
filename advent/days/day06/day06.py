def part1(lines: list[str]) -> int:
    swarm = convert(lines[0])
    return sum(age(swarm, 80))


def part2(lines: list[str]) -> int:
    swarm = convert(lines[0])
    return sum(age(swarm, 256))


def convert(line: str) -> list[int]:
    ages = [int(num) for num in line.split(",")]
    swarm = [0] * 9
    for age in range(9):
        swarm[age] = len([f for f in ages if f == age])
    return swarm


def age(swarm: list[int], days: int = 1):
    for _ in range(days):
        aged = swarm[1:]
        aged += [swarm[0]]
        aged[6] += swarm[0]
        swarm = aged
    return swarm
