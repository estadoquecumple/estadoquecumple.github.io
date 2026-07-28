import hashlib
import json
import re
from abc import ABC, abstractmethod
from pathlib import Path

SAFE = re.compile(r"^[a-zA-Z0-9._-]+$")

class VaultProvider(ABC):
    @abstractmethod
    def put(self, source: str, snapshot: str, filename: str, content: bytes) -> dict: ...
    @abstractmethod
    def verify(self, relative_path: str) -> bool: ...

class LocalFilesystemVault(VaultProvider):
    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
    def put(self, source: str, snapshot: str, filename: str, content: bytes) -> dict:
        if not all(SAFE.fullmatch(part) for part in (source, snapshot, filename)):
            raise ValueError("Nombre de bóveda inválido")
        digest = hashlib.sha256(content).hexdigest()
        directory = (self.root / source / snapshot / digest).resolve()
        if self.root not in directory.parents:
            raise ValueError("Ruta fuera de la bóveda")
        target = directory / "original"
        metadata = directory / "metadata.json"
        directory.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != content:
            raise FileExistsError("Un original inmutable no puede sobrescribirse")
        if not target.exists():
            target.write_bytes(content)
            metadata.write_text(json.dumps({"sha256": digest, "filename": filename, "size": len(content)}), encoding="utf-8")
        return {"path": str(target.relative_to(self.root)).replace("\\", "/"), "sha256": digest, "size": len(content)}
    def verify(self, relative_path: str) -> bool:
        target = (self.root / relative_path).resolve()
        if self.root not in target.parents or target.name != "original":
            return False
        meta = json.loads((target.parent / "metadata.json").read_text(encoding="utf-8"))
        return hashlib.sha256(target.read_bytes()).hexdigest() == meta["sha256"]
