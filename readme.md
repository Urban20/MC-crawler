# MC Crawler

Un programa para encontrar servidores de Minecraft. Escanea direcciones IP y recopila información sobre servidores activos guardandolos en una base de datos.

## Vista previa
<p align="center">
  <img src="https://i.postimg.cc/6p41sY6d/demo.png" alt="McCrawler Demo" width="800" style="border-radius: 8px">
</p>

## Qué hace

- Escanea bloques de IPs buscando servidores de Minecraft
- Detecta si los servidores son premium o permiten jugadores no premium
- Guarda la información en una base de datos local

## Cómo instalarlo

1. Descarga el código:
```bash
git clone https://github.com/Urban20/MC-crawler.git
cd MC-crawler/src/MC-crawler
```

2. Instala lo necesario:
```bash
pip install -r requirements.txt
```

3. Consigue el archivo `escan` (escáner de IPs):
   - Windows: Descarga `escan.exe` [click](https://github.com/Urban20/MC-crawler/releases)
   - Linux: Compílalo vos mismo con Go:

   `1. instalar Golang`

   `2. acceder a la carpeta de escaneos/`

   `3. ejecutar el comando`: 
   ```
   go build .
   
   ```
   `4. arrastrar el bonario generado a la carpeta principal (MC-crawler/)`
   
   

4. Ejecuta:
```bash
python main.py
```
ó

instalalo compilado para Windows (version .exe): [click](https://github.com/Urban20/MC-crawler/releases)

## Cómo se usa

Opciones: 

- **Barrido**: Busca nuevos servidores
- **Purgar**: Elimina servidores que ya no están online
- **Buscar**: Encuentra servidores no premium
- **Buscar versión**: Filtra por versión de Minecraft

## Base de datos

El programa guarda la información en dos archivos:
- `servers.db`: Todos los servidores encontrados
- `crackeados.db`: Servidores que permiten jugadores no premium

## Notas importantes

- El antivirus puede bloquear el escáner (es falso positivo)
- Los escaneos generan tráfico de red - úsalo responsablemente
- No abuses de los escaneos para no saturar tu conexión

**Autor**: Urb@n (Matias Urbaneja)  
**GitHub**: https://github.com/Urban20
