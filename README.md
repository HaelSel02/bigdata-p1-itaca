# Proyecto N · bigdata-p1-itaca

## Descripción y objetivo

Levantamiento del proyecto mediante docker compose y uso de git para la publicación del mismo.

## Arquitectura

```mermaid
graph LR
    A[Fuente de datos<br/>exportación XML] --> B[Procesamiento] --> C[Almacenamiento]
```

## Fuentes de datos

### Mecanismo de acceso

Cada una de las cinco tablas se obtiene mediante exportación XML:

| Tabla | Mecanismo de acceso (exportación XML) |
|-------|----------------------------------------|
| [tabla_1] | [URL / endpoint / fichero / procedimiento de exportación] |
| [tabla_2] | [...] |
| [tabla_3] | [...] |
| [tabla_4] | [...] |
| [tabla_5] | [...] |

### Frecuencia de actualización esperada

| Tabla | Frecuencia |
|-------|-----------|
| [tabla_1] | [diaria / semanal / mensual / bajo demanda] |
| [tabla_2] | [...] |
| ... | ... |

## Campos disponibles por tabla

| Tabla | Campo | Tipo | Descripción |
|-------|-------|------|-------------|
| [tabla_1] | [campo] | [tipo] | [descripción] |
| ... | ... | ... | ... |