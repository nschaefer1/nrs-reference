
# Server Hosting Reference

## Core Domain

Domains can be purchased through NAMECHEAP. The domain is just the rights to the address, not the actual website.

## Mental Model

Client → Cloudflare DNS → Cloudflare Tunnel → Local Service

- DNS resolves domain
- Cloudflare routes to tunnel
- Tunnel forwards to local port

## Cloudflare

Cloudflare manages DNS and routing for the domain, not ownership. Cloudflared runs a persistent outboudn connection from your machine to Cloudflare, so no ports need to be opened. The steps to utilize Cloudflare are the following:

1. Register a domain through **namecheap**
2. Register the two `nameservers` given by cloudflare into **namecheap**. Ensure *DNS* is set to *Custom*.
3. Download [Cloudflared](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/) and place into a file in your directory, run it with CMD.
4. Run `cloudfalred tunnel login` into the CMD  
    You are now authorizing the machine to control Cloudflared account - which should be saved.   
    This can be reran and does not need to be saved - do not share it.
5. Run `cloudflared tunnel create some_name`
    This just creates the unnel with credentials -- you can delete this tunnel in the future  
    For example `core-tunnel`
6. Route a subdomain into the tunnel `cloudflared tunnel route dns <tunnel_name> <subdomain>.<domain>`  
    This writes a DNS, but you can create *any* amount  
    Tunnel = Pipe  
    Domain = namespace  
    Subdomain = routing label  
7. Once the subdomain and tunnel are running, create a `yml` file that documents your tunnel, associated credentails, and ingress
    This should be *next* to the credentials file  
    Hostname, service, and service  
```yml
tunnel: tunnel_name
credentials-file: /path/to/credentials.json

ingress:

    - hostname: app.example.com
      service: http://localhost:8000
    
    - service: http_status:404
```
8. Start the tunnel `cloudflared tunnel run core-tunnel`  
    Once this is running, hostnames defined in `ingress` are exposed to the **public** - anyone can access this domain
9. Once the tunnel is started, on cloudflare, implement protections to prevent random connections. Some things can be exposed in the tunnel if needbe.

## Tunnel Model

- Tunnel is controlled by the PC
- Authenticated by the JSON file
- Ingress maps the hostname to service
- One tunnel can serve multiple host names
- Control prots nad routing internally

## Domain Ownership

- Namecheap = registrar
- Cloudflare = DNS + proxy + security + auth
  
You do not have to recreate a tunnel if the domain dies, only change the *DNS* route, the tunnel is independent of the domain name.

## API Keys

- Require an API Key for POST/PUT/DELETE
- Allow GET publicly (if safe data)

```python
if method != "GET":
    validate_api_key()
```

## DB Locking

For writes use `asyncio.Lock` or `threading.lock`  
Usually safe to allow concurrency for reads

## Startup the Tunnel

**Option 1: run from the target directory (simplest)**

```powershell
cd C:\projects\myapp
.\start.ps1
```

```powershell
Start-Process `
    -FilePath "C:\Users\Owner\cloudflared\cloudflared.exe" `
    -ArgumentList "tunnel run tunnel_name" `
    -WorkingDirectory "." `
    -RedirectStandardOutput ".\cloudflared.log" `
    -RedirectStandardError ".\cloudflared_error.log" `
    -PassThru `
    -NoNewWindow
```

**Option 2: RUn from anywhere (script controls location)**

```powershell
C:\projects\myapp\start.ps1
```

```powershell
Set-Location $PSScriptRoot

$tunnel = Start-Process `
    -FilePath "C:\Users\Owner\cloudflared\cloudflared.exe" `
    -ArgumentList "tunnel run tunnel_name" `
    -WorkingDirectory "." `
    -RedirectStandardOutput ".\cloudflared.log" `
    -RedirectStandardError ".\cloudflared_error.log" `
    -PassThru `
    -NoNewWindow
```