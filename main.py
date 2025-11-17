import os
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

# ------------------ FastAPI app ------------------
app = FastAPI(title="Timetabling API")

# ------------------ CORS ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes cambiar a tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Función de timetabling ------------------
def solve_timetabling(data):

    columnas_empleados = ["employee", "cost_hour"]
    datos_empleados = [
        ["Ana", 120],
        ["Luis", 100],
        ["Sara", 110],
        ["Pedro", 105],
    ]

    columnas_turnos = ["turno", "inicio", "fin", "comida", "nocturno"]
    datos_turnos = [
        ["T1", 6, 15, 12, 0],
        ["T2", 9, 18, 14, 0],
        ["T3", 14, 23, 19, 0],
        ["T4", 22, 7, 3, 1],
    ]

    datos_demanda = [
    [0, 0, 100],[0, 1, 100],[0, 2, 100],[0, 3, 100],[0, 4, 100],
    [0, 5, 100],[0, 6, 100],[0, 7, 50],[0, 8, 50],[0, 9, 50],
    [0, 10, 50],[0, 11, 50],[0, 12, 80],[0, 13, 80],[0, 14, 80],
    [0, 15, 50],[0, 16, 50],[0, 17, 50],[0, 18, 80],[0, 19, 80],
    [0, 20, 80],[0, 21, 50],[0, 22, 50],[0, 23, 100],[1, 0, 50],
    [1, 1, 50],[1, 2, 50],[1, 3, 50],[1, 4, 50],[1, 5, 50],
    [1, 6, 50],[1, 7, 50],[1, 8, 50],[1, 9, 50],[1, 10, 50],
    [1, 11, 50],[1, 12, 80],[1, 13, 80],[1, 14, 80],[1, 15, 50],
    [1, 16, 50],[1, 17, 50],[1, 18, 80],[1, 19, 80],[1, 20, 80],
    [1, 21, 50],[1, 22, 50],[1, 23, 50],[2, 0, 50],[2, 1, 50],
    [2, 2, 50],
    [2, 3, 50],
    [2, 4, 50],
    [2, 5, 50],
    [2, 6, 50],
    [2, 7, 50],
    [2, 8, 50],
    [2, 9, 50],
    [2, 10, 50],
    [2, 11, 50],
    [2, 12, 80],
    [2, 13, 80],
    [2, 14, 80],
    [2, 15, 50],
    [2, 16, 50],
    [2, 17, 50],
    [2, 18, 80],
    [2, 19, 80],
    [2, 20, 80],
    [2, 21, 50],
    [2, 22, 50],
    [2, 23, 50],
    [3, 0, 50],
    [3, 1, 50],
    [3, 2, 50],
    [3, 3, 50],
    [3, 4, 50],
    [3, 5, 50],
    [3, 6, 50],
    [3, 7, 50],
    [3, 8, 50],
    [3, 9, 50],
    [3, 10, 50],
    [3, 11, 50],
    [3, 12, 80],
    [3, 13, 80],
    [3, 14, 80],
    [3, 15, 50],
    [3, 16, 50],
    [3, 17, 50],
    [3, 18, 80],
    [3, 19, 80],
    [3, 20, 80],
    [3, 21, 50],
    [3, 22, 50],
    [3, 23, 50],
    [4, 0, 50],
    [4, 1, 50],
    [4, 2, 50],
    [4, 3, 50],
    [4, 4, 50],
    [4, 5, 50],
    [4, 6, 50],
    [4, 7, 50],
    [4, 8, 50],
    [4, 9, 50],
    [4, 10, 50],
    [4, 11, 50],
    [4, 12, 80],
    [4, 13, 80],
    [4, 14, 80],
    [4, 15, 50],
    [4, 16, 50],
    [4, 17, 50],
    [4, 18, 80],
    [4, 19, 80],
    [4, 20, 80],
    [4, 21, 50],
    [4, 22, 50],
    [4, 23, 50],
    [5, 0, 50],
    [5, 1, 50],
    [5, 2, 50],
    [5, 3, 50],
    [5, 4, 50],
    [5, 5, 50],
    [5, 6, 50],
    [5, 7, 50],
    [5, 8, 50],
    [5, 9, 50],
    [5, 10, 50],
    [5, 11, 50],
    [5, 12, 80],
    [5, 13, 80],
    [5, 14, 80],
    [5, 15, 50],
    [5, 16, 50],
    [5, 17, 50],
    [5, 18, 80],
    [5, 19, 80],
    [5, 20, 80],
    [5, 21, 50],
    [5, 22, 50],
    [5, 23, 50],
    [6, 0, 50],
    [6, 1, 50],
    [6, 2, 50],
    [6, 3, 50],
    [6, 4, 50],
    [6, 5, 50],
    [6, 6, 50],
    [6, 7, 50],
    [6, 8, 50],
    [6, 9, 50],
    [6, 10, 50],
    [6, 11, 50],
    [6, 12, 80],
    [6, 13, 80],
    [6, 14, 80],
    [6, 15, 50],
    [6, 16, 50],
    [6, 17, 50],
    [6, 18, 80],
    [6, 19, 80],
    [6, 20, 80],
    [6, 21, 50],
    [6, 22, 50],
    [6, 23, 50],
]

    columnas_demanda = ["dia", "hora", "afluencia"]

    employees_df = pd.DataFrame(datos_empleados, columns=columnas_empleados)
    shifts_df = pd.DataFrame(datos_turnos, columns=columnas_turnos)
    demand_df = pd.DataFrame(datos_demanda, columns=columnas_demanda)

    EMPLOYEES = employees_df['employee'].tolist()
    t_cost = {row['employee']: row['cost_hour'] for _, row in employees_df.iterrows()}
    DAYS = sorted(demand_df['dia'].unique())
    HOURS = sorted(demand_df['hora'].unique())

    SHIFTS = {}
    work_hours = {}
    NIGHT_SHIFTS = []
    for _, row in shifts_df.iterrows():
        s = row['turno']
        start = row['inicio']
        end = row['fin']
        lunch = row['comida']
        SHIFTS[s] = (start, end, lunch)
        hours = [(start + i) % 24 for i in range((end - start) % 24 or 24)]
        if lunch in hours:
            hours.remove(lunch)
        work_hours[s] = hours
        if row['nocturno'] == 1:
            NIGHT_SHIFTS.append(s)

    client_dem = {(int(r['hora']), int(r['dia'])): int(r['afluencia']) for _, r in demand_df.iterrows()}

    capacidad = 10
    lam = 10000
    w = {s: len(work_hours[s]) for s in SHIFTS}

    # Configuración de licencia Gurobi
    params = {
        "WLSACCESSID": '458bab2d-35d3-4a54-8418-9c25aa380dca',
        "WLSSECRET": '1a523d61-f8a2-4440-aea3-9f712e32d786',
        "LICENSEID": 2683271
    }
    
    env = gp.Env(params=params)

    # Modelo
    model = gp.Model(env=env)
    x = model.addVars(EMPLOYEES, SHIFTS, DAYS, vtype=GRB.BINARY, name='x')
    u = model.addVars(HOURS, DAYS, vtype=GRB.INTEGER, lb=0, name='u')
    z = model.addVars(EMPLOYEES, SHIFTS, vtype=GRB.BINARY, name='z')

    model.setObjective(
        gp.quicksum(t_cost[e] * w[s] * x[e, s, d] for e in EMPLOYEES for s in SHIFTS for d in DAYS)
        + lam * gp.quicksum(u[h, d] for h in HOURS for d in DAYS),
        GRB.MINIMIZE
    )

    # Restricciones
    for d in DAYS:
        for h in HOURS:
            cap = gp.quicksum(x[e, s, d] * capacidad for e in EMPLOYEES for s in SHIFTS if h in work_hours[s])
            model.addConstr(cap + u[h, d] >= client_dem.get((h, d), 0), name=f'cov_{h}_{d}')

    for e in EMPLOYEES:
        model.addConstr(gp.quicksum(x[e, s, d] * w[s] for s in SHIFTS for d in DAYS) == 48, name=f'week_hours_{e}')
        for d in DAYS:
            model.addConstr(gp.quicksum(x[e, s, d] for s in SHIFTS) <= 1, name=f'one_shift_{e}_{d}')
        model.addConstr(gp.quicksum(x[e, s, d] for s in SHIFTS for d in DAYS) <= 6, name=f'max_days_{e}')
        model.addConstr(gp.quicksum(z[e, s] for s in SHIFTS) == 1, name=f'consist_{e}')
        for s in SHIFTS:
            for d in DAYS:
                model.addConstr(x[e, s, d] <= z[e, s], name=f'link_{e}_{s}_{d}')

    model.optimize()

    # Extraer resultados
    rows = []
    for (empleado, turno, dia), var in x.items():
        if var.X > 0.5:
            rows.append({'Empleado': empleado, 'Turno': turno, 'Dia': dia})

    df = pd.DataFrame(rows)
    gantt_rows = []
    for _, row in df.iterrows():
        turno = row['Turno']
        dia = row['Dia']
        empleado = row['Empleado']
        start_hour, end_hour, lunch = SHIFTS[turno]
        gantt_rows.append({
            'Empleado': empleado,
            'Turno': turno,
            'Dia': dia,
            'Inicio': start_hour,
            'Fin': end_hour,
            'Costo': t_cost[empleado]
        })

    return {"timetable": gantt_rows}

# ------------------ Endpoint FastAPI ------------------
@app.post("/solve")
async def solve_endpoint(payload: dict = Body(...)):
    """
    Endpoint para resolver el timetabling.
    """
    result = solve_timetabling(payload)
    return result

# ------------------ Run Uvicorn ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
