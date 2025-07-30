# MC-crawler 🕹️🌍  

## ¿Qué es esto? 🔍  

**MC-crawler** es un explorador que rastrea servidores de *Minecraft Java Edition* por todo el mundo. Un rastreador simple pero efectivo de servidores tanto públicos como ocultos (pensado para jugar unicamente entre amigos)


## Para qué sirve 🚀  
- 🎯 **Descubrir servidores** activos en cualquier país  
- 📊 **Analizar información clave**: jugadores online, versión, MOTD  
- 🔍 **Buscar por palabras clave (tags)** (ej: "survival", "minigames")  
- 🌐 **Detectar servidores "ocultos"** mediante escaneo de redes  

---

## Características únicas   

### 1. Doble método de rastreo  
```python
# Método 1: Búsqueda inteligente (menos intrusiva)
bot = Crawler(tag="minecraft")
for ip, país in bot.info():
    # Verifica servidor...

# Método 2: 
ejecutar_barrido()  # Usa binario Go para máxima velocidad
```

### 2. Interfaz simple
### Imagen de la Interfaz:

<p align="center">
  <img src="https://i.postimg.cc/TYgkm314/demo.png" alt="demo" width="800">
</p>

### 3. Guardado persistente
```markdown
| IP             | País       | Versión    |
| x.x.1.5        | Argentina  | 1.19.4     | 
| 104.129.x.x    | USA        | 1.20.1     | 
| 89.203.12.x    | Alemania   | 1.18.2     | 
```

---

## Requisitos e instalación ⬇️  

Abrí la consola (cmd o powershell) y escribí lo suguiente:

1. Cloná el repo:
```bash
git clone https://github.com/Urban20/MC-crawler.git # asumiendo que git está en tu sistema

cd "MC-crawler\src\MC-crawler"

```
2. Instalá dependencias:  
```bash
pip install -r requirements.txt
```


3. Ejecutá:  
```bash
python main.py
```

> 💡 **Tip:** Para el modo escaneo necesitas el binario `escan.exe` 

---

## Ética de uso ⚖️  

- 🔒 Solo escanear redes propias o con permiso  
- 📵 Nunca saturar servidores  

---