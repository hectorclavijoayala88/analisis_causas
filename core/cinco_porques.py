from dataclasses import dataclass, field
from typing import Optional
from .evento import Evento


@dataclass
class Porque:
    numero: int
    pregunta: str
    respuesta: str
    es_causa_raiz: bool = False

    def __str__(self):
        marca = " ← CAUSA RAÍZ" if self.es_causa_raiz else ""
        return f"  Por qué {self.numero}: {self.pregunta}\n  Respuesta: {self.respuesta}{marca}"


@dataclass
class AnalisisCincoPorques:
    evento: Evento
    porques: list[Porque] = field(default_factory=list)
    causa_raiz_identificada: Optional[str] = None
    notas_facilitador: str = ""

    def agregar_porque(self, respuesta: str) -> Porque:
        numero = len(self.porques) + 1
        if numero == 1:
            pregunta = f"¿Por qué ocurrió: '{self.evento.descripcion}'?"
        else:
            pregunta = f"¿Por qué {self.porques[-1].respuesta.lower().rstrip('.')}?"

        porque = Porque(numero=numero, pregunta=pregunta, respuesta=respuesta)
        self.porques.append(porque)
        return porque

    def marcar_causa_raiz(self, numero: int, justificacion: str = ""):
        for p in self.porques:
            p.es_causa_raiz = False
        self.porques[numero - 1].es_causa_raiz = True
        self.causa_raiz_identificada = self.porques[numero - 1].respuesta
        if justificacion:
            self.notas_facilitador = justificacion

    def es_completo(self) -> bool:
        return len(self.porques) >= 1 and self.causa_raiz_identificada is not None

    def reporte(self) -> str:
        lineas = [
            "=" * 60,
            "ANÁLISIS 5 PORQUÉS",
            "=" * 60,
            self.evento.resumen(),
            "",
            "CADENA CAUSAL:",
            "-" * 40,
        ]
        for p in self.porques:
            lineas.append(str(p))
            lineas.append("")
        lineas += [
            "-" * 40,
            f"CAUSA RAÍZ IDENTIFICADA: {self.causa_raiz_identificada or 'Pendiente'}",
        ]
        if self.notas_facilitador:
            lineas.append(f"Notas: {self.notas_facilitador}")
        lineas.append("=" * 60)
        return "\n".join(lineas)

    def criterios_buena_causa_raiz(self) -> list[str]:
        return [
            "¿Es una causa que podemos controlar o influenciar directamente?",
            "¿Si eliminamos esta causa, el problema no volvería a ocurrir?",
            "¿Es específica y no genérica (ej: 'falta de mantenimiento' vs 'falta de plan de mantenimiento preventivo para bomba X')?",
            "¿Existe evidencia que la soporte (datos, registros, testimonios)?",
            "¿Está en el nivel más profundo posible de nuestra cadena causal?",
        ]
