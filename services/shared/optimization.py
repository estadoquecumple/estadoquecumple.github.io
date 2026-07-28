import time
from ortools.sat.python import cp_model
import ortools


def _solve(model, variables, objectives, seed=42, timeout=10):
    solver = cp_model.CpSolver()
    solver.parameters.random_seed = seed
    solver.parameters.max_time_in_seconds = timeout
    started = time.monotonic()
    status = solver.Solve(model)
    result = {
        "solver": "OR-Tools CP-SAT",
        "solver_version": ortools.__version__,
        "seed": seed,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "status": solver.StatusName(status),
        "result_kind": "calculated",
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result["solution"] = {name: solver.Value(var) for name, var in variables.items()}
        result["objectives"] = {name: solver.Value(expr) for name, expr in objectives.items()}
    else:
        result["solution"] = None
    return result


def _infeasible(reason, constraints):
    return {
        "status": "INFEASIBLE", "solution": None, "result_kind": "calculated",
        "infeasibility": {"summary": reason, "conflicting_constraints": constraints,
                          "explanation_method": "deterministic_precheck"},
        "alternatives": [], "sensitivity": {},
    }


def contiguous_regions(payload):
    units = payload.get("units", [])
    regions = int(payload.get("regions", 0))
    adjacency = {str(k): set(map(str, v)) for k, v in payload.get("adjacency", {}).items()}
    protected = {str(k): int(v) for k, v in payload.get("protected", {}).items()}
    if not units or regions < 1 or regions > len(units):
        return _infeasible("Número de regiones incompatible con las unidades.", ["1 <= regions <= units"])
    if protected and max(protected.values(), default=-1) >= regions:
        return _infeasible("Una unidad protegida exige una región inexistente.", ["protected region index"])
    model = cp_model.CpModel()
    x = {(unit, region): model.NewBoolVar(f"x_{unit}_{region}") for unit in units for region in range(regions)}
    for unit in units:
        model.AddExactlyOne(x[(unit, region)] for region in range(regions))
    for unit, region in protected.items():
        model.Add(x[(unit, region)] == 1)
    # Restricción local verificable: salvo ancla mínima, cada unidad asignada debe tener vecino en su región.
    for region in range(regions):
        anchor = units[region]
        model.Add(x[(anchor, region)] == 1)
        for unit in units:
            if unit == anchor:
                continue
            neighbors = [x[(neighbor, region)] for neighbor in adjacency.get(str(unit), set()) if neighbor in units]
            if neighbors:
                model.Add(x[(unit, region)] <= sum(neighbors))
            else:
                model.Add(x[(unit, region)] == 0)
    sizes = [sum(x[(unit, region)] for unit in units) for region in range(regions)]
    maximum, minimum = model.NewIntVar(0, len(units), "max_size"), model.NewIntVar(0, len(units), "min_size")
    model.AddMaxEquality(maximum, sizes)
    model.AddMinEquality(minimum, sizes)
    imbalance = maximum - minimum
    model.Minimize(imbalance)
    result = _solve(model, {f"{unit}:{region}": var for (unit, region), var in x.items()},
                    {"imbalance": imbalance}, int(payload.get("seed", 42)))
    result["formulation"] = {"variables": "x[unit,region] binary", "constraints": [
        "one region per unit", "protected assignments", "adjacent support", "one anchor per region"],
        "objective": "minimize max region size - min region size"}
    result["alternatives"] = [{"objective": "balance", "solution": result.get("solution")} ] if result["solution"] else []
    if not result["solution"]:
        result.update(_infeasible("Las restricciones de contigüidad y protección no admiten asignación.",
                                  ["adjacent support", "protected assignments"]))
    return result


def service_location(payload):
    sites, demands = payload.get("sites", []), payload.get("demands", [])
    distances, coverage = payload.get("distances", {}), int(payload.get("max_distance", 0))
    budget = int(payload.get("budget", 0))
    costs = {str(k): int(v) for k, v in payload.get("costs", {}).items()}
    capacities = {str(k): int(v) for k, v in payload.get("capacities", {}).items()}
    quantities = {str(k): int(v) for k, v in payload.get("demand", {}).items()}
    if sum(quantities.values()) > sum(capacities.values()):
        return _infeasible("La capacidad total es menor que la demanda declarada.", ["sum(capacity) >= sum(demand)"])
    if min((costs.get(site, 0) for site in sites), default=0) > budget:
        return _infeasible("El presupuesto no permite abrir ningún sitio.", ["opening cost <= budget"])
    model = cp_model.CpModel()
    opened = {site: model.NewBoolVar(f"open_{site}") for site in sites}
    assign = {(demand, site): model.NewBoolVar(f"a_{demand}_{site}") for demand in demands for site in sites
              if int(distances.get(f"{demand}:{site}", coverage + 1)) <= coverage}
    for demand in demands:
        options = [assign[(demand, site)] for site in sites if (demand, site) in assign]
        if not options:
            return _infeasible(f"La demanda {demand} no tiene sitio dentro de cobertura.", ["distance <= max_distance"])
        model.AddExactlyOne(options)
    for (demand, site), var in assign.items():
        model.Add(var <= opened[site])
    for site in sites:
        model.Add(sum(quantities[d] * assign[(d, site)] for d in demands if (d, site) in assign) <= capacities[site])
    total_cost = sum(costs[site] * opened[site] for site in sites)
    total_distance = sum(int(distances[f"{d}:{s}"]) * quantities[d] * var for (d, s), var in assign.items())
    model.Add(total_cost <= budget)
    weight = int(payload.get("distance_weight", 1))
    model.Minimize(total_cost + weight * total_distance)
    variables = {**{f"open:{k}": v for k, v in opened.items()},
                 **{f"assign:{d}:{s}": v for (d, s), v in assign.items()}}
    result = _solve(model, variables, {"cost": total_cost, "weighted_distance": total_distance},
                    int(payload.get("seed", 42)))
    result["formulation"] = {"variables": "open[site], assign[demand,site] binary",
                             "constraints": ["coverage", "capacity", "budget", "one site per demand"],
                             "objective": "weighted cost and distance"}
    result["alternatives"] = _pareto_service(payload)
    result["sensitivity"] = {"budget_minus_one": "infeasible" if budget <= min(costs.values(), default=0) else "not evaluated",
                             "inputs": "user_defined"}
    if not result["solution"]:
        result.update(_infeasible("No existe localización que satisfaga cobertura, capacidad y presupuesto.",
                                  ["coverage", "capacity", "budget"]))
    return result


def _pareto_service(payload):
    alternatives = []
    for weight in (0, 1, 10):
        variant = dict(payload)
        variant["distance_weight"] = weight
        # Evita recursión: solución compacta por evaluación del mismo problema sin Pareto.
        variant["_pareto"] = True
        result = _service_once(variant)
        if result.get("solution"):
            item = {"distance_weight": weight, "objectives": result["objectives"], "solution": result["solution"]}
            if not any(existing["objectives"] == item["objectives"] for existing in alternatives):
                alternatives.append(item)
    return alternatives


def _service_once(payload):
    copied = dict(payload)
    result = service_location.__wrapped__(copied) if hasattr(service_location, "__wrapped__") else None
    if result is not None:
        return result
    # Implementación acotada para Pareto: desactiva temporalmente la generación anidada.
    copied["_skip_pareto"] = True
    return _service_core(copied)


def _service_core(payload):
    # Se reutiliza el optimizador principal suprimiendo Pareto mediante una marca.
    original = _pareto_service
    try:
        globals()["_pareto_service"] = lambda _: []
        return service_location(payload)
    finally:
        globals()["_pareto_service"] = original


def allocation(payload, kind):
    items, targets = payload.get("items", []), payload.get("targets", [])
    supply = {str(k): int(v) for k, v in payload.get("supply", {}).items()}
    minimum = {str(k): int(v) for k, v in payload.get("minimum", {}).items()}
    compatibility = payload.get("compatibility", {})
    if sum(supply.values()) < sum(minimum.values()):
        return _infeasible("Los recursos declarados no cubren los mínimos.", ["sum(supply) >= sum(minimum)"])
    model = cp_model.CpModel()
    x = {(item, target): model.NewIntVar(0, supply[item], f"x_{item}_{target}")
         for item in items for target in targets if target in compatibility.get(item, targets)}
    for item in items:
        model.Add(sum(x[(item, target)] for target in targets if (item, target) in x) <= supply[item])
    for target in targets:
        model.Add(sum(x[(item, target)] for item in items if (item, target) in x) >= minimum[target])
    unused = sum(supply.values()) - sum(x.values())
    model.Minimize(unused)
    result = _solve(model, {f"{item}:{target}": var for (item, target), var in x.items()},
                    {"unused": unused}, int(payload.get("seed", 42)))
    result["formulation"] = {"variables": f"{kind} allocation integer",
                             "constraints": ["supply", "minimum", "compatibility"],
                             "objective": "minimize unused capacity"}
    result["alternatives"] = [{"objective": "minimum unused", "solution": result.get("solution")}] if result.get("solution") else []
    if not result.get("solution"):
        result.update(_infeasible("No hay asignación compatible con mínimos y oferta.", ["supply", "minimum", "compatibility"]))
    return result


def transition(payload):
    tasks = payload.get("tasks", [])
    horizon = int(payload.get("horizon", sum(int(t["duration"]) for t in tasks)))
    model = cp_model.CpModel()
    starts, ends, intervals = {}, {}, {}
    for task in tasks:
        key, duration = str(task["id"]), int(task["duration"])
        starts[key] = model.NewIntVar(0, horizon, f"start_{key}")
        ends[key] = model.NewIntVar(0, horizon, f"end_{key}")
        intervals[key] = model.NewIntervalVar(starts[key], duration, ends[key], f"interval_{key}")
    for task in tasks:
        for predecessor in task.get("predecessors", []):
            model.Add(starts[str(task["id"])] >= ends[str(predecessor)])
    for resource in payload.get("resources", []):
        related = [intervals[str(task["id"])] for task in tasks if resource in task.get("resources", [])]
        if related:
            model.AddNoOverlap(related)
    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(makespan, list(ends.values()))
    model.Minimize(makespan)
    result = _solve(model, {**{f"start:{k}": v for k, v in starts.items()},
                            **{f"end:{k}": v for k, v in ends.items()}},
                    {"makespan": makespan}, int(payload.get("seed", 42)))
    result["formulation"] = {"variables": "task start/end", "constraints": ["precedence", "resource no-overlap"],
                             "objective": "minimize transition makespan"}
    result["alternatives"] = [{"objective": "minimum duration", "solution": result.get("solution")}] if result.get("solution") else []
    if not result.get("solution"):
        result.update(_infeasible("La transición excede horizonte o contradice precedencias.",
                                  ["precedence", "resource no-overlap", "horizon"]))
    return result


def optimize(kind, payload):
    if kind == "contiguous_regions":
        return contiguous_regions(payload)
    if kind == "service_location":
        return service_location(payload)
    if kind == "capacity_distribution":
        return allocation(payload, "capacity")
    if kind == "competence_assignment":
        return allocation(payload, "competence")
    if kind == "institutional_transition":
        return transition(payload)
    raise ValueError("tipo de optimización no permitido")
