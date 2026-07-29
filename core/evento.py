from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Evento:
    descripcion: str
    area: str
    proceso: str
    fecha: datetime
    consecuencias: str
    tipo: str  # "accidente", "incidente", "falla_equipo", "calidad", "ambiental", "otro"
    reportado_por: str
    turno: Optional[str] = None
    equipos_involucrados: list[str] = field(default_factory=list)
    personas_involucradas: int = 0

    def resumen(self) -> str:
        return (
            f"Evento: {self.descripcion}\n"
            f"Área/Proceso: {self.area} / {self.proceso}\n"
            f"Fecha: {self.fecha.strftime('%d/%m/%Y %H:%M')}\n"
            f"Turno: {self.turno or 'No especificado'}\n"
            f"Tipo: {self.tipo.replace('_', ' ').title()}\n"
            f"Consecuencias: {self.consecuencias}\n"
            f"Reportado por: {self.reportado_por}"
        )
