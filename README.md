# Gamificação ORG

Site estático construído com Hugo e o tema Blowfish. Conteúdo bilíngue (Português e Inglês) com seções Home, Sobre, Reuniões e Pessoas.

## Requisitos
- Hugo (recomendado: versão estável recente; mínimo 0.87)
- Git (para submódulo do tema)

## Como rodar
- Desenvolvimento: `npm start` (Hugo server com rascunhos)
- Produção (pré‑visualização): `npm run serve:prod`
- Build: `npm run build` (gera em `newSite/public/`)
- Limpar e buildar: `npm run build:clean`
- Checagens de build: `npm run check` (falha em warnings)

## Estrutura
- `newSite/config/_default/`: configuração Hugo (site, idiomas, menus, params, markup, module)
- `newSite/content/`: conteúdo PT/EN (`about`, `meetings`/`reunioes`, `people`/`pessoas`)
- `newSite/layouts/`: customizações do tema (head, header, footer, shortcode `meetings`)
- `newSite/assets/`: logos do CEDIS e UnB, `logo.png`
- `newSite/static/img/`: avatares
- `themes/blowfish`: submódulo do tema

## Edição de conteúdo
- Home: `newSite/content/pt/_index.md` e `newSite/content/en/_index.md`
- Sobre: `newSite/content/pt/about/_index.md` e `newSite/content/en/about/_index.md`
- Reuniões:
  - PT: `newSite/content/pt/reunioes/_index.md`
  - EN: `newSite/content/en/meetings/_index.md`
  - Adicione itens no front matter (YAML/TOML) sob `meetings:` com `date`, `title`, `speaker`, `icon`, `badge`, `desc`.
  - A página usa o shortcode `{{< meetings >}}` que gera uma timeline com filtro por ano e ícones do tema.
- Pessoas:
  - PT: `newSite/content/pt/pessoas/_index.md`
  - EN: `newSite/content/en/people/_index.md`
  - Atualmente os cards são HTML simples; uma evolução é migrar perfis para `newSite/data/*.yaml` e renderizar via partial.

## Internacionalização
- Idioma padrão: PT (`defaultContentLanguage = "pt"`)
- Padrão na raiz (sem subdiretório): `defaultContentLanguageInSubdir = false`
- Menus por idioma: `newSite/config/_default/menus.pt.toml` e `menus.en.toml`
- Seletor de idioma em `layouts/partials/translations.html` (sempre visível; tenta linkar a tradução; fallback para home do idioma)

## Deploy (GitHub Pages)
Este repositório inclui um workflow de GitHub Actions em `.github/workflows/hugo.yml` que:
- Faz checkout com submódulos
- Instala Hugo (extended)
- Roda `hugo -s newSite --minify`
- Publica `newSite/public` no GitHub Pages

Passos para habilitar:
1. Em Settings → Pages, selecione “Build and deployment: GitHub Actions”
2. Garanta permissões de Pages para o workflow (já configurado no arquivo)
3. Faça push na branch padrão (ex.: `main`) e aguarde o deploy

Alternativas de deploy:
- Netlify: aponte para `newSite/` e use comando `hugo -s newSite --gc --minify`; diretório de publicação `newSite/public`
- Qualquer hosting estático: publique o conteúdo de `newSite/public`

## Manutenção do tema
- O tema Blowfish é um submódulo (`themes/blowfish`). Para atualizar:
  ```bash
  git submodule update --remote --init --recursive
  # Opcional: fixe em um commit/tag para reprodutibilidade
  ```
- Recomenda‑se fixar o submódulo em uma tag/commit estável ao invés de seguir `main`.

## Notas de configuração
- Removido `newSite/hugo.toml` (duplicado) para evitar conflitos com `config/_default/*`
- `defaultContentLanguageInSubdir` definido como `false` (Português na raiz do site); ajuste para `true` se quiser `/pt/`

