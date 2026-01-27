# MC Crawler

MC Crawler aims to be a command-line program whose purpose is to keep a record of Minecraft Java servers.

Its general operation is as follows:
- obtains IP ranges occupied by hosting providers
- selects some ranges at random and performs a port scan using a /16 range for each
- sends a series of specific packets used to communicate with this type of servers
- deploys a bot that simulates a player and automatically connects to the target server without completing the login. Based on the response, one can infer with high accuracy whether the server is premium or non-premium, if it has mods, a whitelist, and even if the bot was banned.

NOTE: the program can update the database automatically.


## How to install

1. Download the code:
```bash
git clone https://github.com/Urban20/MC-crawler.git
cd MC-crawler/src/MC-crawler
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Obtain the `escan` file (IP scanner) (critical part of the program — without this the program does not work as intended):
   - Windows: Download `escan.exe` [click](https://github.com/Urban20/MC-crawler/releases)
   - Linux: Compile it yourself with Go (you need the binary specific to your distribution):

   `1. install Golang`

   `2. go to the scans/ folder`

   `3. run the command`:
   ```
   go build .
   ```
   `4. move the generated binary to following folder: MC-crawler/escaner/binario`


4. Run:
```bash
python main.py
```
or

install the compiled Windows version (an .exe) which comes ready to use [click here](https://github.com/Urban20/MC-crawler/releases)

## How to use

Options:

- **Sweep**: Searches for new servers (performs IP range retrieval and scanning)
- **Purge**: Removes servers that are no longer online
- **Search**: Finds non-premium servers
- **Search version**: Filters by Minecraft version

## Database

The program stores information in two files:
- `servers.db`: All discovered servers
- `crackeados.db`: Servers that allow non-premium players

## Important notes

- Scans generate network traffic — use responsibly
- Do not abuse the scans to avoid saturating your connection
- The project is extensible and accepts modifications by third parties, allowing adaptation to new use cases or features **but I do not take responsibility for modifications or misuse of the tool.**

## Things to implement in the future

- performance and concurrency improvements in the modules written in Python
- language support
- addition of /8 range scans (8 bits)


**Author**: Urb@n

**GitHub**: https://github.com/Urban20
