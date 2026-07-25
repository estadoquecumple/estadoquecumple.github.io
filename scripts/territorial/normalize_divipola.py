from common import normalize_divipola

def run():
    cases = [("5","municipality","00005"),("05001","municipality","05001"),("5","department","05")]
    for raw, level, expected in cases:
        assert normalize_divipola(raw, level) == expected
    print("DIVIPOLA: normalización verificada")

if __name__ == "__main__": run()
