# WSL autostart (systemd user)

Ce guide configure l'auto-start WSL pour le backend (ngram), le frontend, le
MCP server FalkorDB et le tunnel ngrok, avec journald + logs locaux.

## 1) Activer systemd dans WSL

Edite `/etc/wsl.conf`:

```ini
[boot]
systemd=true
```

Puis relance WSL (depuis Windows):

```powershell
wsl --shutdown
```

## 2) Activer linger pour l'auto-start

```bash
loginctl enable-linger "$USER"
loginctl show-user "$USER" -p Linger
```

## 3) Binaries et chemins absolus

Les services utilisent des chemins absolus pour eviter les problemes de PATH:

- Python: `/usr/bin/python3`
- npm (nvm): `/home/mind-protocol/.nvm/versions/node/v24.10.0/bin/npm`
- ngrok: `/usr/local/bin/ngrok`

Si vos chemins sont differents, mettez a jour les fichiers dans
`~/ngram/tools/systemd/user/`.

## 4) Configurer le frontend

Le service frontend attend `FE_CMD` dans `~/ngram/.ngram/systemd.env`.
Renseignez la commande exacte du frontend (aucune supposition n'est faite):

```bash
sed -n '1,20p' ~/ngram/.ngram/systemd.env
```

## 5) Installer les units systemd

```bash
mkdir -p ~/.config/systemd/user
cp -v ~/ngram/tools/systemd/user/*.service ~/.config/systemd/user/
cp -v ~/ngram/tools/systemd/user/ngram-stack.target ~/.config/systemd/user/
systemctl --user daemon-reload
```

Activer l'ensemble:

```bash
systemctl --user enable --now ngram-stack.target
```

Ou activer service par service:

```bash
systemctl --user enable --now ngram-be.service
systemctl --user enable --now ngram-fe.service
systemctl --user enable --now falkor-mcp.service
systemctl --user enable --now ngrok-falkor.service
```

## 6) Config ngrok v3

Le fichier `~/ngram/tools/ngrok.yml` est en v3 et desactive
l'interface web pour eviter l'erreur EPERM:

```yaml
version: 3
agent:
  web_addr: false
```

Si vous voulez l'interface web, activez-la explicitement (et acceptez le risque
de bind EPERM dans WSL).

## 7) Logs et status

Journald:

```bash
journalctl --user -u ngram-be.service -f
journalctl --user -u ngram-fe.service -f
journalctl --user -u falkor-mcp.service -f
journalctl --user -u ngrok-falkor.service -f
```

Status:

```bash
systemctl --user status ngram-be.service
systemctl --user status ngram-fe.service
systemctl --user status falkor-mcp.service
systemctl --user status ngrok-falkor.service
```

Fichiers locaux (human-friendly):

- `~/ngram/.ngram/logs/ngram-be.log`
- `~/ngram/.ngram/logs/ngram-fe.log`
- `~/ngram/.ngram/logs/falkor-mcp.log`
- `~/ngram/.ngram/logs/ngrok-falkor.log`
- `~/ngram/.ngram/error.log`

## 8) Checks de sante

Local:

```bash
curl -i http://127.0.0.1:3005/api/mcp/health
```

Remote:

```bash
curl -i https://trusted-magpie-social.ngrok-free.app/api/mcp/health
```

## 9) Depannage

DNS WSL:

- Verifiez `/etc/resolv.conf` (nameserver corrompu ou supprime).
- Si WSL regenere un mauvais fichier, ajoutez:

```ini
[network]
generateResolvConf=false
```

dans `/etc/wsl.conf`, puis recreez `/etc/resolv.conf` avec un nameserver
adapte a votre environnement.

ngrok offline vs DNS:

- Si `journalctl` montre "failed to dial ngrok server", c'est souvent DNS.
- Si le tunnel est up mais l'URL repond en erreur, verifiez le port local.

Ports occupes:

```bash
lsof -i :3005
lsof -i :8000
```
