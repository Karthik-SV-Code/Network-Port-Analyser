# Network Port Scanner GUI

A lightweight TCP port scanner with a graphical user interface built using Python and Tkinter. The application allows users to scan a target system, detect open ports, and view results in real time.

## Features

- Simple interface – enter a target host, start port, and end port  
- TCP-based scanning – uses socket connections to detect open ports  
- Service identification – labels common ports (FTP, SSH, HTTP, HTTPS, SMB, etc.)  
- Risk level classification – categorizes ports as High, Medium, or Low  
- Real-time progress – progress bar and scan status update during scanning  
- Live statistics – displays open port count and scan duration  
- Stop at any time – cancel a running scan gracefully  
- Save results – export discovered open ports to a `.txt` file  
- Quick scan option – automatically sets port range (1–1024)  
- Clear results – reset the interface easily  
- Cross-platform – runs on Windows, macOS, and Linux  

## Requirements

- Python 3.7 or newer  
- Tkinter (included in the standard Python distribution; on Debian/Ubuntu install `python3-tk`)  

No third-party packages are required.

## Installation

```bash
git clone https://github.com/your-username/port-scanner.git
cd port-scanner
```

## Usage

```bash
python port.py
```

1. Enter the **Target** – an IP address (e.g. `127.0.0.1`) or hostname (e.g. `google.com`).  
2. Set the **Start Port** and **End Port** (defaults: `1` – `1024`).  
3. Click **Start Scan**. Open ports appear in real time in the results table.  
4. Click **Stop** to cancel a scan early.  
5. After completion, click **Export** to save results to a text file.  
6. Use **Quick Scan** for common ports.  
7. Click **Clear** to reset the interface.  

## Detected Services

The following ports are automatically labelled:

| Port | Service |
|------|--------|
| 21   | FTP    |
| 22   | SSH    |
| 23   | Telnet |
| 25   | SMTP   |
| 53   | DNS    |
| 80   | HTTP   |
| 443  | HTTPS  |
| 445  | SMB    |
| 3306 | MySQL  |
| 3389 | RDP    |

Ports not in the list are reported as `Unknown`.

## Project Structure

```
port-scanner/
├── port.py       # Main application (scanner + GUI)
└── README.md
```

## Disclaimer

Use this tool only on hosts and networks you own or have explicit permission to scan. Unauthorized port scanning may be illegal in your jurisdiction.

## License

This project is released under the MIT License.
