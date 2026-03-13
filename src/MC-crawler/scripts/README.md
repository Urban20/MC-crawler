# Scripts de Inicio y Compilación

Carpeta con scripts para iniciar el programa y compilar ejecutables en Windows y Linux.

**Ejecutar SIEMPRE desde: MC-crawler/** (raíz del proyecto)

## Windows (.bat)

- **dependencias.bat**: Crea el entorno virtual e instala todas las dependencias
- **iniciar.bat**: Activa el entorno virtual y ejecuta el programa
- **compilar.bat**: Compila el programa a ejecutable .exe usando Nuitka

### Uso en Windows (desde MC-crawler/):
```powershell
cd MC-crawler
scripts\dependencias.bat
scripts\iniciar.bat
scripts\compilar.bat
```

## Linux (.sh)

- **dependencias.sh**: Crea el entorno virtual e instala todas las dependencias
- **iniciar.sh**: Activa el entorno virtual y ejecuta el programa
- **compilar.sh**: Compila el programa a ejecutable usando Nuitka

### Uso en Linux (desde MC-crawler/):
```bash
cd MC-crawler
chmod +x scripts/*.sh
./scripts/dependencias.sh
./scripts/iniciar.sh
./scripts/compilar.sh
```

## Notas

- Los scripts deben ejecutarse siempre desde la raíz del proyecto (MC-crawler/)
- Los scripts automáticamente se posicionan en la raíz y tienen acceso a todos los recursos
- Los scripts de dependencias deben ejecutarse primero
- En Linux, es necesario hacer los archivos .sh ejecutables con `chmod +x`
- El entorno virtual se crea en la raíz del proyecto bajo el nombre `env`
