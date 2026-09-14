## Install WSL

## Install spoofdpi

In cmd:

```cmd
curl -fsSL https://raw.githubusercontent.com/xvzc/spoofdpi/main/install.sh -o install.sh
```

Output:

```output
Resolving latest version ...
Downloading spoofdpi_1.5.3_linux_x86_64. tar.gz ...
Extracting.
Installing to /usr/local/bin ...
Admin permission required to install to /usr/local/bin
[sudo] password for ubuntu:
```
Enter password and press `enter`

```output
Successfully installed spoofdpi v1.5.3 to /usr/local/bin/spoofdpi
```

#### Run the install.sh

```cmd
bash install.sh linux-amd64
```

#### delete the install.sh

```cmd
del install.sh
```

## Start & Stop

Run the start.bat to start SpoofDPI, let the `spoofdpi terminal` stay open

Run the stop.bat to stop, it can be run whenever, no matter spoofdpi is running or not
