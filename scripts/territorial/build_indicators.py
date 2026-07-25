from common import PUBLIC, read_json, write_json, now
def run():
    sources=[]
    for path in sorted((PUBLIC/"indicators").glob("*.json")):
        doc=read_json(path); sources.append({"id":doc.get("source"),"status":doc.get("status"),"file":path.name,"records":len(doc.get("records",[]))})
    write_json(PUBLIC/"indicators"/"index.json",{"version":"1.0.0","generatedAt":now(),"sources":sources})
    print(f"Indicadores: {len(sources)} fuentes indexadas")
if __name__=="__main__": run()
