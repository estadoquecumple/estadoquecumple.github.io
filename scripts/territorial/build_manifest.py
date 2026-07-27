from common import PUBLIC, now, sha256, write_json
def run():
    files=[]
    for path in sorted(PUBLIC.rglob("*")):
        if path.is_file() and path.name!="manifest.json":
            files.append({"path":path.relative_to(PUBLIC).as_posix(),"bytes":path.stat().st_size,"sha256":sha256(path)})
    write_json(PUBLIC/"manifest.json",{"version":"1.0.0","generatedAt":now(),"files":files,"contract":{"key":"DIVIPOLA","resultTypes":["observed","calculated","assumption"],"missing":"Sin dato disponible"}})
    print(f"Manifiesto: {len(files)} archivos")
if __name__=="__main__": run()
