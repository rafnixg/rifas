# Guía de Desarrollo - Rifas Module

## 🚀 Configuración del Entorno de Desarrollo

### Requisitos

- Python 3.8+
- Odoo 18.0 (modo desarrollo)
- Git
- Editor de código (recomendado: VS Code con extensión de Python)

### Configuración Inicial

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/rafnixg/rifas.git
   cd rifas
   ```

2. **Configurar entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configurar Odoo en modo desarrollo:**
   ```bash
   ./odoo-bin -c config.conf --dev=reload,qweb,werkzeug,xml
   ```

## 📁 Estructura del Proyecto

```
rifas/
├── __init__.py              # Inicialización del módulo
├── __manifest__.py          # Manifiesto y dependencias
├── controllers/             # Controladores web
│   ├── __init__.py
│   ├── main.py             # Controlador principal
│   └── website.py          # Controladores del sitio web
├── data/                   # Datos de demostración y configuración
│   ├── ir.sequence.xml     # Secuencias de numeración
│   └── mail_templates.xml  # Plantillas de email
├── models/                 # Modelos de datos
│   ├── __init__.py
│   ├── raffle.py          # Modelo principal de rifas
│   ├── ticket.py          # Modelo de boletos
│   ├── client.py          # Modelo de clientes
│   └── payment.py         # Modelo de pagos
├── security/               # Permisos y accesos
│   └── ir.model.access.csv # Reglas de acceso
├── static/                 # Archivos estáticos
│   ├── css/               # Hojas de estilo
│   ├── js/                # JavaScript
│   └── img/               # Imágenes
├── views/                  # Vistas y formularios
│   ├── raffle_views.xml   # Vistas de rifas
│   ├── ticket_views.xml   # Vistas de boletos
│   └── menu_items.xml     # Elementos del menú
├── wizards/                # Asistentes
│   └── raffle_winner_views.xml
└── tests/                  # Pruebas unitarias
    ├── __init__.py
    └── test_raffle.py
```

## 🏗️ Arquitectura del Módulo

### Modelos Principales

1. **raffle.raffle**: Modelo principal de rifas
2. **raffle.ticket**: Boletos de las rifas
3. **raffle.client**: Clientes/participantes
4. **raffle.payment**: Pagos de boletos

### Relaciones entre Modelos

```
raffle.raffle (1) -----> (many) raffle.ticket
raffle.client (1) -----> (many) raffle.ticket
raffle.ticket (1) -----> (many) raffle.payment
```

## 🔧 Estándares de Desarrollo

### Convenciones de Código

1. **Python**: Seguir PEP 8
2. **XML**: Indentación de 4 espacios
3. **JavaScript**: Usar ES6+
4. **CSS**: Metodología BEM

### Nomenclatura

- **Modelos**: `raffle.nombre_modelo`
- **Campos**: snake_case
- **Métodos**: snake_case
- **Vistas**: `nombre_modelo_tipo_view`

### Ejemplo de Modelo

```python
from odoo import models, fields, api

class Raffle(models.Model):
    _name = 'raffle.raffle'
    _description = 'Rifa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Nombre', required=True)
    description = fields.Text('Descripción')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activa'),
        ('finished', 'Finalizada')
    ], default='draft', tracking=True)
    
    @api.model
    def create(self, vals):
        # Lógica personalizada
        return super().create(vals)
```

## 🔄 Workflow de Desarrollo

### Git Flow

1. **Crear rama:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Desarrollar y testear:**
   ```bash
   # Hacer cambios
   git add .
   git commit -m "feat: agregar nueva funcionalidad"
   ```

3. **Crear Pull Request:**
   - Descripción clara del cambio
   - Screenshots si es necesario
   - Tests pasando

### Commits Convencionales

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `style:` Formato de código
- `refactor:` Refactorización
- `test:` Agregrar tests
- `chore:` Tareas de mantenimiento

## 🐛 Debugging

### Logs

```python
import logging
_logger = logging.getLogger(__name__)

# En tus métodos
_logger.info("Información general")
_logger.warning("Advertencia")
_logger.error("Error")
```

### Debugger

```python
import pdb; pdb.set_trace()  # Punto de parada
```

### Variables de Entorno

```bash
export ODOO_RC=/path/to/config
export PYTHONPATH=/path/to/odoo
```

## 📚 Recursos Útiles

### Documentación Oficial

- [Odoo Developer Documentation](https://www.odoo.com/documentation/18.0/developer.html)
- [ORM API](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html)
- [Web Controllers](https://www.odoo.com/documentation/18.0/developer/reference/backend/http.html)

### Herramientas Recomendadas

- **VS Code Extensions:**
  - Python
  - XML Tools
  - Odoo Snippets

- **Debugging Tools:**
  - Odoo Debug Mode
  - Browser Developer Tools
  - Python Debugger
  - VS Code Debugger

## 🤝 Contribuir

### Proceso de Contribución

1. Fork del repositorio
2. Crear rama de feature
3. Desarrollar con tests
4. Crear pull request
5. Code review
6. Merge

### Code Review Checklist

- [ ] Código sigue estándares
- [ ] Tests implementados y pasando
- [ ] Documentación actualizada
- [ ] Sin conflictos de merge
- [ ] Funcionalidad probada

## 📧 Contacto

Para dudas sobre desarrollo:

- **Issues**: [GitHub Issues](https://github.com/rafnixg/rifas/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rafnixg/rifas/discussions)
- **Email**: rafnixg@gmail.com

---

¡Gracias por contribuir al desarrollo del módulo Rifas! 🎯
