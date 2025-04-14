import tkinter as tk
from timetable_csp import solve_timetable

# Configuration de la grille
jours = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
creneaux = [1, 2, 3, 4, 5]

CELL_WIDTH = 150
CELL_HEIGHT = 60
PADDING = 5

def draw_timetable(solution):
    root = tk.Tk()
    root.title("Emploi du temps S2 - 1CS")

    canvas = tk.Canvas(root, width=(len(jours)+1)*CELL_WIDTH, height=(len(creneaux)+1)*CELL_HEIGHT)
    canvas.pack()

    # En-tête jours
    for i, jour in enumerate(jours):
        x = (i+1) * CELL_WIDTH
        canvas.create_rectangle(x, 0, x + CELL_WIDTH, CELL_HEIGHT, fill="lightblue")
        canvas.create_text(x + CELL_WIDTH//2, CELL_HEIGHT//2, text=jour, font=("Arial", 12, "bold"))

    # En-tête créneaux
    for j, slot in enumerate(creneaux):
        y = (j+1) * CELL_HEIGHT
        canvas.create_rectangle(0, y, CELL_WIDTH, y + CELL_HEIGHT, fill="lightgrey")
        canvas.create_text(CELL_WIDTH//2, y + CELL_HEIGHT//2, text=f"Slot {slot}", font=("Arial", 12, "bold"))

    # Placement des cours
    for var, (day, slot) in solution.items():
        try:
            i = jours.index(day)
            j = slot - 1
        except ValueError:
            continue

        x = (i+1) * CELL_WIDTH
        y = (j+1) * CELL_HEIGHT

        canvas.create_rectangle(x, y, x + CELL_WIDTH, y + CELL_HEIGHT, fill="lightgreen")
        canvas.create_text(x + CELL_WIDTH//2, y + CELL_HEIGHT//2, text=var, font=("Arial", 10))

    root.mainloop()

if __name__ == "__main__":
    timetable = solve_timetable()
    if timetable:
        draw_timetable(timetable)
    else:
        print("Aucune solution trouvée.")
