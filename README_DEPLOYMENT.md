# QRE - Escáner de Códigos QR con Emergent

Aplicación web para escanear códigos QR usando la cámara del celular y almacenarlos en archivos CSV.

## 🚀 Deployment en Coolify

### Pre-requisitos

1. **VPS con Ubuntu 24.04 LTS**
2. **Coolify instalado** (https://coolify.io/docs/installation)
3. **MongoDB** (en el mismo VPS o MongoDB Atlas)
4. **Dominio apuntando al VPS:** barras.facore.cloud

### Variables de Entorno Requeridas

Configurar en Coolify:

```bash
# Backend
MONGO_URL=mongodb://localhost:27017
DB_NAME=barcode_scanner
CORS_ORIGINS=https://barras.facore.cloud

# Frontend
REACT_APP_BACKEND_URL=https://barras.facore.cloud
WDS_SOCKET_PORT=443
ENABLE_HEALTH_CHECK=false
```

### MongoDB

**Opción A: MongoDB en el mismo VPS**
```bash
docker run -d \
  --name mongodb \
  --restart unless-stopped \
  -p 27017:27017 \
  -v /data/mongodb:/data/db \
  mongo:latest
```

**Opción B: MongoDB Atlas (cloud)**
- Crear cuenta en https://www.mongodb.com/cloud/atlas
- Crear cluster gratuito
- Copiar connection string a `MONGO_URL`

### Deployment

1. **En Coolify:**
   - New Resource → Git Repository
   - Conectar repositorio: https://github.com/[tu-usuario]/qre
   - Branch: main

2. **Build Configuration:**
   - Coolify detectará el Dockerfile automáticamente
   - Build Type: Dockerfile
   - Dockerfile Location: ./Dockerfile

3. **Variables de Entorno:**
   - Agregar las variables listadas arriba

4. **Dominio:**
   - Configurar: barras.facore.cloud
   - Habilitar SSL automático (Let's Encrypt)

5. **Volumen Persistente:**
   - Source: `/var/lib/coolify/qre/data`
   - Destination: `/app/data`

6. **Deploy:**
   - Click "Deploy"
   - Coolify construirá y desplegará automáticamente

### URLs

- **Producción:** https://barras.facore.cloud
- **API:** https://barras.facore.cloud/api/

### Archivos CSV

Los archivos CSV se guardan en: `/app/data/barras_YYYYMMDD_v{n}.csv`

Formato:
```csv
timestamp,codigo,usuario
2025-01-30 10:30:45,PROD-12345,user@example.com
```

### Características

- ✅ Login con Google (Emergent OAuth)
- ✅ Scanner de QR con cámara del celular
- ✅ Detección automática con pausa inteligente
- ✅ Cuadro de lectura vertical (etiquetas 3×5 cm)
- ✅ Contador de lecturas en tiempo real
- ✅ Detección de duplicados
- ✅ Generación de CSV con múltiples versiones por día
- ✅ Diseño responsive con paleta marrón
- ✅ Todo en español

### Stack Técnico

- **Frontend:** React 19 + html5-qrcode + Tailwind CSS
- **Backend:** FastAPI (Python 3.11)
- **Base de datos:** MongoDB
- **Autenticación:** Emergent OAuth (Google)
- **Deployment:** Docker + Coolify

### Documentación

- 📖 [README.md](./README.md) - Documentación técnica completa
- 🚀 [COOLIFY_DEPLOYMENT.md](./COOLIFY_DEPLOYMENT.md) - Guía detallada de deployment
- 📱 [QUICK_START.md](./QUICK_START.md) - Guía de usuario
- 🔧 [SCANNER_TROUBLESHOOTING.md](./SCANNER_TROUBLESHOOTING.md) - Solución de problemas

### Soporte

Para dudas o problemas:
1. Revisar documentación en el repositorio
2. Verificar logs en Coolify
3. Verificar variables de entorno
4. Verificar conectividad a MongoDB

### Licencia

Propietario - Todos los derechos reservados

---

**Desarrollado con ❤️ usando FastAPI, React y html5-qrcode**
