# 🚀 Guía de Deployment en Coolify

Esta guía te ayudará a desplegar la aplicación de Escáner de Códigos de Barras en tu VPS de Hostinger usando Coolify.

## 📋 Pre-requisitos

### 1. VPS Hostinger con Ubuntu 24.04 LTS
- ✅ Coolify instalado
- ✅ Docker instalado
- ✅ Git instalado

### 2. MongoDB
Tienes dos opciones:

#### Opción A: MongoDB en el mismo VPS
```bash
docker run -d \
  --name mongodb \
  --restart unless-stopped \
  -p 27017:27017 \
  -v /data/mongodb:/data/db \
  mongo:latest
```

#### Opción B: MongoDB Atlas (cloud)
1. Crear cuenta en https://www.mongodb.com/cloud/atlas
2. Crear un cluster gratuito
3. Obtener la connection string

## 🔧 Pasos de Deployment

### Paso 1: Preparar el repositorio Git

```bash
# Subir el código a tu repositorio Git (GitHub, GitLab, etc.)
git init
git add .
git commit -m "Initial commit - Barcode Scanner App"
git remote add origin <tu-url-del-repositorio>
git branch -M main
git push -u origin main
```

### Paso 2: Configurar en Coolify

1. **Login en Coolify**
   - Acceder a tu panel de Coolify en tu VPS
   - URL típica: `http://tu-vps-ip:8000`

2. **Crear nuevo proyecto**
   - Click en "New Project"
   - Nombre: "Barcode Scanner"

3. **Agregar Resource**
   - Click en "Add Resource"
   - Seleccionar "Git Repository"
   - Pegar la URL de tu repositorio Git
   - Rama: `main`

4. **Configurar Build**
   - Coolify detectará automáticamente el `Dockerfile`
   - Build Type: Dockerfile
   - Dockerfile Location: `./Dockerfile`

### Paso 3: Configurar Variables de Entorno

En la sección "Environment Variables" de Coolify, agregar:

```bash
# MongoDB Connection
MONGO_URL=mongodb://mongodb:27017
# Si usas MongoDB Atlas:
# MONGO_URL=mongodb+srv://usuario:password@cluster.mongodb.net/

# Database Name
DB_NAME=barcode_scanner

# CORS Origins (tu dominio)
CORS_ORIGINS=https://barras.facore.cloud

# Frontend Backend URL
REACT_APP_BACKEND_URL=https://barras.facore.cloud
```

### Paso 4: Configurar Dominio

1. **En tu proveedor de DNS:**
   - Crear un registro A apuntando a la IP de tu VPS:
     - Nombre: `barras` (o `@` si es dominio raíz)
     - Tipo: A
     - Valor: `<IP-de-tu-VPS>`
     - TTL: 3600

