"""
Training data for intent classification
"""

INTENT_TRAINING_DATA = [
    # ===========================
    # SQL: USUARIOS
    # ===========================
    {
        "text": "¿Cuántos usuarios hay registrados?",
        "intent": "sql"
    },
    {
        "text": "Lista de usuarios con sus correos",
        "intent": "sql"
    },
    {
        "text": "Mostrar la fecha de creación de los últimos usuarios",
        "intent": "sql"
    },
    {
        "text": "Quiero ver los nombres de todos los usuarios",
        "intent": "sql"
    },
    {
        "text": "¿Cuál es el correo del usuario con id 5?",
        "intent": "sql"
    },
    
    # ===========================
    # SQL: CAMIONES
    # ===========================
    {
        "text": "¿Qué camiones están registrados en el sistema?",
        "intent": "sql"
    },
    {
        "text": "Dame la capacidad del camión con placa ABC123",
        "intent": "sql"
    },
    {
        "text": "Mostrar todos los modelos de camiones",
        "intent": "sql"
    },
    {
        "text": "¿Cuántos camiones hay disponibles?",
        "intent": "sql"
    },
    {
        "text": "Ver la fecha de registro del último camión agregado",
        "intent": "sql"
    },

    # ===========================
    # SQL: PAQUETES
    # ===========================
    {
        "text": "Listar todos los paquetes pendientes",
        "intent": "sql"
    },
    {
        "text": "¿Qué paquetes tiene asignados el camión 2?",
        "intent": "sql"
    },
    {
        "text": "Ver el estado del paquete con número de seguimiento 123456",
        "intent": "sql"
    },
    {
        "text": "Mostrar los destinos de los últimos 10 paquetes",
        "intent": "sql"
    },
    {
        "text": "¿Qué usuario creó el paquete con id 15?",
        "intent": "sql"
    },

    # ===========================
    # SQL: HISTORIAL_SEGUIMIENTO
    # ===========================
    {
        "text": "Historial de estados del paquete 98765",
        "intent": "sql"
    },
    {
        "text": "¿En qué ubicación estuvo el paquete con seguimiento 111222?",
        "intent": "sql"
    },
    {
        "text": "Mostrar todas las actualizaciones recientes de seguimiento",
        "intent": "sql"
    },
    {
        "text": "Lista de paquetes que cambiaron de estado hoy",
        "intent": "sql"
    },
    {
        "text": "Última actualización del paquete 2024",
        "intent": "sql"
    },

    # ===========================
    # DOCS: INSTALACIÓN Y CONFIGURACIÓN
    # ===========================
    {
        "text": "¿Cómo configuro la aplicación por primera vez?",
        "intent": "docs"
    },
    {
        "text": "¿Cuál es la configuración recomendada para que la app funcione mejor?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo desactivo la optimización de batería para Wis Tracking?",
        "intent": "docs"
    },
    {
        "text": "¿Qué permisos debo otorgar en la configuración inicial?",
        "intent": "docs"
    },
    {
        "text": "¿Cuáles son los pasos para asociar un dispositivo?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: TRABAJAR VIAJES
    # ===========================
    {
        "text": "¿Cómo acceder a los viajes disponibles?",
        "intent": "docs"
    },
    {
        "text": "¿Qué información muestra la pantalla de un viaje?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo cambiar el orden de visitas durante un viaje?",
        "intent": "docs"
    },
    {
        "text": "¿Qué pasa si quiero cancelar una visita?",
        "intent": "docs"
    },
    {
        "text": "¿Cuál es la diferencia entre confirmación automática y manual de llegada?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: VISITAS, ENTREGAS Y RECEPCIONES
    # ===========================
    {
        "text": "¿Cómo registrar la entrega de objetos?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo usar el escáner para registrar entregas?",
        "intent": "docs"
    },
    {
        "text": "¿Qué hacer si recibo un objeto no esperado?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo puedo agregar comentarios a una visita?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo restaurar objetos procesados?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: FINALIZAR VIAJE
    # ===========================
    {
        "text": "¿Qué condición debo cumplir para finalizar un viaje?",
        "intent": "docs"
    },
    {
        "text": "¿Qué ocurre con las visitas pendientes al cerrar un viaje?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo es el comportamiento posterior a la finalización del viaje?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: SINCRONIZACIÓN Y REGISTRO
    # ===========================
    {
        "text": "¿Cómo se sincronizan los datos de los dispositivos?",
        "intent": "docs"
    },
    {
        "text": "¿Qué notificaciones envía el sistema al registrar visitas?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo se registra la ubicación del dispositivo?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: AUTENTICACIÓN Y CONTRASEÑAS
    # ===========================
    {
        "text": "¿Cómo registrar un nuevo usuario en la app?",
        "intent": "docs"
    },
    {
        "text": "¿Qué políticas de seguridad existen para las contraseñas?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo recuperar o cambiar mi contraseña?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: INDICADORES
    # ===========================
    {
        "text": "¿Qué indicadores puedo consultar sobre los objetos entregados?",
        "intent": "docs"
    },
    {
        "text": "¿Dónde veo los accesos rápidos en la aplicación?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo revisar los indicadores del día?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: MANTENIMIENTO Y OBJETOS
    # ===========================
    {
        "text": "¿Cómo se gestionan los motivos desde el panel web?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo vincular un dispositivo móvil al sistema?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo editar un punto de entrega?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo crear un nuevo objeto en el sistema?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo generar una etiqueta de recepción?",
        "intent": "docs"
    },
    {
        "text": "¿Qué significa la trazabilidad de un objeto?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: VEHÍCULOS
    # ===========================
    {
        "text": "¿Cómo consultar los vehículos registrados?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo crear un nuevo tipo de vehículo?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo editar un vehículo existente?",
        "intent": "docs"
    },

    # ===========================
    # DOCS: REPORTES
    # ===========================
    {
        "text": "¿Dónde puedo consultar las tareas activas?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo ver el detalle de un viaje?",
        "intent": "docs"
    },
    {
        "text": "¿Dónde encuentro las fotos y firmas registradas?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo exportar un reporte de viajes?",
        "intent": "docs"
    },
    {
        "text": "¿Cómo revisar el resumen de viajes realizados?",
        "intent": "docs"
    }
]
