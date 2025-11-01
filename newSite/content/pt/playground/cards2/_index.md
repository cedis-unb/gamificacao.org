---
title: "Cards do Blowfish"
build:
  list: never
  render: always
  publishResources: true
sitemap:
  disable: true
robots: "noindex,nofollow"
menu: false
draft: false
---

## Codeberg
Exibe repositórios hospedados no Codeberg. Parâmetro obrigatório: `repo` no formato `usuario/repositorio`. :contentReference[oaicite:0]{index=0}

{{< codeberg repo="forgejo/forgejo" >}}

---

## Forgejo
Exibe repositórios Forgejo. Parâmetros: `server` (URL da instância) e `repo`. :contentReference[oaicite:1]{index=1}

{{< forgejo server="https://v11.next.forgejo.org" repo="a/mastodon" >}}

---

## Gitea
Exibe repositórios Gitea. Parâmetros: `server` (URL da instância) e `repo`. :contentReference[oaicite:2]{index=2}

{{< gitea server="https://git.fsfe.org" repo="FSFE/fsfe-website" >}}

---

## GitHub
Exibe repositórios GitHub. Parâmetro obrigatório: `repo` no formato `usuario/repositorio`. :contentReference[oaicite:3]{index=3}

{{< github repo="nunocoracao/blowfish" >}}

---

## GitLab
Exibe projetos GitLab. Parâmetros: `projectID` (numérico) e `baseURL` opcional. :contentReference[oaicite:4]{index=4}

{{< gitlab projectID="278964" >}}

---

## listas em cartões (extra)
Para listas de artigos como cartões, use `list` com `cardView=true` ou ative `list.cardView` na configuração. :contentReference[oaicite:6]{index=6}

{{< list title="Amostras (cards)" cardView=true limit=6 where="Type" value="sample" >}}
