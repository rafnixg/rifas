# Rifas - Módulo de Gestión de Rifas para Odoo 18.0

[![Version](https://img.shields.io/badge/version-18.0.3.0.0-blue.svg)](https://github.com/rafnixg/rifas)
[![License](https://img.shields.io/badge/license-LGPL--3-green.svg)](LICENSE)
[![Odoo](https://img.shields.io/badge/Odoo-18.0-purple.svg)](https://www.odoo.com/)
[![Author](https://img.shields.io/badge/author-Rafnix%20Guzman-orange.svg)](https://rafnixg.com)

## 📝 DESCRIPCIÓN

El módulo **Rifas** es una solución completa para la gestión de rifas, sorteos y venta de boletos en Odoo 18.0. Diseñado especialmente para organizaciones, empresas y fundaciones que necesitan realizar sorteos de manera eficiente y transparente.

### Características Principales

- 🎲 **Gestión Completa de Rifas**: Creación, configuración y administración de rifas con parámetros personalizables
- 🎟️ **Sistema de Boletos**: Generación automática de números de boletos y control de asignación
- 👥 **Gestión de Participantes**: Registro completo de clientes y seguimiento de sus participaciones
- 💰 **Control de Pagos**: Integración con sistema de pagos y seguimiento de transacciones
- 🎯 **Sorteo Manual Controlado**: Ingreso manual del número ganador con validación automática
- 📊 **Reportes Detallados**: Informes completos de rifas, ventas y participantes
- 🌐 **Interfaz Web**: Portal web integrado para la venta de boletos online
- 📧 **Notificaciones**: Sistema de correos automáticos para participantes y ganadores

## 🌐 CONTEXTO

Este módulo fue desarrollado para cubrir la necesidad específica de organizaciones que realizan rifas como método de recaudación de fondos o actividades comerciales. Es ideal para:

- **Fundaciones y ONGs**: Recaudación de fondos mediante rifas benéficas
- **Empresas**: Promociones y campañas de marketing
- **Organizaciones Deportivas**: Rifas para financiar actividades
- **Instituciones Educativas**: Eventos de recaudación escolar
- **Emprendedores**: Negocio de rifas y sorteos

El módulo se integra completamente con el ecosistema Odoo, aprovechando las funcionalidades existentes de CRM, contabilidad y comercio electrónico.

## 🚀 INSTALACIÓN

### Requisitos Previos

- Odoo 18.0 instalado y funcionando
- Acceso de administrador al sistema
- Python 3.8 o superior

### Pasos de Instalación

1. **Clonar el repositorio en el directorio de addons:**
   ```bash
   cd /path/to/odoo/addons
   git clone https://github.com/rafnixg/rifas.git
   ```

2. **Para instalación en Windows:**
   ```bash
   cd c:\projectos\odoo\data_dir\addons\18.0
   git clone https://github.com/rafnixg/rifas.git
   ```

3. **Reiniciar el servidor Odoo:**
   ```bash
   ./odoo-bin -c /path/to/config/file.conf --update=all
   ```

4. **Activar el modo desarrollador:**
   - Ve a `Configuración > Activar el modo desarrollador`

5. **Instalar el módulo:**
   - Ve a `Aplicaciones`
   - Busca "Rifas"
   - Haz clic en "Instalar"

### Verificación de la Instalación

Después de la instalación, deberías ver el menú "Rifas" en tu dashboard principal de Odoo.

## ⚙️ CONFIGURACIÓN

### Configuración Inicial

1. **Configurar secuencias de numeración:**
   - Los números de boletos se generan automáticamente usando secuencias predefinidas
   - Las rifas tienen códigos únicos asignados automáticamente

2. **Configurar plantillas de email:**
   - El módulo incluye plantillas predefinidas para confirmación de compra
   - Las plantillas se pueden personalizar desde `Configuración > Técnico > Email > Plantillas`

3. **Configurar métodos de pago:**
   - Ve a `Rifas > Gestión de Ventas > Métodos de Pago`
   - Configura los métodos disponibles para la venta de boletos
   - Integra con las cuentas contables correspondientes

### Configuración de Seguridad

El módulo incluye roles de seguridad predefinidos:

- **Administrador de Rifas**: Control total del módulo
- **Usuario de Rifas**: Creación y gestión de rifas
- **Vendedor de Boletos**: Solo venta de boletos

### Configuración Web

Para habilitar la venta online:

1. **Activar el sitio web:**
   - Asegúrate de tener el módulo Website instalado
   - El módulo incluye controladores web para la venta de boletos

2. **Portal de rifas:**
   - Los clientes pueden acceder a `/rifas` para ver rifas disponibles
   - Funcionalidad de compra integrada con el portal web de Odoo

## 📖 USO

### Gestión de Rifas

1. **Crear una nueva rifa:**
   ```
   Rifas > Gestión de Rifas > Rifas > Crear
   ```
   - Completa la información básica (nombre, descripción, fechas)
   - Define el número de boletos y precio
   - Configura las reglas del sorteo

2. **Gestionar boletos:**
   ```
   Rifas > Gestión de Rifas > Boletos
   ```
   - Visualiza todos los boletos vendidos
   - Asigna boletos manualmente o automáticamente

3. **Gestionar participantes:**
   ```
   Rifas > Clientes
   ```
   - Registra nuevos participantes
   - Visualiza el historial de compras

4. **Procesar ventas y pagos:**
   ```
   Rifas > Gestión de Ventas > Órdenes de Venta
   Rifas > Gestión de Ventas > Pagos
   ```
   - Registra órdenes de venta de boletos
   - Confirma pagos y transacciones

5. **Realizar sorteo:**
   - Desde la rifa específica, usa el botón "Realizar Sorteo"
   - Ingresa el número ganador manualmente
   - El sistema valida que el número esté vendido y marca al ganador
   - Se envían notificaciones automáticas

### Venta Online

Los clientes pueden:
- Acceder al portal web de rifas
- Seleccionar rifas disponibles
- Comprar boletos online
- Recibir confirmaciones por email
- Verificar el estado de sus boletos

### Reportes y Análisis

El módulo proporciona vistas detalladas para análisis:

**Gestión de Rifas:**
- Lista de todas las rifas con estados y estadísticas
- Detalle de boletos vendidos por rifa
- Historial de ganadores

**Gestión de Ventas:**
- Órdenes de venta y su estado
- Seguimiento de pagos por método
- Análisis de ventas por cliente

**Reportes Financieros:**
- Integración con reportes contables de Odoo
- Seguimiento de ingresos por rifa
- Estados de cuenta por cliente


## 🛠️ DESARROLLO

¿Quieres contribuir al proyecto? ¡Excelente! Consulta nuestro [DEVELOP.md](DEVELOP.md) para obtener información detallada sobre:

- Configuración del entorno de desarrollo
- Estándares de código
- Proceso de testing
- Guidelines de contribución

### Estructura del Proyecto

```
rifas/
├── controllers/          # Controladores web
├── data/                # Datos iniciales y plantillas
├── models/              # Modelos de datos
├── security/            # Reglas de acceso
├── static/              # Archivos estáticos (CSS, JS)
├── views/               # Vistas y formularios
├── wizards/             # Asistentes
├── __manifest__.py      # Manifiesto del módulo
└── README.md           # Este archivo
```

## 🗺️ ROADMAP

Consulta nuestro [ROADMAP.md](ROADMAP.md) para conocer:

- Funcionalidades actuales
- Características planificadas
- Cronograma de desarrollo
- Cómo proponer nuevas funcionalidades

## 📚 HISTORIAL

### Versión 18.0.2.1.0 (Actual)
- ✅ Gestión completa de rifas y boletos
- ✅ Portal web para venta online
- ✅ Sistema de pagos integrado
- ✅ Sorteo automático de ganadores
- ✅ Reportes básicos y notificaciones

### Versiones Anteriores

Para el historial completo de cambios, consulta las versiones en el repositorio de GitHub.

## 📋 NOVEDADES EN VERSIÓN 3.0.0

### 🆕 Mejoras en Documentación
- **Documentación Completa**: Todos los modelos, clases y métodos ahora cuentan con documentación comprensiva en inglés
- **Estándares de Código**: Implementación de mejores prácticas en la documentación del código
- **Guías Técnicas**: Documentación detallada para desarrolladores que quieran extender el módulo

### 🔧 Mejoras Técnicas
- **Corrección de Errores**: Eliminación de errores de sintaxis y mejora en la estructura del código
- **Optimización**: Mejoras en el rendimiento y legibilidad del código
- **Validaciones**: Mejor manejo de errores y validaciones de datos

### 📚 Documentación para Desarrolladores
La versión 3.0.0 incluye documentación técnica completa que facilita:
- Comprensión del flujo de negocio
- Extensión y personalización del módulo
- Integración con otros módulos de Odoo
- Mantenimiento y debugging

## 🤝 CONTRIBUIR

¡Las contribuciones son bienvenidas! Para contribuir:

1. **Fork** el repositorio
2. **Crea** una rama para tu funcionalidad (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Código de Conducta

Este proyecto se adhiere al [Código de Conducta de Odoo](https://www.odoo.com/code-of-conduct).

## 📄 LICENCIA

Este proyecto está licenciado bajo la Licencia LGPL-3 - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 AUTOR

**Rafnix Guzmán**
- Website: [rafnixg.com](https://rafnixg.com)
- GitHub: [@rafnixg](https://github.com/rafnixg)
- LinkedIn: [Rafnix Guzmán](https://linkedin.com/in/rafnixg)

## 🆘 SOPORTE

Si necesitas ayuda:

1. **Documentación**: Revisa la documentación completa
2. **Issues**: Abre un issue en GitHub
3. **Discusiones**: Participa en las discusiones del proyecto
4. **Email**: Contacta directamente al autor

---

⭐ **¡Si este proyecto te resulta útil, considera darle una estrella en GitHub!**