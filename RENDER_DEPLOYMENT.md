# 🚀 Guía de Despliegue en Render

## Archivos Creados para Render

He creado los siguientes archivos para que tu aplicación funcione correctamente en Render:

### 1. **requirements.txt** (Actualizado)
- Cambié las versiones exactas (`==`) por versiones flexibles (`>=`)
- Agregué `gunicorn` para el servidor de producción
- Esto soluciona el error de "metadata-generation-failed"

### 2. **runtime.txt** (Nuevo)
- Especifica la versión de Python (3.11.0)
- Render usará esta versión para ejecutar tu aplicación

### 3. **render.yaml** (Nuevo)
- Configuración automática para Render
- Define el comando de build y start

### 4. **app.py** (Actualizado)
- Ahora usa el puerto dinámico de Render (`PORT` environment variable)
- Configurado para producción (debug=False, host='0.0.0.0')

## 📋 Pasos para Desplegar en Render

### Opción 1: Despliegue Automático (Recomendado)

1. **Ve a Render Dashboard**: https://dashboard.render.com/

2. **Crea un nuevo Web Service**:
   - Click en "New +" → "Web Service"

3. **Conecta tu repositorio**:
   - Selecciona "Connect a repository"
   - Busca: `Performance-Analyst-AE`
   - Click en "Connect"

4. **Render detectará automáticamente** el archivo `render.yaml` y configurará todo

5. **Click en "Create Web Service"**

6. **¡Listo!** Render comenzará a desplegar tu aplicación

### Opción 2: Configuración Manual

Si prefieres configurar manualmente:

1. **Información Básica**:
   - **Name**: `performance-analyst-ae`
   - **Region**: Elige la más cercana
   - **Branch**: `main`

2. **Build & Deploy**:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Environment**:
   - **Python Version**: `3.11.0`

4. **Plan**: Selecciona "Free" (o el plan que prefieras)

5. Click en **"Create Web Service"**

## ✅ Verificación del Despliegue

Una vez desplegado, Render te dará una URL como:
```
https://performance-analyst-ae.onrender.com
```

### Funcionalidades que Funcionarán:
- ✅ Subir archivos Excel
- ✅ Análisis de estudiantes
- ✅ Generación de PDFs
- ✅ Historial de análisis
- ✅ Interfaz web completa

## ⚠️ Notas Importantes

### 1. **Primer Despliegue**
El primer despliegue puede tardar 5-10 minutos

### 2. **Plan Gratuito de Render**
- La aplicación se "duerme" después de 15 minutos de inactividad
- El primer acceso después de dormir puede tardar 30-60 segundos
- Esto es normal en el plan gratuito

### 3. **Persistencia de Datos**
- Los archivos en `uploads/` y `history/` se perderán cuando Render reinicie
- Para persistencia permanente, necesitarás:
  - Usar Render Disk (plan de pago)
  - O usar almacenamiento externo (AWS S3, Cloudinary, etc.)

### 4. **Variables de Entorno** (Opcional)
Si necesitas agregar variables de entorno:
- Ve a tu servicio en Render
- Click en "Environment"
- Agrega las variables necesarias

## 🔧 Solución de Problemas

### Si el despliegue falla:

1. **Revisa los logs**:
   - En Render Dashboard → Tu servicio → "Logs"

2. **Errores comunes**:
   - **Build failed**: Verifica que `requirements.txt` esté correcto
   - **Start failed**: Verifica que `gunicorn` esté instalado
   - **Port error**: Asegúrate que `app.py` use `os.environ.get('PORT')`

3. **Re-desplegar**:
   - Render se re-despliega automáticamente con cada push a GitHub
   - O puedes hacer "Manual Deploy" desde el dashboard

## 📝 Comandos Git para Futuros Cambios

Cuando hagas cambios a tu aplicación:

```bash
cd "/Users/charliejovel/Documents/Proyectos IA/Performance Analyst"
git add .
git commit -m "Descripción de tus cambios"
git push origin main
```

Render detectará el push y re-desplegará automáticamente.

## 🎯 Próximos Pasos Recomendados

1. **Dominio Personalizado** (Opcional):
   - Puedes agregar tu propio dominio en Render
   - Settings → Custom Domains

2. **HTTPS**:
   - Render proporciona HTTPS automáticamente
   - No necesitas configurar nada

3. **Monitoreo**:
   - Revisa los logs regularmente
   - Render Dashboard muestra métricas de uso

## 📧 Soporte

Si tienes problemas:
- Revisa la documentación de Render: https://render.com/docs
- Contacta al soporte de Render
- O revisa los logs para identificar el error específico

---

**¡Tu aplicación está lista para desplegarse en Render!** 🚀
