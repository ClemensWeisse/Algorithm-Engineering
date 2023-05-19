import sys


def check_file(vrp_file: str, sol_file: str):
    # vrp- file
    with open(vrp_file, 'r') as f:
        data: str = f.read()
        lines = data.splitlines()
        dimensions = int((lines[3].split(":"))[1].strip())
        capacity: int
        for line in lines:
            if line.find("CAPACITY") != -1:
                capacity = int(line.split(":")[1].strip())
                break
        demand_lines = (data.split("DEMAND_SECTION")[1].split("DEPOT_SECTION")[0]).strip().splitlines()
        customers_demand = dict()
        for line in demand_lines:
            customer: int = int(line.split()[0])
            demand: int = int(line.split()[1])
            customers_demand[customer] = demand

    # sol-file
    with open(sol_file, 'r') as f:
        data = f.read()
        lines = data.splitlines()
        cost_str = lines.pop()
        route_number = 1
        route: [int]
        set_of_customers: set = set()
        list_of_customers: list = []
        for line in lines:
            pre_part = line.split("Route #" + str(route_number) + ": ")
            numbers = pre_part[1].split()
            route = list(map(int, numbers))
            sum = 0
            for num in route:
                assert num != 0, "depot was visited before the end of the tour (0 in sol-file)"
                assert dimensions >= num + 1 and num >= 1, \
                    "there was a customer visited that should not be visited\n" \
                    + "(there is a number of a customer in the sol-file that is not in the vrp-file)"
                sum += customers_demand[num + 1]
            # Sum of DEMAND cannot exceed CAPACITY
            assert sum <= capacity, "Route #" + str(route_number) + " is exceeding the capacity"

            set_of_customers = set_of_customers.union(set(map(int, numbers)))
            list_of_customers.extend(route)
            route_number += 1

    # Every point is exactly one time visited
    # Exactly DIMENSIONS - 1 many points
    assert (dimensions - 1) == len(set_of_customers), "at least one customer is not visited"
    assert (dimensions - 1) == len(list_of_customers), "at least one customer is visited more than once"

    # Format checks? "Route #x:"... Cost y
    # Checking for fixed edges???
    return "VALID"


if __name__ == "__main__":
    print(check_file(sys.argv[1], sys.argv[2]))