2. **En Coolify:**
   - Ir a "Domains"
   - Agregar: `barras.facore.cloud`
   - Habilitar SSL (Let's Encrypt automático)

### Paso 5: Configurar Volumen Persistente

Para mantener los archivos CSV:

1. En Coolify, ir a "Storage"
2. Agregar nuevo volumen:
   - Source: `/var/lib/coolify/barcode-scanner/data`
   - Destination: `/app/data`
   - Este volumen guardará todos los CSV generados

### Paso 6: Configurar Networking

Si MongoDB está en el mismo VPS:

1. Crear una Docker network en Coolify:
   - Nombre: `barcode-network`
2. Agregar tanto MongoDB como la app a la misma network
3. Usar `mongodb://mongodb:27017` como MONGO_URL

### Paso 7: Deploy 🚀

1. Click en "Deploy"
2. Coolify:
   - Clonará el repositorio
   - Construirá la imagen Docker
   - Creará el contenedor
   - Configurará SSL automáticamente
   - Iniciará la aplicación

3. Monitorear logs en tiempo real:
   - Ver "Deployment Logs" en Coolify

### Paso 8: Verificar Deployment

1. **Verificar que la app está corriendo:**
   ```bash
   curl https://barras.facore.cloud/api/
   ```
   Debería responder:
   ```json
   {"message": "Barcode Scanner API - Ready"}
   ```

2. **Acceder desde el navegador:**
   - Ir a https://barras.facore.cloud
   - Deberías ver la página de login

3. **Verificar MongoDB:**
   ```bash
   docker exec -it mongodb mongosh
   > show dbs
   > use barcode_scanner
   > show collections
   ```

## 🔄 Actualizar la Aplicación

### Opción 1: Desde Git (Recomendado)

```bash
# En tu máquina local
git add .
git commit -m "Update: descripción del cambio"
git push origin main

# Coolify detectará automáticamente los cambios
# O manualmente: Click en "Redeploy" en Coolify
```

### Opción 2: Webhook Automático

1. En Coolify, ir a "Webhooks"
2. Copiar la URL del webhook
3. En GitHub/GitLab:
   - Settings → Webhooks
   - Agregar la URL de Coolify
   - Seleccionar eventos: "Push"
4. Ahora cada `git push` desplegará automáticamente

## 🐛 Troubleshooting

### Problema: La app no inicia

**Solución:**
```bash
# Ver logs en Coolify o directamente:
docker logs <container-name>

# Verificar que MongoDB está corriendo:
docker ps | grep mongodb
```

### Problema: Error de conexión a MongoDB

**Solución:**
```bash
# Verificar variable MONGO_URL
# Verificar que MongoDB está accesible:
docker exec -it <app-container> ping mongodb

# Si MongoDB está en el mismo VPS:
# Asegurar que ambos contenedores están en la misma network
```

### Problema: CSS/JS no carga (404)

**Solución:**
- Verificar que el frontend se construyó correctamente
- Ver logs de build en Coolify
- Asegurar que `REACT_APP_BACKEND_URL` está correcto

### Problema: CORS Error

**Solución:**
```bash
# Verificar variable CORS_ORIGINS en Coolify
# Debe ser: https://barras.facore.cloud
# (Sin slash al final)
```

## 📊 Monitoreo

### Ver logs en tiempo real:

**En Coolify:**
- Ir a tu aplicación
- Tab "Logs"

**O directamente en el VPS:**
```bash
docker logs -f <container-name>
```

### Verificar uso de recursos:
```bash
docker stats <container-name>
```

### Acceder al contenedor:
```bash
docker exec -it <container-name> /bin/bash
```

## 💾 Backup de Datos

### Backup de MongoDB:
```bash
docker exec mongodb mongodump \
  --db=barcode_scanner \
  --out=/backup

docker cp mongodb:/backup ./backup-$(date +%Y%m%d)
```

### Backup de archivos CSV:
```bash
# Los CSV están en el volumen persistente:
cp -r /var/lib/coolify/barcode-scanner/data ./backup-csv-$(date +%Y%m%d)
```

## 🔐 Seguridad

### Recomendaciones:

1. **Firewall:**
   ```bash
   # Permitir solo puertos necesarios
   ufw allow 80/tcp   # HTTP
   ufw allow 443/tcp  # HTTPS
   ufw allow 22/tcp   # SSH
   ufw enable
   ```

2. **Actualizaciones automáticas:**
   ```bash
   apt install unattended-upgrades
   dpkg-reconfigure -plow unattended-upgrades
   ```

3. **Backup automático:**
   - Configurar cron job para backups diarios
   - Guardar en almacenamiento externo (S3, etc.)

## 📞 Soporte

Si encuentras problemas:
1. Revisar logs en Coolify
2. Verificar variables de entorno
3. Verificar conectividad a MongoDB
4. Contactar al equipo de desarrollo

## ✅ Checklist Final

- [ ] VPS configurado con Coolify
- [ ] MongoDB instalado y funcionando
- [ ] Repositorio Git configurado
- [ ] Aplicación desplegada en Coolify
- [ ] Variables de entorno configuradas
- [ ] Dominio `barras.facore.cloud` apuntando al VPS
- [ ] SSL configurado (HTTPS)
- [ ] Volumen persistente para `/app/data`
- [ ] Login con Google funcionando
- [ ] Scanner de códigos funcionando
- [ ] CSV generándose correctamente en `/app/data`
- [ ] Backup configurado

¡Listo! 🎉 Tu aplicación está funcionando en producción.
