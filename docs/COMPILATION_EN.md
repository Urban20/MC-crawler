# MC-Crawler — Build Guide

## What you need installed

- **Python** → https://www.python.org/downloads/
- **Go** → https://go.dev/dl/

---

## Step 1 — Clone the repository

```bash
git clone https://github.com/Urban20/MC-crawler.git
cd MC-crawler/src/MC-crawler
```

---

## Step 2 — Build the IP scanner (`escan`)

The program depends on a Go component that handles IP scanning. Without it, the program won't work.

**Windows:** Download `escan.exe` from the [repository releases](https://github.com/Urban20/MC-crawler/releases) and place it in the `escaner/binario/` folder.

**Linux:** Build it yourself from the project folder:

```bash
cd escaner/golang
go build .
mv escan ../binario/
```

---

## Step 3 — Install dependencies

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

## Step 4 — Compile MC-Crawler

**Windows:**
```powershell
scripts\compilar.bat
```

**Linux:**
```bash
./scripts/compilar.sh
```

The final executable will be inside the `MC-crawler.dist/` folder that gets created automatically.

---

## Just want to run it without compiling?

**Windows:** `scripts\iniciar.bat`

**Linux:** `./scripts/iniciar.sh`
