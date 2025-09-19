from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ItemDataclass:
    nome: str
    valor: float
    peso: float

    def ratio_valor_peso(self) -> float:
        if self.peso == 0:
            return float('inf')
        return self.valor / self.peso
    
class ItensPreDefinidos:
    """Classe para gerenciar os 15 itens da tabela"""
    
    _dados_itens = [
        ("Item 1", 60, 10),   ("Item 2", 100, 20),  ("Item 3", 120, 30),
        ("Item 4", 90, 15),   ("Item 5", 30, 5),    ("Item 6", 70, 12),
        ("Item 7", 40, 7),    ("Item 8", 160, 25),  ("Item 9", 20, 3),
        ("Item 10", 50, 9),   ("Item 11", 110, 18), ("Item 12", 85, 14),
        ("Item 13", 95, 16),  ("Item 14", 200, 28), ("Item 15", 55, 6)
    ]
    
    _itens_criados: Optional[List[ItemDataclass]] = None
    
    @classmethod
    def obter_todos_itens(cls) -> List[ItemDataclass]:
        if cls._itens_criados is None:
            cls._criar_itens()
        return cls._itens_criados.copy()

    @classmethod
    def _criar_itens(cls):
        """Cria os itens uma única vez"""
        cls._itens_criados = []
        for nome, valor, peso in cls._dados_itens:
            item = ItemDataclass(nome, valor, peso)
            cls._itens_criados.append(item)
