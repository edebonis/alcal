# 📋 Análisis de Campos Faltantes - Fichas de Inscripción

**Fecha:** 2025-01-XX  
**Objetivo:** Verificar que los modelos cumplan con todos los campos requeridos en las fichas oficiales

---

## 📄 FICHA DE INSCRIPCIÓN (Alumno)

### ✅ Campos que YA existen en el modelo Alumno:
- ✅ Apellido/s, Nombre/s
- ✅ Fecha de Nacimiento (`fecha_nacimiento`)
- ✅ DNI (`dni`, `documento_tipo`)
- ✅ Sexo (`sexo` - pero limitado a M/F)
- ✅ Lugar de nacimiento (`lugar_nacimiento`)
- ✅ Nacionalidad (`nacionalidad`)
- ✅ Domicilio (`direccion`)
- ✅ Localidad (`localidad`)
- ✅ Teléfono (`telefono`)
- ✅ Teléfono celular (`celular_alumno`)
- ✅ Email (`email`)
- ✅ Responsables (Padre, Madre, Tutor)
- ✅ Profesión del responsable (`profesion_padre`, `profesion_madre`, `profesion_tutor`)
- ✅ Vínculo con el estudiante (`vinculo_tutor`)

### ❌ Campos FALTANTES en el modelo Alumno:

#### 1. Identificación
- ❌ **CUIL**: Número de CUIL del estudiante
- ❌ **Estado del DNI**: 
  - Tiene DNI físico
  - DNI en trámite
  - DNI no en trámite
  - No posee DNI argentino
- ❌ **Certificado de Pre-Identificación (CPI)**: SI/NO

#### 2. Identidad de Género (ampliar opciones)
- ❌ Actualmente solo tiene: M/F
- ❌ Necesita: Mujer, Varón, Mujer trans/travesti, Varón trans/masculinidad trans, No binario, Otra, No desea responder

#### 3. Domicilio (más detallado)
- ❌ **Piso**: Número de piso
- ❌ **Torre**: Número o nombre de torre
- ❌ **Depto**: Número de departamento
- ❌ **Entre calle 1**: Primera calle de referencia
- ❌ **Entre calle 2**: Segunda calle de referencia
- ❌ **Provincia**: Provincia (separada de localidad)
- ❌ **Distrito**: Distrito/Partido

#### 4. Contacto (más detallado)
- ❌ **Código de área teléfono**: Separado del número
- ❌ **Código de área celular**: Separado del número

#### 5. Familia
- ❌ **Tiene hermanos**: SI/NO
- ❌ **Cantidad de hermanos**: Número total
- ❌ **Hermanos en el establecimiento**: Cantidad que asiste a esta escuela

#### 6. Cultural y Social
- ❌ **Lenguas distintas al castellano**: SI/NO
- ❌ **Lengua/s indígena/s**: Texto
- ❌ **Otra/s lengua/s**: Texto
- ❌ **Pertenencia a Pueblos Originarios**: SI/NO

#### 7. Beneficios Sociales
- ❌ **Asignación Universal por Hijo (AUH)**: SI/NO
- ❌ **Progresar**: SI/NO

#### 8. Transporte
- ❌ **Medio de transporte**: Múltiple selección
  - A pie/bicicleta
  - Transporte escolar DGCyE
  - Colectivo
  - Tren
  - Vehículo particular
  - Taxi/Remis
  - Otro

#### 9. Responsables (mejoras)
- ❌ **Responsable 2**: Puede haber un segundo responsable
- ❌ **Vínculo específico**: Para cada responsable (Padre, Madre, Tutor, Tutora, Otro)

---

## 📄 ALTA DOCENTE

