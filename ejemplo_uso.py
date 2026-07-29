"""
Ejemplo de uso completo del sistema de análisis causal.
Simula el análisis del derrame de aceite en bomba B-03.
"""
from datetime import datetime
from core import Evento
from core.orquestador import AnalisisCausal


def main():
    # ── 1. Definir el evento ─────────────────────────────────────────────────
    evento = Evento(
        descripcion="Derrame de aceite hidráulico en línea de producción LN-02",
        area="Producción",
        proceso="Llenado y sellado",
        fecha=datetime(2026, 7, 28, 14, 30),
        consecuencias="Paro de línea 2 horas. Riesgo de caída por piso resbaloso. "
                      "150 litros de aceite derramado. Costo estimado: $800 USD.",
        tipo="incidente",
        reportado_por="Carlos Mendoza",
        turno="Tarde",
        equipos_involucrados=["Bomba B-03", "Sistema hidráulico LN-02"],
        personas_involucradas=3,
    )

    analisis = AnalisisCausal(evento)

    # ── 2. Cinco Porqués ─────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("ETAPA 1: CINCO PORQUÉS")
    print("=" * 60)

    p1 = analisis.registrar_porque("Falló el sello mecánico de la bomba B-03")
    p2 = analisis.registrar_porque("El sello estaba desgastado más allá de su vida útil")
    p3 = analisis.registrar_porque("No fue reemplazado en el último mantenimiento preventivo")
    p4 = analisis.registrar_porque("La bomba B-03 no estaba incluida en el plan de mantenimiento vigente")
    p5 = analisis.registrar_porque(
        "El plan de mantenimiento no se actualizó cuando se instaló la bomba hace 8 meses"
    )

    # Marcar causa raíz en el porqué 5 y cerrar etapa
    analisis.cerrar_cinco_porques(
        numero_causa_raiz=5,
        justificacion="No existe un proceso formal para actualizar el plan de mantenimiento al incorporar nuevos equipos"
    )
    print(analisis.cinco_porques.reporte())
    print("\nCRITERIOS PARA VALIDAR LA CAUSA RAÍZ:")
    for criterio in analisis.cinco_porques.criterios_buena_causa_raiz():
        print(f"  □ {criterio}")

    # ── 3. Ishikawa ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("ETAPA 2: DIAGRAMA DE ISHIKAWA")
    print("=" * 60)

    # Máquina
    analisis.registrar_causa_ishikawa(
        "maquina",
        "Sello mecánico sin monitoreo de condición",
        subcausas=["No hay sensor de temperatura/vibración en bomba B-03",
                   "Inspección visual no detectó desgaste externo"],
        evidencia="Registro de mantenimiento sin entrada para B-03 en últimos 8 meses"
    )

    # Método
    c_metodo = analisis.registrar_causa_ishikawa(
        "metodo",
        "Plan de mantenimiento no incluye proceso de incorporación de nuevos equipos",
        subcausas=["Procedimiento de puesta en marcha de equipos no menciona actualización del plan MP",
                   "No hay lista de verificación al instalar equipos nuevos"],
        evidencia="Revisión del procedimiento de instalación de equipos: no incluye paso de actualización MP"
    )
    analisis.confirmar_causa_ishikawa("metodo", 0)  # Esta es causa raíz confirmada

    # Mano de obra
    analisis.registrar_causa_ishikawa(
        "mano_de_obra",
        "Técnico que instaló la bomba no notificó al área de mantenimiento",
        subcausas=["No está definido formalmente quién debe notificar la instalación"],
        evidencia="Entrevista con técnico: 'no sabía que debía avisarle a mantenimiento'"
    )

    # Medición
    analisis.registrar_causa_ishikawa(
        "medicion",
        "Sin indicador de cobertura del plan de mantenimiento vs equipos reales en planta",
        evidencia="No existe reporte de inventario de equipos vs plan MP"
    )

    analisis.cerrar_ishikawa(
        conclusion="La causa raíz es sistémica: ausencia de proceso de actualización del plan de "
                   "mantenimiento al incorporar nuevos equipos. Factores contribuyentes: falta de "
                   "indicador de cobertura y responsabilidad no definida en la instalación de equipos."
    )
    print(analisis.ishikawa.reporte())

    # ── 4. Acciones Correctivas ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("ETAPA 3: ACCIONES CORRECTIVAS INTEGRALES")
    print("=" * 60)

    # Acción correctiva — nivel 4 (administrativo)
    analisis.registrar_accion(
        descripcion="Actualizar plan de mantenimiento preventivo incluyendo bomba B-03 con frecuencia "
                    "de inspección de sello cada 1.000 horas de operación",
        tipo="correctiva",
        responsable="Jefe de Mantenimiento — Rodrigo Torres",
        fecha_limite=datetime(2026, 8, 5),
        causa_que_atiende="Bomba B-03 no incluida en plan de mantenimiento",
        nivel_jerarquia=4,
        criterio_cierre="Plan de MP actualizado, revisado y comunicado al equipo. Bomba B-03 aparece "
                        "con próxima intervención programada.",
        recursos="2 horas de tiempo del jefe de mantenimiento. Sistema CMMS.",
        indicador="% de equipos activos con cobertura en plan MP (meta: 100%)"
    )

    # Acción preventiva — nivel 4 (administrativo)
    analisis.registrar_accion(
        descripcion="Crear e implementar procedimiento de incorporación de nuevos equipos que incluya "
                    "paso obligatorio de actualización del plan de mantenimiento preventivo",
        tipo="preventiva",
        responsable="Coordinador SGI — Ana Ríos",
        fecha_limite=datetime(2026, 8, 20),
        causa_que_atiende="No existe proceso formal de actualización del plan MP al incorporar nuevos equipos",
        nivel_jerarquia=4,
        criterio_cierre="Procedimiento aprobado, publicado en sistema documental y comunicado a "
                        "técnicos de instalación y área de mantenimiento",
        recursos="Reunión de trabajo con mantenimiento y producción. 1 día de elaboración.",
        indicador="# de equipos nuevos instalados que completaron proceso de incorporación / total instalados"
    )

    # Acción de ingeniería — nivel 3
    analisis.registrar_accion(
        descripcion="Instalar sensor de vibración/temperatura en bomba B-03 y configurar alerta "
                    "en sistema SCADA al superar umbrales definidos",
        tipo="mitigacion",
        responsable="Supervisor de Mantenimiento Eléctrico — Pedro Luna",
        fecha_limite=datetime(2026, 9, 15),
        causa_que_atiende="Sello mecánico sin monitoreo de condición",
        nivel_jerarquia=3,
        criterio_cierre="Sensor instalado, calibrado y alerta activa en SCADA. Registro de primera "
                        "lectura normal de operación.",
        recursos="Sensor IOT $350 USD. 8 horas de instalación y configuración.",
        indicador="Disponibilidad del sistema de monitoreo (%)"
    )

    # Estandarización
    analisis.registrar_accion(
        descripcion="Realizar auditoría de cobertura del plan de mantenimiento vs inventario real "
                    "de equipos en planta e incorporar como indicador mensual del área",
        tipo="estandarizacion",
        responsable="Jefe de Mantenimiento — Rodrigo Torres",
        fecha_limite=datetime(2026, 8, 31),
        causa_que_atiende="Sin indicador de cobertura del plan MP vs equipos reales",
        nivel_jerarquia=4,
        criterio_cierre="Primer informe de cobertura emitido y KPI incluido en tablero mensual de mantenimiento",
        indicador="Cobertura MP = equipos con plan / equipos activos × 100 (meta: ≥95%)"
    )

    analisis.cerrar_analisis(
        lecciones="La instalación de nuevos equipos debe activar automáticamente la actualización "
                  "del plan de mantenimiento preventivo. La ausencia de este paso generó una brecha "
                  "silenciosa que derivó en falla y derrame.",
        fecha_seguimiento=datetime(2026, 8, 15)
    )

    print(analisis.plan_acciones.reporte())

    # ── Reporte completo ─────────────────────────────────────────────────────
    with open("output/reporte_analisis_ejemplo.txt", "w", encoding="utf-8") as f:
        f.write(analisis.reporte_completo())
    print("\n✓ Reporte completo guardado en output/reporte_analisis_ejemplo.txt")


if __name__ == "__main__":
    main()
