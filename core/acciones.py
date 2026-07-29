from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


TIPOS_ACCION = {
    "correctiva": "Corregir la causa raíz identificada",
    "preventiva": "Evitar recurrencia en situaciones similares",
    "mitigacion": "Reducir el impacto si el evento se repite",
    "estandarizacion": "Estandarizar aprendizajes en procedimientos",
}

NIVELES_JERARQUIA = [
    "1. Eliminar el peligro/causa (más efectivo)",
    "2. Sustitución por alternativa más segura",
    "3. Controles de ingeniería",
    "4. Controles administrativos / procedimientos",
    "5. EPP / protección personal (menos efectivo)",
]


@dataclass
class AccionCorrectiva:
    descripcion: str
    tipo: str
    responsable: str
    fecha_limite: datetime
    causa_que_atiende: str
    nivel_jerarquia: int  # 1-5 según jerarquía de controles
    criterio_cierre: str
    recursos_necesarios: str = ""
    indicador_seguimiento: str = ""
    estado: str = "pendiente"  # pendiente, en_curso, cerrada, vencida
    fecha_cierre_real: Optional[datetime] = None
    evidencia_cierre: str = ""

    def es_smart(self) -> dict[str, bool]:
        return {
            "Específica": len(self.descripcion) > 20,
            "Medible": bool(self.criterio_cierre),
            "Asignable": bool(self.responsable),
            "Realista": bool(self.recursos_necesarios),
            "Con tiempo definido": self.fecha_limite is not None,
        }

    def __str__(self):
        smart = self.es_smart()
        smart_ok = all(smart.values())
        estado_smart = "✓ SMART" if smart_ok else "⚠ Revisar criterios SMART"
        return (
            f"  Acción: {self.descripcion}\n"
            f"  Tipo: {TIPOS_ACCION.get(self.tipo, self.tipo)}\n"
            f"  Atiende causa: {self.causa_que_atiende}\n"
            f"  Nivel de control: {NIVELES_JERARQUIA[self.nivel_jerarquia - 1]}\n"
            f"  Responsable: {self.responsable}\n"
            f"  Fecha límite: {self.fecha_limite.strftime('%d/%m/%Y')}\n"
            f"  Criterio de cierre: {self.criterio_cierre}\n"
            f"  Indicador: {self.indicador_seguimiento or 'No definido'}\n"
            f"  Estado: {self.estado.upper()} | {estado_smart}"
        )


@dataclass
class PlanAcciones:
    causas_raiz: list[str]
    acciones: list[AccionCorrectiva] = field(default_factory=list)
    lecciones_aprendidas: str = ""
    fecha_seguimiento: Optional[datetime] = None

    def agregar_accion(self, accion: AccionCorrectiva):
        self.acciones.append(accion)

    def acciones_por_tipo(self) -> dict[str, list[AccionCorrectiva]]:
        resultado = {t: [] for t in TIPOS_ACCION}
        for a in self.acciones:
            if a.tipo in resultado:
                resultado[a.tipo].append(a)
        return resultado

    def acciones_por_nivel(self) -> list[AccionCorrectiva]:
        return sorted(self.acciones, key=lambda a: a.nivel_jerarquia)

    def reporte(self) -> str:
        lineas = [
            "=" * 60,
            "PLAN DE ACCIONES CORRECTIVAS INTEGRALES",
            "=" * 60,
            "",
            "CAUSAS RAÍZ QUE SE ATIENDEN:",
        ]
        for i, causa in enumerate(self.causas_raiz, 1):
            lineas.append(f"  {i}. {causa}")

        lineas += [
            "",
            "ACCIONES (ordenadas por efectividad de control):",
            "-" * 40,
        ]

        for accion in self.acciones_por_nivel():
            lineas.append(str(accion))
            lineas.append("")

        por_tipo = self.acciones_por_tipo()
        lineas += [
            "-" * 40,
            "RESUMEN POR TIPO:",
        ]
        for tipo, lista in por_tipo.items():
            if lista:
                lineas.append(f"  {TIPOS_ACCION[tipo]}: {len(lista)} acción(es)")

        if self.lecciones_aprendidas:
            lineas += ["", "LECCIONES APRENDIDAS:", f"  {self.lecciones_aprendidas}"]

        if self.fecha_seguimiento:
            lineas += ["", f"Próximo seguimiento: {self.fecha_seguimiento.strftime('%d/%m/%Y')}"]

        lineas.append("=" * 60)
        return "\n".join(lineas)
