"""
Orquestador del flujo completo de análisis causal:
Evento → 5 Porqués → Ishikawa → Acciones Correctivas
"""
from datetime import datetime
from .evento import Evento
from .cinco_porques import AnalisisCincoPorques
from .ishikawa import DiagramaIshikawa, CATEGORIAS_6M
from .acciones import PlanAcciones, AccionCorrectiva


class AnalisisCausal:
    def __init__(self, evento: Evento):
        self.evento = evento
        self.cinco_porques = AnalisisCincoPorques(evento=evento)
        self.ishikawa: DiagramaIshikawa = None
        self.plan_acciones: PlanAcciones = None
        self._etapa_actual = "cinco_porques"

    # ── ETAPA 1: 5 Porqués ──────────────────────────────────────────────────

    def registrar_porque(self, respuesta: str):
        if self._etapa_actual != "cinco_porques":
            raise RuntimeError("Ya se cerró la etapa de 5 Porqués.")
        return self.cinco_porques.agregar_porque(respuesta)

    def cerrar_cinco_porques(self, numero_causa_raiz: int, justificacion: str = ""):
        self.cinco_porques.marcar_causa_raiz(numero_causa_raiz, justificacion)
        self._etapa_actual = "ishikawa"
        self.ishikawa = DiagramaIshikawa(
            evento=self.evento,
            causa_raiz_desde_5porques=self.cinco_porques.causa_raiz_identificada,
        )

    # ── ETAPA 2: Ishikawa ────────────────────────────────────────────────────

    def registrar_causa_ishikawa(self, categoria: str, causa_principal: str,
                                  subcausas: list[str] = None, evidencia: str = ""):
        if self._etapa_actual != "ishikawa":
            raise RuntimeError("Primero complete la etapa de 5 Porqués.")
        return self.ishikawa.agregar_causa(categoria, causa_principal, subcausas, evidencia)

    def confirmar_causa_ishikawa(self, categoria: str, indice: int = 0):
        self.ishikawa.confirmar_causa_raiz(categoria, indice)

    def cerrar_ishikawa(self, conclusion: str = ""):
        if conclusion:
            self.ishikawa.conclusion_final = conclusion
        causas = [c.causa_principal for c in self.ishikawa.causas_confirmadas()]
        if not causas:
            causas = [self.cinco_porques.causa_raiz_identificada]
        self.plan_acciones = PlanAcciones(causas_raiz=causas)
        self._etapa_actual = "acciones"

    # ── ETAPA 3: Acciones Correctivas ────────────────────────────────────────

    def registrar_accion(self, descripcion: str, tipo: str, responsable: str,
                          fecha_limite: datetime, causa_que_atiende: str,
                          nivel_jerarquia: int, criterio_cierre: str,
                          recursos: str = "", indicador: str = "") -> AccionCorrectiva:
        if self._etapa_actual != "acciones":
            raise RuntimeError("Primero complete las etapas anteriores.")
        accion = AccionCorrectiva(
            descripcion=descripcion,
            tipo=tipo,
            responsable=responsable,
            fecha_limite=fecha_limite,
            causa_que_atiende=causa_que_atiende,
            nivel_jerarquia=nivel_jerarquia,
            criterio_cierre=criterio_cierre,
            recursos_necesarios=recursos,
            indicador_seguimiento=indicador,
        )
        self.plan_acciones.agregar_accion(accion)
        return accion

    def cerrar_analisis(self, lecciones: str = "", fecha_seguimiento: datetime = None):
        if self.plan_acciones:
            self.plan_acciones.lecciones_aprendidas = lecciones
            self.plan_acciones.fecha_seguimiento = fecha_seguimiento
        self._etapa_actual = "cerrado"

    # ── REPORTE INTEGRADO ────────────────────────────────────────────────────

    def reporte_completo(self) -> str:
        secciones = [
            "=" * 60,
            "REPORTE COMPLETO DE ANÁLISIS CAUSAL",
            f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            "=" * 60,
            "",
            self.cinco_porques.reporte(),
        ]
        if self.ishikawa:
            secciones += ["", self.ishikawa.reporte()]
        if self.plan_acciones:
            secciones += ["", self.plan_acciones.reporte()]
        return "\n".join(secciones)

    def etapa_actual(self) -> str:
        return self._etapa_actual
