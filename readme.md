# MC-crawler 

Es un rastreador de servidores de Minecraft Java, tanto públicos como privados (servidores pensados para jugar entre amigos).

Rastrea servidores en todo el mundo con ayuda de fuentes abiertas basandose en palabras clave de las descripciones de los servidores y escaneos de grandes cantidades de bloques de direcciones ips asociadas a hostings de plataformas en el puerto 25565.

La informacion obtenida de dichos servidores se aloja en una base de datos que puede ser consultada segun las versiones o pais de origen del servidor a investigar



## Características

#### 1. Doble método de rastreo  
```python
# Método 1: Búsqueda por fuentes públicas
bot = Crawler(tag="minecraft")
for ip, país in bot.info():
    # Verifica servidor...

# Método 2: 
ejecutar_barrido()  # Usa binario de Go para escanear bloques de ipv4 por cuenta propia
```

#### 2. Interfaz simple


<p align="center">
  <img src="https://i.postimg.cc/cLnHkpN7/demo.png)](https://postimg.cc/nXnpCwrM" alt="demo" width="800">
</p>

#### 3. Guardado en base de datos sqlite
```markdown
| IP             | País       | Versión    |
| x.x.1.5        | Argentina  | 1.19.4     | 
| 104.129.x.x    | USA        | 1.20.1     | 
| 89.203.12.x    | Alemania   | 1.18.2     | 
```

---

#### 4. Actualizacion de servidores
permite verificar si un servidor ya no se encuentra online, de ser asi lo elimina de la db.

También permite actualizar las versiones de los servidores que siguen en linea pero que modificaron su versión

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

> 💡 **Tip:** Para el modo escaneo necesitas el binario `escan.exe` , podés obtenerlo en  https://github.com/Urban20/MC-crawler/releases

---
