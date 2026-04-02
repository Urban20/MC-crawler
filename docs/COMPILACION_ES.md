# MC-Crawler — Guía de Compilación

## Lo que necesitás tener instalado

- **Python** → https://www.python.org/downloads/
- **Go** → https://go.dev/dl/

---

## Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/Urban20/MC-crawler.git
cd MC-crawler/src/MC-crawler
```

---

## Paso 2 — Compilar el escaner de IPs (`escan`)

El programa depende de un componente escrito en Go que se encarga de escanear IPs. Sin este no funciona.

**Windows:** Descargá `escan.exe` desde los [releases del repositorio](https://github.com/Urban20/MC-crawler/releases) y colocalo en la carpeta `escaner/binario/`.

**Linux:** Compilalo vos mismo desde la carpeta del proyecto:

```bash
cd escaner/golang
go build .
mv escan ../binario/
```

---

## Paso 3 — Instalar dependencias

**Windows:**
```powershell
scripts\dependencias.bat
```

**Linux:**
```bash
chmod +x scripts/*.sh
./scripts/dependencias.sh
```

---

## Paso 4 — Compilar MC-Crawler

**Windows:**
```powershell
scripts\compilar.bat
```

**Linux:**
```bash
./scripts/compilar.sh
```

El ejecutable final queda en la carpeta `MC-crawler.dist/` que se genera automáticamente.

---

## ¿Solo querés ejecutarlo sin compilar?

**Windows:** `scripts\iniciar.bat`

**Linux:** `./scripts/iniciar.sh`
