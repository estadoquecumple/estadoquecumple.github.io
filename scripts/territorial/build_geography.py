from common import PUBLIC, read_json
def run():
    manifest=read_json(PUBLIC/"geography"/"geography-manifest.json")
    assert manifest["municipalityCount"] > 1000 and manifest["departmentCount"] >= 32
    print("Geografía: manifiesto y cobertura nacional verificados")
if __name__=="__main__": run()
