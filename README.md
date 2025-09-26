# Gamificação ORG

Site estático construído com Hugo e o tema Blowfish. Conteúdo bilíngue (Português e Inglês) com seções Home, Sobre, Reuniões e Pessoas.

## Requisitos
- Hugo (recomendado: versão estável recente; mínimo 0.87)
- Git (para submódulo do tema)

## Como rodar
- Desenvolvimento: `npm start` (Hugo server com rascunhos)
- Produção (pré‑visualização): `npm run serve:prod`
- Build: `npm run build` (gera em `docs/` na raiz do repositório)
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
- Português sob subdiretório `/pt/`: `defaultContentLanguageInSubdir = true`
- Menus por idioma: `newSite/config/_default/menus.pt.toml` e `menus.en.toml`
- Seletor de idioma em `layouts/partials/translations.html` (sempre visível; tenta linkar a tradução; fallback para home do idioma)

## Deploy (GitHub Pages)
O projeto está configurado para publicar o build no diretório `docs/` (raiz do repositório) via `publishDir = "../docs"`.

Há duas formas recomendadas de deploy:

1) Pages a partir da pasta `/docs` (mais simples)
- Em Settings → Pages: “Build and deployment: Deploy from a branch”
- Branch: `main` (ou a padrão) • Folder: `/docs`
- Após `npm run build`, o site é servido a partir de `https://<user>.github.io/<repo>/` (ou do domínio configurado).

2) GitHub Actions (workflow incluso)
- Arquivo: `.github/workflows/hugo.yml`
- O passo de build roda `hugo -s newSite --minify --gc`, que gera o site em `docs/` (por causa do `publishDir`).
- Ajuste o artifact de publicação para usar `path: docs` (o workflow padrão aponta para `newSite/public`).

Outras opções de deploy:
- Netlify: base `newSite/`, comando `hugo -s newSite --gc --minify`, diretório de publicação `docs` (ou ajuste conforme sua preferência)
- Qualquer hosting estático: publique o conteúdo de `docs/`

## Manutenção do tema
- O tema Blowfish é um submódulo (`themes/blowfish`). Para atualizar:
  ```bash
  git submodule update --remote --init --recursive
  # Opcional: fixe em um commit/tag para reprodutibilidade
  ```
- Recomenda‑se fixar o submódulo em uma tag/commit estável ao invés de seguir `main`.

## Notas de configuração
- `baseURL = "https://gamificacao.org/"`
- `publishDir = "../docs"` (gera em `docs/` na raiz)
- `defaultContentLanguage = "pt"` e `defaultContentLanguageInSubdir = true` (Português em `/pt/`)

## Autor

Sergio Antônio Andrade de Freitas

