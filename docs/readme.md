# MC Crawler

### Idiomas:

[ENGLISH](https://github.com/Urban20/MC-crawler/tree/main/docs/readme_en.md) 

##

MC Crawler apunta a ser un programa de linea de comandos cuyo objetivo es llevar un registro de servidores de Minecraft Java.

Su funcionamiento general es el siguiente:
- obtiene rangos de ips ocupados por hostings
- selecciona algunos rangos al azar y ejecuta un escaneo de puertos con un rango de /16 cada uno
- envia una serie de paquetes especificos utilizados para comunicarse con este tipo de servidores
- envia un bot el cual simula un jugador y se conecta de forma automatica al servidor objetivo sin completar el login. En base a la respuesta se puede inferir con bastante exactitud si el servidor es premium o no premium, si tiene mods, withelist e incluso si el bot fue baneado.

NOTA: el programa puede actualizar la base de datos de forma automatica. 


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

3. Conseguir el archivo `escan` (escáner de IPs) (parte critica del programa, sin esto el programa no funciona como debe hacerlo):
   - Windows: Descarga `escan.exe` [click](https://github.com/Urban20/MC-crawler/releases) 
   - Linux: Compílalo vos mismo con Go (necesitas el binario especifico de tu distribucion):

   `1. instalar Golang`

   `2. acceder a la carpeta de escaneos/`

   `3. ejecutar el comando`: 
   ```
   go build .
   
   ```
   `4. arrastrar el binario generado a la siguiente carpeta: MC-crawler/escaner/binario`
   
   
4. Una vez creado el entorno virtual e instalado las dependencias 

Ejecutar:
```bash
python main.py
```
ó

instalalo compilado para Windows (version .exe):
el cual viene listo para usar [click aca](https://github.com/Urban20/MC-crawler/releases)

## Cómo se usa

Opciones: 

- **Barrido**: Busca nuevos servidores (ejecuta la obtencion de rangos ips y el escaneo)
- **Purgar**: Elimina servidores que ya no están online
- **Buscar**: Encuentra servidores no premium
- **Buscar versión**: Filtra por versión de Minecraft

## Base de datos

El programa guarda la información en dos archivos:
- `servers.db`: Todos los servidores encontrados
- `crackeados.db`: Servidores que permiten jugadores no premium

## Notas importantes

- Los escaneos generan tráfico de red - usar responsablemente
- No abuses de los escaneos para no saturar tu conexión
- El proyecto es extensible y admite modificaciones por parte de terceros, permitiendo su adaptación a nuevos casos de uso o funcionalidades **mas no me hago responsable de las modificaciones o mal uso que se le dé a la herramienta.**

## Cosas a implementar en un futuro

- mejora de rendimiento y concurrencia por parte de los modulos escritos en python
- soporte de lenguajes
- adicion de escaneos de rango de /8 (8 bits)



**Autor**: Urb@n

**GitHub**: https://github.com/Urban20