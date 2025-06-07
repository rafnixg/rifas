# Historial de Cambios

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [18.0.2.1.0] - 2025-05-19

### ✨ Agregado
- Campos de imagen y URL de logo en el modelo PaymentMethod con generación automática de URLs
- Notificaciones por email para pagos aprobados con registro de errores
- Funcionalidad de modal de imágenes en JavaScript global para la galería
- Controlador de imágenes para manejo optimizado de recursos gráficos

### 🔧 Mejorado
- Actualización de enlaces CSS y JS a la versión 1.3.3 en todas las plantillas web
- Refactorización de estilos CSS con variables CSS para mejor mantenibilidad
- Mejora en el selector de boletos con estadísticas adicionales y layout optimizado
- Ordenamiento por fecha de creación en modelos SaleOrder y Ticket
- Layout mejorado para métodos de pago y proceso de checkout

### 🧹 Removido
- Estilos CSS no utilizados en páginas home y raffle para optimizar el código
- Direcciones de email hardcodeadas en el wizard de ganador de rifa

## [18.0.2.0.0] - 2025-05-14

### ✨ Agregado
- Sistema completo de menús para gestión de rifas y ventas
- Estilos mejorados para badges en la interfaz de usuario
- Estructura de navegación organizada con submenús específicos

### 🔧 Mejorado
- Generación mejorada de slugs para mejor versionado e identificación
- Actualización de enlaces CSS para consistencia en el versionado

## [18.0.1.3.0] - 2025-05-13

### ✨ Agregado
- Sistema de validación con códigos únicos para órdenes
- Gestión completa de clientes con campos extendidos
- Componentes UI mejorados para una mejor experiencia de usuario
- Plantilla de validación para verificar compras
- Modelo Company para gestión de empresa

### 🔧 Mejorado
- Gestión de clientes con campos adicionales y validaciones
- Plantillas de email actualizadas con mejor formato
- Vistas de cliente con formularios completos
- Componentes web con funcionalidades ampliadas
- Proceso de checkout con validaciones mejoradas

### 🐛 Corregido
- Optimización de plantillas home y raffle para mejor rendimiento
- Mejoras en el CSS global y de checkout

## [18.0.1.2.0] - 2025-05-12

### ✨ Agregado
- Funcionalidades completas de cliente, pago y rifas
- Sistema de pagos integrado con validaciones
- Gestión avanzada de rifas con múltiples estados

### 🔧 Mejorado
- Modelos de datos con relaciones optimizadas
- Validaciones de negocio para integridad de datos
- Interfaz de usuario más intuitiva

## [18.0.1.1.0] - 2025-05-10

### ✨ Agregado
- Proceso de checkout completamente funcional
- Selección de boletos de rifa con validaciones mejoradas
- Actualización de interfaz de usuario para mejor usabilidad

### 🔧 Mejorado
- Refactorización del proceso de selección de boletos
- Validaciones mejoradas en el checkout
- Optimización de la experiencia del usuario

## [18.0.1.0.0] - 2025-05-09

### ✨ Agregado
- Funcionalidades de gestión de rifas incluyendo selección de boletos
- Proceso de checkout completo
- Vistas mejoradas para rifas y boletos con decoraciones de estado
- Mejor manejo de descripciones en las interfaces

### 🔧 Mejorado
- Decoraciones de estado para mejor visualización
- Manejo optimizado de descripciones en las vistas

## [18.0.0.1.0] - 2025-05-09 (Versión Inicial)

### ✨ Agregado
- **Funcionalidades Core:**
  - Modelo Ticket para gestión de boletos de rifa con campos para asociación de rifa, número de boleto, estado de ganador y orden de venta relacionada
  - Derechos de acceso para el modelo Ticket y modelos relacionados en la configuración de seguridad
  - Vistas para gestión de pagos, rifas, órdenes de venta y boletos (vistas de árbol y formulario)
  - Wizard para selección de ganador de rifa con validación de número ganador y existencia de boleto
  - Funcionalidad de notificación para informar al ganador de la rifa

- **Estructura del Proyecto:**
  - Controladores base para checkout, home, raffle y validate
  - Modelos de datos: client, payment, raffle, sale_order, ticket
  - Vistas web con plantillas para home, raffle, checkout, confirmation y validate
  - Secuencias automáticas para numeración
  - Plantillas de email para notificaciones
  - Iconos SVG y PNG para el módulo

- **Documentación:**
  - README.md inicial con descripción del proyecto
  - ROADMAP.md con planes de desarrollo
  - Configuración de .gitignore

- **Configuración:**
  - Manifiesto del módulo con dependencias y configuración
  - Archivos de seguridad y permisos
  - Assets CSS y JavaScript para frontend

### 🏗️ Arquitectura
- Módulo compatible con Odoo 18.0
- Integración completa con el sistema de mail de Odoo
- Diseño modular y extensible
- Separación clara entre lógica de negocio y presentación

---

## Convenciones de Versionado

Este proyecto utiliza [Versionado Semántico](https://semver.org/) con el formato:
**MAYOR.MENOR.PARCHE.BUILD**

- **MAYOR**: Cambios incompatibles en la API
- **MENOR**: Funcionalidades nuevas compatibles hacia atrás
- **PARCHE**: Correcciones de errores compatibles hacia atrás
- **BUILD**: Número de construcción específico para Odoo

## Tipos de Cambios

- ✨ **Agregado**: Para nuevas funcionalidades
- 🔧 **Mejorado**: Para cambios en funcionalidades existentes
- 🐛 **Corregido**: Para corrección de errores
- 🧹 **Removido**: Para funcionalidades eliminadas
- 🔒 **Seguridad**: Para correcciones relacionadas con seguridad
- 🏗️ **Arquitectura**: Para cambios en la estructura del proyecto

## Contribuciones

Para contribuir al proyecto:
1. Revisa este historial para entender la evolución del proyecto
2. Sigue las convenciones de commit establecidas
3. Actualiza este archivo con tus cambios siguiendo el formato establecido

## Soporte

Para consultas sobre versiones específicas o para reportar problemas:
- **Issues**: [GitHub Issues](https://github.com/rafnixg/rifas/issues)
- **Contacto**: rafnixg@gmail.com