class MemoryDedupe:
    def __init__(self) -> None:
        self._seen: set[str] = set()

    def claim(self, key: str) -> bool:
        if key in self._seen:
            return False
        
        self._seen.add(key)
        return True
    
        