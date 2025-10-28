# 🚨 Reporte de Error - Instalación SDK Facephi

## 📋 Información del Error

**Fecha**: 28 de octubre de 2025  
**Comando**: `npm install @facephi/sdk-web-fphi`  
**Error**: E401 - Incorrect or missing password  
**Registry**: https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/

## 🔍 Detalles Técnicos

### Error Principal:
```
HttpErrorAuthUnknown: Unable to authenticate, need: Basic realm="Artifactory Realm"
```

### Código de Error:
```
error code E401
error Incorrect or missing password.
```

### URL que falla:
```
http fetch GET 401 https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/@facephi%2fsdk-web-fphi
```

## 🔑 Credenciales Utilizadas

### Usuario 1:
- **Username**: `maybecloudes01`
- **Token Short**: `cmVmdGtuOjAxOjAwMDAwMDAwMDA6YVpvM2l6c2NuTDJycUJvQVhDYnJPVExXYlhm`
- **Token B64**: `Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllWcHZNMmw2YzJOdVRESnljVUp2UVZoRFluSlBWRXhYWWxobQ==`

### Usuario 2:
- **Username**: `maybecloudes02`
- **Token Short**: `cmVmdGtuOjAxOjAwMDAwMDAwMDA6YUJsVGxkNlpEZXhIa01RRDRINzRZUkJVcjNv`
- **Token B64**: `Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllVSnNWR3hrTmxwRVpYaElhMDFSUkRSSU56UlpVa0pWY2pOdg==`

## ⚙️ Configuración .npmrc

```bash
# Facephi registry credentials (prod)
@facephi:registry=https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/
//facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/:_auth=Y21WbWRHdHVPakF4T2pBd01EQXdNREF3TURBNllWcHZNMmw2YzJOdVRESnljVUp2UVZoRFluSlBWRXhYWWxobQ==
//facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/:username=maybecloudes01
//facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/:email=maybecloudes01@facephi.com
```

## 🔧 Entorno de Desarrollo

- **Sistema Operativo**: Windows NT 10.0.26220
- **Node.js**: v25.0.0
- **npm**: v11.6.2
- **Directorio**: C:\Users\AndreuSerra\source\Python\ControlDocumentos

## 📊 Log Completo

```
0 verbose cli C:\Program Files\nodejs\node.exe C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js
1 info using npm@11.6.2
2 info using node@v25.0.0
3 silly config load:file:C:\Program Files\nodejs\node_modules\npm\npmrc
4 silly config load:file:C:\Users\AndreuSerra\source\Python\ControlDocumentos\.npmrc
5 silly config load:file:C:\Users\AndreuSerra\.npmrc
6 silly config load:file:C:\Users\AndreuSerra\AppData\Roaming\npm\etc\npmrc
7 verbose title npm install @facephi/sdk-web-fphi
8 verbose argv "install" "@facephi/sdk-web-fphi"
9 verbose logfile logs-max:10 dir:C:\Users\AndreuSerra\AppData\Local\npm-cache\_logs\2025-10-28T20_38_41_463Z-
10 verbose logfile C:\Users\AndreuSerra\AppData\Local\npm-cache\_logs\2025-10-28T20_38_41_463Z-debug-0.log
11 silly logfile start cleaning logs, removing 1 files
12 silly packumentCache heap:4496293888 maxSize:1124073472 maxEntrySize:562036736
13 silly logfile done cleaning log files
14 silly idealTree buildDeps
15 silly fetch manifest @facephi/sdk-web-fphi@*
16 silly packumentCache full:https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/@facephi%2fsdk-web-fphi cache-miss
17 http fetch GET 401 https://facephicorp.jfrog.io/artifactory/api/npm/sdk-web-fphi/@facephi%2fsdk-web-fphi 359ms (cache skip)
18 silly placeDep ROOT @facephi/sdk-web-fphi@ OK for:  want: *
19 verbose stack HttpErrorAuthUnknown: Unable to authenticate, need: Basic realm="Artifactory Realm"
19 verbose stack     at C:\Program Files\nodejs\node_modules\npm\node_modules\npm-registry-fetch\lib\check-response.js:88:17
19 verbose stack     at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
19 verbose stack     at async RegistryFetcher.packument (C:\Program Files\nodejs\node_modules\npm\node_modules\pacote\lib\registry.js:90:19)
19 verbose stack     at async RegistryFetcher.manifest (C:\Program Files\nodejs\node_modules\npm\node_modules\pacote\lib\registry.js:128:23)
19 verbose stack     at async #fetchManifest (C:\Program Files\nodejs\node_modules\npm\node_modules\@npmcli\arborist\lib\arborist\build-ideal-tree.js:1227:20)
19 verbose stack     at async #nodeFromEdge (C:\Program Files\nodejs\node_modules\npm\node_modules\@npmcli\arborist\lib\arborist\build-ideal-tree.js:1065:19)
19 verbose stack     at async #buildDepStep (C:\Program Files\nodejs\node_modules\npm\node_modules\@npmcli\arborist\lib\arborist\build-ideal-tree.js:929:11)
19 verbose stack     at async Arborist.buildIdealTree (C:\Program Files\nodejs\node_modules\npm\node_modules\@npmcli\arborist\lib\arborist\build-ideal-tree.js:182:7)
19 verbose stack     at async Promise.all (index 1)
19 verbose stack     at async Arborist.reify (C:\Program Files\nodejs\node_modules\npm\node_modules\@npmcli\arborist\lib\arborist\reify.js:114:5)
20 verbose statusCode 401
21 verbose pkgid @facephi/sdk-web-fphi@*
22 error code E401
23 error Incorrect or missing password.
24 error If you were trying to login, change your password, create an
24 error authentication token or enable two-factor authentication then
24 error that means you likely typed your password in incorrectly.
24 error Please try again, or recover your password at:
24 error   https://www.npmjs.com/forgot
24 error
24 error If you were doing some other operation then your saved credentials are
24 error probably out of date. To correct this please try logging in again with:
24 error   npm login
25 silly unfinished npm timer reify 1761683923837
26 silly unfinished npm timer reify:loadTrees 1761683923852
27 verbose cwd C:\Users\AndreuSerra\source\Python\ControlDocumentos
28 verbose os Windows_NT 10.0.26220
29 verbose node v25.0.0
30 verbose npm  v11.6.2
31 verbose exit 1
32 verbose code 1
33 error A complete log of this run can be found in: C:\Users\AndreuSerra\AppData\Local\npm-cache\_logs\2025-10-28T20_38_41_463Z-debug-0.log
```

## 🎯 Posibles Causas

1. **Credenciales expiradas** o desactivadas
2. **Permisos insuficientes** para acceder al registry
3. **Token de autenticación** incorrecto o mal formateado
4. **Configuración de Artifactory** que requiere autenticación adicional
5. **Problemas de conectividad** con el registry

## 📞 Acción Requerida

Por favor, verificar:
- ✅ **Estado de las credenciales** (activas/expiradas)
- ✅ **Permisos de acceso** al registry npm
- ✅ **Formato correcto** del token de autenticación
- ✅ **Configuración de Artifactory** para npm registry

## 📧 Información de Contacto

**Desarrollador**: Andreu Serra  
**Proyecto**: Control de Documentos  
**Fecha del Error**: 28/10/2025 20:38:41 UTC
