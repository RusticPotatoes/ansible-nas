---
title: "Cloudflare Tunnel"
---

Homepage: [https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

Remote access without an open port: `cloudflared` keeps an outbound connection to Cloudflare,
and the routes and access policies you set in the Cloudflare Zero Trust dashboard decide what
reaches which service. It replaces exposing a port (for example WireGuard's) to the internet.

## Settings

```yaml
cloudflared_enabled: true
```

and, in your **vault** (never in a tracked file: this repository may be public):

```yaml
vault_cloudflared_tunnel_token: "<the tunnel token from the Zero Trust dashboard>"
```

With the token empty the role deploys nothing and says why.

Routes and access policies live in the Zero Trust dashboard, not here. Publish only what you
mean to, behind an access policy.
