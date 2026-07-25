from common import ROOT, PUBLIC, read_json, write_json
def run():
    for path in (ROOT/"data"/"scenarios").glob("*.json"):
        write_json(PUBLIC/"scenarios"/path.name, read_json(path))
    print("Escenarios: 3 configuraciones publicadas")
if __name__=="__main__": run()
