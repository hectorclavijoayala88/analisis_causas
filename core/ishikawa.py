from dataclasses import dataclass, field
from typing import Optional
from .evento import Evento


CATEGORIAS_6M = {
    "maquina": {
        "nombre": "Máquina / Equipo",
        "icono": "⚙️",
        "preguntas_guia": [
            "¿El equipo tenía fallas previas o señales de deterioro?",
            "¿Se realizó mantenimiento preventivo según el plan?",
            "¿La herramienta o equipo era el adecuado para la tarea?",
            "¿Había alarmas o sistemas de protección activos?",
            "¿La capacidad del equipo era suficiente para la demanda?",
        ],
    },
    "mano_de_obra": {
        "nombre": "Mano de Obra",
        "icono": "👷",
        "preguntas_guia": [
            "¿El operador tenía la capacitación requerida para la tarea?",
            "¿Estaba familiarizado con el procedimiento específico?",
            "¿Las condiciones físicas o mentales del trabajador eran óptimas?",
            "¿Había suficiente personal para ejecutar la tarea de forma segura?",
            "¿Se siguieron las instrucciones de trabajo?",
        ],
    },
    "metodo": {
        "nombre": "Método / Procedimiento",
        "icono": "📋",
        "preguntas_guia": [
            "¿Existe un procedimiento documentado y actualizado?",
            "¿El procedimiento es claro y fácil de seguir en campo?",
            "¿Se había validado el método con anterioridad?",
            "¿El paso a paso era adecuado para las condiciones actuales?",
            "¿Existen desvíos aceptados informalmente del procedimiento?",
        ],
    },
    "material": {
        "nombre": "Material / Insumo",
        "icono": "📦",
        "preguntas_guia": [
            "¿El material era el especificado para la operación?",
            "¿Había sido almacenado correctamente?",
            "¿Se verificó la calidad o estado del material antes de usar?",
            "¿El proveedor había presentado problemas anteriores?",
            "¿Las especificaciones del material eran las adecuadas?",
        ],
    },
    "medicion": {
        "nombre": "Medición / Control",
        "icono": "📏",
        "preguntas_guia": [
            "¿Los instrumentos de medición estaban calibrados?",
            "¿Se realizaban controles durante el proceso?",
            "¿Los límites de control estaban correctamente definidos?",
            "¿Los datos disponibles eran suficientes para detectar el problema?",
            "¿El sistema de monitoreo era confiable?",
        ],
    },
    "entorno": {
        "nombre": "Entorno / Medio Ambiente",
        "icono": "🌿",
        "preguntas_guia": [
            "¿Las condiciones ambientales (temperatura, humedad, ruido) eran adecuadas?",
            "¿El orden y aseo del área contribuyeron al evento?",
            "¿La iluminación era suficiente?",
            "¿Había factores externos que afectaron la operación?",
            "¿El espacio de trabajo era el adecuado para la tarea?",
        ],
    },
}


@dataclass
class CausaIshikawa:
    categoria: str
    causa_principal: str
    subcausas: list[str] = field(default_factory=list)
    es_causa_raiz_confirmada: bool = False
    evidencia: str = ""

    def agregar_subcausa(self, subcausa: str):
        self.subcausas.append(subcausa)

    def __str__(self):
        marca = " ★ CONFIRMADA" if self.es_causa_raiz_confirmada else ""
        lineas = [f"  → {self.causa_principal}{marca}"]
        for sc in self.subcausas:
            lineas.append(f"      • {sc}")
        if self.evidencia:
            lineas.append(f"      Evidencia: {self.evidencia}")
        return "\n".join(lineas)


@dataclass
class DiagramaIshikawa:
    evento: Evento
    causa_raiz_desde_5porques: Optional[str] = None
    categorias: dict[str, list[CausaIshikawa]] = field(default_factory=dict)
    conclusion_final: str = ""

    def __post_init__(self):
        for cat in CATEGORIAS_6M:
            self.categorias[cat] = []

    def agregar_causa(self, categoria: str, causa_principal: str,
                      subcausas: list[str] = None, evidencia: str = "") -> CausaIshikawa:
        if categoria not in CATEGORIAS_6M:
            raise ValueError(f"Categoría inválida. Use: {list(CATEGORIAS_6M.keys())}")
        causa = CausaIshikawa(
            categoria=categoria,
            causa_principal=causa_principal,
            subcausas=subcausas or [],
            evidencia=evidencia,
        )
        self.categorias[categoria].append(causa)
        return causa

    def confirmar_causa_raiz(self, categoria: str, indice: int):
        self.categorias[categoria][indice].es_causa_raiz_confirmada = True

    def causas_confirmadas(self) -> list[CausaIshikawa]:
        confirmadas = []
        for causas in self.categorias.values():
            confirmadas.extend(c for c in causas if c.es_causa_raiz_confirmada)
        return confirmadas

    def preguntas_guia(self, categoria: str) -> list[str]:
        return CATEGORIAS_6M[categoria]["preguntas_guia"]

    def reporte(self) -> str:
        lineas = [
            "=" * 60,
            "DIAGRAMA DE ISHIKAWA — ANÁLISIS DE CAUSAS",
            "=" * 60,
            self.evento.resumen(),
            "",
        ]
        if self.causa_raiz_desde_5porques:
            lineas += [
                f"Causa raíz desde 5 Porqués: {self.causa_raiz_desde_5porques}",
                "(Ishikawa valida y expande los factores que la originaron)",
                "",
            ]
        lineas += ["ESPINAS DEL DIAGRAMA:", "-" * 40]
        for cat_key, causas in self.categorias.items():
            meta = CATEGORIAS_6M[cat_key]
            lineas.append(f"\n{meta['icono']}  {meta['nombre'].upper()}")
            if causas:
                for c in causas:
                    lineas.append(str(c))
            else:
                lineas.append("  (sin causas registradas)")
        confirmadas = self.causas_confirmadas()
        lineas += ["", "=" * 60, "CAUSAS RAÍZ CONFIRMADAS:", "-" * 40]
        if confirmadas:
            for c in confirmadas:
                meta = CATEGORIAS_6M[c.categoria]
                lineas.append(f"  [{meta['nombre']}] {c.causa_principal}")
        else:
            lineas.append("  Ninguna confirmada aún.")
        if self.conclusion_final:
            lineas += ["", f"Conclusión del análisis: {self.conclusion_final}"]
        lineas.append("=" * 60)
        return "\n".join(lineas)
