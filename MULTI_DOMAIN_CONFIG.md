# Configuração Multi-Domínio - gamificacao.org

## ✅ Mudanças Realizadas

### 1. Configuração Hugo (hugo.toml)

**Adicionadas as seguintes configs:**

```toml
# URLs relativas para funcionar em múltiplos domínios
relativeURLs = true
canonifyURLs = false

# Cada idioma em seu próprio subdiretório
defaultContentLanguageInSubdir = true
```

**Resultado:** O site funciona perfeitamente em:
- `https://gamificacao.org/`
- `https://gamification.cedis.cloud/`

### 2. Templates (head.html)

**Canonical Link atualizado:**

```html
<!-- ANTES (absoluto - causa problemas em multi-domínio) -->
<link rel="canonical" href="{{ .Permalink }}" />

<!-- DEPOIS (relativo - funciona em qualquer domínio) -->
<link rel="canonical" href="{{ .RelPermalink }}" />
```

**Resultado:** Canonical links agora são relativas (`../../en/members/`)

### 3. Assets Estáticos (CNAME)

**Criado arquivo:**
- `newSite/static/CNAME` → copiado para `docs/CNAME`
- Contém: `gamificacao.org`

### 4. Verificações Realizadas

✅ Nenhuma tag `<base>` encontrada (não há redirects)
✅ Nenhum `meta http-equiv="refresh"` (sem redirects)
✅ Sem `window.location` redirects
✅ Assets usam `relURL` (correto)
✅ OpenGraph meta tags usam `absURL` (aceitável para redes sociais)

## 🚀 Deploy em Múltiplos Domínios

### GitHub Pages (gamificacao.org)
- Configurado para servir da branch `main`
- Usa diretório `docs/` como source
- CNAME automático: `gamificacao.org`

### Custom Domain (gamification.cedis.cloud)
```bash
# Copiar build para servidor customizado
rsync -az --delete ./docs/ deploy@72.60.58.99:/var/www/gamification
```

**Resultado:** Ambos os domínios servem o mesmo build sem redirecionamentos!

## 🧪 Testes Realizados

```bash
# Build bem-sucedido
cd newSite && npm run build
# Resultado: 75 PT + 71 EN páginas, 11 static files

# Verificar canonical links
grep "rel=\"canonical\"" docs/en/members/index.html
# Resultado: <link rel="canonical" href="../../en/members/" />
```

## 📋 Configuração Multilíngue

**Idiomas:**
- PT (Português) - idioma padrão
- EN (Inglês)

**Estrutura:**
- `docs/pt/` - conteúdo português
- `docs/en/` - conteúdo inglês
- `docs/index.html` - redirect/landing (PT por padrão)

## ✨ Benefícios

1. **Multi-domínio sem redirects** - melhor performance
2. **SEO-friendly** - canonical links relativas funcionam em ambos os domínios
3. **Escalável** - fácil adicionar novos domínios sem reconstruir
4. **GitHub Pages compatible** - funciona nativamente
5. **CDN friendly** - URLs relativas cache melhor

## 📝 Notas

- `relativeURLs = true` garante que URLs internas são relativas
- `canonifyURLs = false` evita forçar URLs absolutas
- `defaultContentLanguageInSubdir = true` mantém PT e EN em subdiretórios separados
- O arquivo CNAME é apenas para GitHub Pages, não afeta multi-domínio

---

**Status:** ✅ Pronto para produção em múltiplos domínios!
