# 🚀 Guía Rápida de Inicio

## ¿Qué es esta aplicación?

Una aplicación web para **escanear códigos de barras** usando la cámara del celular y guardarlos en archivos CSV. Perfecta para inventarios, almacenes, y control de productos.

---

## ✨ Características Principales

- 📷 **Escanea con tu celular** - Usa la cámara para leer códigos
- 🔐 **Login con Google** - Seguro y fácil
- 💾 **Guarda en CSV** - Archivos organizados por fecha
- 🔢 **Contador en tiempo real** - Ve cuántos códigos has escaneado
- ⚠️ **Detecta duplicados** - Te avisa si escaneas el mismo código dos veces
- 🎨 **Diseño profesional** - Paleta de colores marrón elegante

---

## 📱 Cómo Usar la Aplicación

### 1. Iniciar Sesión
1. Abre la aplicación en tu navegador
2. Click en "Iniciar sesión con Google"
3. Selecciona tu cuenta de Google
4. Serás redirigido a la página de escaneo

### 2. Escanear Códigos
1. Permite el acceso a la cámara cuando el navegador lo solicite
2. Apunta la cámara al código de barras
3. El código se escaneará automáticamente
4. Verás una alerta ✅ confirmando el escaneo
5. El contador aumentará en +1

### 3. Continuar Escaneando
- Después de cada escaneo exitoso, el botón "Próximo" se activará
- Click en "Próximo" para escanear el siguiente código
- Repite el proceso para cada producto

### 4. Finalizar Sesión
1. Cuando termines, click en "Finalizar"
2. Aparecerá un modal de confirmación
3. Confirma para generar el archivo CSV
4. El archivo se guardará automáticamente en el servidor

### 5. Archivos CSV
Los archivos se crean en `/app/data/` con este formato:
- Nombre: `barras_20260228_v1.csv` (fecha + versión)
- Contenido:
  ```csv
  timestamp,codigo,usuario
  2026-02-28 10:30:45,1234567890123,tu-email@gmail.com
  ```

---

## 🔧 Deployment en Tu Servidor

### Opción A: Coolify (Recomendado)

1. **Subir a Git:**
   ```bash
   git init
   git add .
   git commit -m "Barcode Scanner App"
   git push origin main
   ```

2. **En Coolify:**
   - Nuevo proyecto → Git Repository
   - Seleccionar tu repositorio
   - Coolify detectará el Dockerfile automáticamente

3. **Variables de entorno:**
   ```bash
   MONGO_URL=mongodb://mongodb:27017
   DB_NAME=barcode_scanner
   CORS_ORIGINS=https://barras.facore.cloud
   REACT_APP_BACKEND_URL=https://barras.facore.cloud
   ```

4. **Configurar dominio:**
   - DNS: `barras.facore.cloud` → IP del VPS
   - En Coolify: Agregar dominio + SSL automático

5. **Deploy:**
   - Click "Deploy" y esperar
   - ¡Listo! Tu app estará en https://barras.facore.cloud

### Documentación Completa:
📖 Ver `/app/COOLIFY_DEPLOYMENT.md` para guía detallada paso a paso

---

## 💡 Consejos de Uso

### Para mejores resultados al escanear:
- ✅ Buena iluminación
- ✅ Mantén el código de barras plano
- ✅ Distancia de 10-20 cm de la cámara
- ✅ Evita reflejos en códigos brillantes
- ✅ Usa la cámara trasera del celular (mejor calidad)

### Gestión de sesiones:
- Cada sesión puede tener múltiples códigos
- Finaliza la sesión cuando termines un lote
- Puedes iniciar una nueva sesión inmediatamente
- Se crean múltiples archivos CSV por día (v1, v2, v3...)

### Códigos duplicados:
- Si escaneas el mismo código dos veces, verás una alerta ⚠️
- El código se guardará de todas formas
- Útil para contar cantidades del mismo producto

---

## 📊 Tipos de Códigos Soportados

La aplicación lee **TODOS** estos formatos:

- ✅ EAN-13 (productos comerciales)
- ✅ EAN-8
- ✅ UPC-A (productos USA)
- ✅ UPC-E
- ✅ Code 128
- ✅ Code 39
- ✅ Code 93
- ✅ QR Code
- ✅ Data Matrix
- ✅ PDF-417
- ✅ Y más...

---

## 🐛 Solución de Problemas

### La cámara no funciona:
1. Verifica permisos del navegador
2. Usa HTTPS (requerido para acceso a cámara)
3. Intenta recargar la página
4. Prueba con otro navegador (Chrome recomendado)

### El código no se escanea:
1. Mejora la iluminación
2. Limpia la lente de la cámara
3. Verifica que el código esté completo y legible
4. Acércate o aléjate del código

### Error al guardar:
1. Verifica tu conexión a internet
2. Verifica que estés autenticado
3. Recarga la página e intenta nuevamente

### No aparece el botón de login:
1. Limpia caché del navegador
2. Verifica que la URL sea correcta
3. Verifica que el backend esté funcionando

---

## 📁 Estructura de Archivos

```
/app/
├── backend/              # API en FastAPI
│   ├── server.py        # Servidor principal
│   └── requirements.txt # Dependencias Python
├── frontend/            # App React
│   ├── src/            # Código fuente
│   └── package.json    # Dependencias Node
├── data/               # ⭐ Archivos CSV aquí
│   ├── barras_20260228_v1.csv
│   └── barras_20260228_v2.csv
├── Dockerfile          # Para deployment
├── README.md           # Documentación técnica
└── COOLIFY_DEPLOYMENT.md  # Guía de deployment
```

---

## 📞 Contacto y Soporte

### Documentación disponible:
- 📖 `/app/README.md` - Info técnica completa
- 🚀 `/app/COOLIFY_DEPLOYMENT.md` - Deployment en Coolify
- ✅ `/app/IMPLEMENTATION_SUMMARY.md` - Resumen de implementación
- 🧪 `/app/auth_testing.md` - Testing de autenticación

### Verificar funcionamiento:
```bash
# Backend API
curl https://barras.facore.cloud/api/

# Ver archivos CSV generados
ls -lh /app/data/

# Ver logs
docker logs <container-name>
```

---

## ✅ Checklist Pre-Producción

Antes de usar en producción:

- [ ] Aplicación desplegada en servidor
- [ ] Dominio configurado (https://barras.facore.cloud)
- [ ] SSL/HTTPS activado
- [ ] MongoDB funcionando
- [ ] Volumen persistente para `/app/data`
- [ ] Backup automático configurado
- [ ] Autenticación Google probada
- [ ] Escaneo de códigos probado
- [ ] Generación de CSV verificada
- [ ] Acceso desde celular verificado

---

## 🎉 ¡Listo para Usar!

Tu aplicación de escaneo de códigos de barras está completamente funcional y lista para:

✨ Escanear productos  
✨ Llevar inventarios  
✨ Controlar entradas/salidas  
✨ Generar reportes en CSV  
✨ Usar desde cualquier celular  

**¡Comienza a escanear ahora! 📦📱**

---

*Desarrollado con ❤️ usando FastAPI, React y html5-qrcode*