### ✅ Campos que YA existen en el modelo Docente:
- ✅ Legajo (`legajo_numero`)
- ✅ Apellidos, Nombres (`apellido`, `nombre`)
- ✅ DNI (`dni`)
- ✅ Sexo (`sexo`)
- ✅ Fecha de Nacimiento (`fecha_nacimiento`)
- ✅ Lugar de Nacimiento (`nacionalidad` - pero no lugar específico)
- ✅ Nacionalidad (`nacionalidad`)
- ✅ Domicilio (`direccion`)
- ✅ Localidad (`direccion` - pero no separado)
- ✅ Teléfono (`telefono`)
- ✅ Celular (`celular`)
- ✅ Email (`email`)
- ✅ Fecha de ingreso a la institución (`fecha_alta`)
- ✅ Cargo (`cargo`)
- ✅ Situación de revista (`es_titular`, `es_suplente`)
- ✅ Modalidad (`modalidad`)
- ✅ Antigüedad (`anios_antiguedad`, `meses_antiguedad`)
- ✅ Horas (`horas_totales`, `horas_extension`)

### ❌ Campos FALTANTES en el modelo Docente:

#### 1. Identificación
- ❌ **CUIL**: Número de CUIL
- ❌ **Tipo de Documento**: DNI, LC, LE, etc.
- ❌ **Estado Civil**: Soltero, Casado, Divorciado, Viudo, Unión Civil

#### 2. Domicilio (más detallado)
- ❌ **Piso/Torre/Depto**: Separado
- ❌ **Código Postal**: Código postal
- ❌ **Provincia**: Provincia (separada)
- ❌ **Distrito**: Distrito/Partido

#### 3. Contacto
- ❌ **Email institucional**: Email separado del personal
- ❌ **Código de área teléfono**: Separado del número
- ❌ **Código de área celular**: Separado del número

#### 4. Datos Filiatorios
- ❌ **Apellido y nombre del padre**: Texto completo
- ❌ **Apellido y nombre de la madre**: Texto completo
- ❌ **Apellido y nombre del cónyuge**: Texto completo

#### 5. Hijos
- ❌ **Hijos**: Modelo relacionado o JSONField para hasta 5 hijos
  - Apellido y nombre
  - Fecha de nacimiento

#### 6. Títulos y Antecedentes Profesionales
- ❌ **Títulos habilitantes**: Modelo relacionado para hasta 4 títulos
  - Fecha
  - Título habilitante
  - Expedido por
  - N°Registro PBA
- ❌ **Otros títulos**: Campo de texto o modelo relacionado

#### 7. Actividad Profesional
- ❌ **Fecha de ingreso a la actividad docente**: Diferente de `fecha_alta` (que es a la institución)

#### 8. Cargos en la Institución
- ❌ **Cargos múltiples**: Modelo relacionado para hasta 4 cargos
  - Cargo
  - Situación de Revista (TIT-SUPL-PROV-POR CONTRATO)
  - Fecha de INICIO Relación Laboral
  - Fecha de FINALIZACIÓN Relación Laboral

#### 9. Otros Antecedentes
- ❌ **Otros Antecedentes de Actuación Profesional**: Modelo relacionado
  - Lugar
  - Cargo

#### 10. Grupo Familiar
- ❌ **Integrantes del Grupo Familiar**: Modelo relacionado para múltiples personas
  - Apellidos
  - Nombres
  - Tipo Doc (DNI, LC, LE, etc.)
  - Número
  - Domicilio (calle, N°, Piso/Torre/Depto)
  - Localidad
  - Código Postal
  - Tarea/Ocupación
  - Parentesco
  - Dependencia (si aplica)

---

## 📊 Resumen de Campos Faltantes

### Alumno: ~20 campos faltantes
### Docente: ~15 campos faltantes + 4 modelos relacionados

---

## 🎯 Prioridad de Implementación

### Alta Prioridad (Campos esenciales):
1. CUIL (Alumno y Docente)
2. Estado del DNI (Alumno)
3. Identidad de género ampliada (Alumno)
4. Domicilio detallado (Piso, Torre, Depto, Provincia, Distrito)
5. Email institucional (Docente)
6. Estado Civil (Docente)
7. Datos filiatorios (Docente)

### Media Prioridad:
8. Hermanos (Alumno)
9. Beneficios sociales (AUH, Progresar)
10. Transporte (Alumno)
11. Títulos habilitantes (Docente)
12. Cargos múltiples (Docente)

### Baja Prioridad:
13. Lenguas y Pueblos Originarios (Alumno)
14. Grupo familiar completo (Docente)
15. Otros antecedentes profesionales (Docente)

---

**Próximo paso:** Actualizar los modelos con los campos faltantes de alta prioridad.

