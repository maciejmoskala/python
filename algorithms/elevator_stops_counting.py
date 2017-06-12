def count_elevator_stops(people_weights, people_floores, M, max_people, max_weight):
    people_count = 0
    weight_count = 0
    floores = []
    solution = 0

    for person_weight, person_floor in zip(people_weights, people_floores):
        if weight_count+person_weight<=max_weight and people_count<max_people:
            if person_floor not in floores:
                floores.append(person_floor)
            weight_count += person_weight
            people_count += 1
        else:
            solution += len(floores)+1
            floores = [person_floor]
            weight_count = person_weight
            people_count = 1
    return solution + len(floores)+1

people_weights = [40, 40, 100, 80, 20]
people_floores = [3, 3, 2, 2, 3]
M = 3
max_people = 5
max_weight = 200

count = count_elevator_stops(people_weights, people_floores, M, max_people, max_weight)
print("Elevator stopped {0} times.".format(count))
