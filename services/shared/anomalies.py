from statistics import median


def review_cases(records, key="value"):
    values = [float(item[key]) for item in records if item.get(key) is not None]
    if len(values) < 4:
        return []
    ordered = sorted(values)
    q1, q3 = ordered[len(ordered) // 4], ordered[(3 * len(ordered)) // 4]
    iqr = q3 - q1
    center = median(values)
    deviations = [abs(value - center) for value in values]
    mad = median(deviations) or 1.0
    cases = []
    seen = set()
    for item in records:
        value = item.get(key)
        subject = str(item.get("id", ""))
        duplicate = subject in seen
        seen.add(subject)
        score = abs(float(value) - center) / (1.4826 * mad) if value is not None else None
        reasons = []
        if value is not None and (float(value) < q1 - 1.5 * iqr or float(value) > q3 + 1.5 * iqr):
            reasons.append("fuera del intervalo IQR")
        if score is not None and score > 3.5:
            reasons.append("z-score robusto superior a 3,5")
        if duplicate:
            reasons.append("identificador duplicado")
        if reasons:
            cases.append({"subject_key": subject, "observed_value": value, "score": score,
                          "method": "IQR+z-score robusto+duplicados", "label": "caso para revisar",
                          "explanation": "; ".join(reasons), "result_kind": "calculated"})
    return cases
