from collections import deque
from itertools import product

#  --- Données de base ---
jours = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
creneaux = {
    "Sunday": [1, 2, 3, 4, 5],
    "Monday": [1, 2, 3, 4, 5],
    "Tuesday": [1, 2, 3],
    "Wednesday": [1, 2, 3, 4, 5],
    "Thursday": [1, 2, 3, 4, 5],
}

# Créneaux valides (jour, slot)
slots = [(j, s) for j in jours for s in creneaux[j]]

# Variables (cours, TD, TP)
variables = [
    "SEC_LEC", "SEC_TD", "MF_LEC", "MF_TD", "ANUM_LEC", "ANUM_TD",
    "ENT_LEC", "RO2_LEC", "RO2_TD", "DAIC_LEC", "DAIC_TD",
    "RES2_LEC", "RES2_TD", "RES2_TP", "AI_LEC", "AI_TD", "AI_TP"
]

# Domaine initial : tous les créneaux
domains = {var: slots.copy() for var in variables}

# Contraintes : cours != TD au même créneau
same_course_pairs = [
    ("SEC_LEC", "SEC_TD"),
    ("MF_LEC", "MF_TD"),
    ("ANUM_LEC", "ANUM_TD"),
    ("RO2_LEC", "RO2_TD"),
    ("DAIC_LEC", "DAIC_TD"),
    ("RES2_LEC", "RES2_TD"),
    ("AI_LEC", "AI_TD"),
]

# Fonction : plus de 3 créneaux consécutifs 
def has_more_than_3_consecutive(day_slots):
    slots = sorted([slot for (day, slot) in day_slots])
    count = 1
    for i in range(1, len(slots)):
        if slots[i] == slots[i-1] + 1:
            count += 1
            if count > 3:
                return True
        else:
            count = 1
    return False

# Fonction : test de validité
def is_valid(var, value, assignment):
    # 1. Pas de créneau déjà pris
    for other_var, other_val in assignment.items():
        if value == other_val:
            return False

    # 2. Pas cours et TD du même module en même temps
    for (a, b) in same_course_pairs:
        if (var == a and b in assignment and assignment[b] == value) or \
           (var == b and a in assignment and assignment[a] == value):
            return False

    # 3. Pas plus de 3 slots consécutifs (verification)
    day_slots = [(assignment[k][0], assignment[k][1]) for k in assignment] + [value]
    day_groups = {}
    for d, s in day_slots:
        if d not in day_groups:
            day_groups[d] = []
        day_groups[d].append((d, s))

    for slots_in_day in day_groups.values():
        if has_more_than_3_consecutive(slots_in_day):
            return False

    return True

# --- AC3 Algorithm ---
def AC3(domains, variables):
    queue = deque()
    for var1 in variables:
        for var2 in variables:
            if var1 != var2:
                queue.append((var1, var2))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in variables:
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    revised = False
    to_remove = []
    for x in domains[xi]:
        # Si aucun y dans domaine[xj] compatible avec x, on l'enlève
        if all(x == y for y in domains[xj]):
            to_remove.append(x)
            revised = True
    for x in to_remove:
        domains[xi].remove(x)
    return revised

# --- Backtracking + Most remaning value : MRV ---
def backtrack(assignment, domains):
    if len(assignment) == len(variables):
        return assignment

    # MRV: variable avec le plus petit domaine
    unassigned = [v for v in variables if v not in assignment]
    var = min(unassigned, key=lambda v: len(domains[v]))

    for value in domains[var]:
        if is_valid(var, value, assignment):
            assignment[var] = value
            result = backtrack(assignment, domains)
            if result:
                return result
            del assignment[var]

    return None

# --- Résolution complète ---
def solve_timetable():
    local_domains = {var: domains[var][:] for var in variables}
    if not AC3(local_domains, variables):
        print("AC3 a détecté un domaine vide. Aucune solution.")
        return None
    print("AC3 terminé. Début du backtracking...")
    solution = backtrack({}, local_domains)
    return solution

# --- Lancer le solveur ---
if __name__ == "__main__":
    solution = solve_timetable()
    if solution:
        print("\n Solution trouvée :\n")
        for var in sorted(solution):
            print(f"{var:<10} → {solution[var]}")
    else:
        print("Aucune solution possible.")
