# Finals Key Extractor

## Requisites

1. Install Python 3.10
2. Install Wireshark to `C:\Program Files\Wireshark` (should be the default install directory)
3. [Setup SSLKEYLOG file](#setup-sslkeylog-file)

## Setup

1. Either clone the repository using git or download it
2. Run it

```shell
python3 main.py
```

3. After running it, it will promt you to select an interface. Select the interface that you're connected to the internet with. Wi-Fi if using Wi-Fi, Ethernet if using a cable.
4. Open up The Finals and the program should start capturing data.

## Output

### `Auth token captured`

This message means that the program has detected an jwt token and it will be written to `token.txt`

### `Stats file captured`

This means that the program has captured all the data needed to fill the stats file. This file is saved in the project root as `stats.json`

## How does it work?

Internally this project uses tshark or [Terminal-based Wireshark](https://www.wireshark.org/docs/wsug_html_chunked/AppToolstshark.html) to listen to the traffic on your network and then decrypts that traffic using `SSLKEYLOGFILE`.

It then waits until it can hear traffic belonging to embark. When it detects that a request belonging to embark has been made, it reads the headers on the request. In the headers it's looking for a JWT token, if it finds the token, then that token gets written to the `token.txt` file.

## Setup SSLKEYLOG file

1. Press WIN, type in `Edit the system environment variables` and press ENTER.

![system-properties.png](./docs/assets/system-properties.png)

2. Press on `Environment Variables...`.

![environment-variables.png](./docs/assets/environment-variables.png)

3. Under the `System variables` section press on new, set variable name as `SSLKEYLOGFILE` and value as any valid path to file. As an example `C:\Users\<username>\Documents\SSLKeys\ssl.log`

![edit-system-variable.png](./docs/assets/edit-system-variable.png)

4. Press OK and restart your computer.
5. After restart make sure that the document has been generated and has text.
