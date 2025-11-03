#!/usr/bin/env node
/**
 * Fix index.html redirects for multi-domain support
 * Replace absolute URL redirects with relative ones
 */

const fs = require('fs');
const path = require('path');

const docsPath = path.join(__dirname, '..', 'docs');

// Root redirect (homepage redirect)
const rootRedirectHTML = `<!DOCTYPE html>
<html lang="pt">
  <head>
    <title>Redirecionando...</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
      // Redirect to default language with relative URL for multi-domain support
      (function() {
        const lang = navigator.language || navigator.userLanguage;
        const targetPath = lang.startsWith('en') ? '/en/' : '/pt/';
        window.location.href = targetPath;
      })();
    </script>
  </head>
  <body>
    <p>Redirecionando para o idioma preferido...</p>
  </body>
</html>`;

// Function to convert absolute URL to relative in redirect
function fixRedirectHTML(content, filePath) {
  // Match: content="0; url=https://gamificacao.org/..."
  const match = content.match(/content="0; url=https:\/\/gamificacao\.org(\/[^"]*?)"/);
  if (match) {
    const absolutePath = match[1];
    // Convert to relative path (use ../ to go back to root, then the path)
    const fileDir = path.dirname(filePath);
    const relFromRoot = path.relative(docsPath, fileDir);
    
    // Count how many levels deep we are
    const depth = relFromRoot.split(path.sep).filter(p => p && p !== '.').length;
    const goUpPath = depth > 0 ? '../'.repeat(depth) : './';
    
    // The target path, removing leading /
    const targetPathClean = absolutePath.startsWith('/') ? absolutePath.slice(1) : absolutePath;
    const relativePath = goUpPath + targetPathClean;
    
    return content.replace(
      /content="0; url=https:\/\/gamificacao\.org(\/[^"]*)"/,
      `content="0; url=${relativePath}"`
    );
  }
  return content;
}

// Recursive function to find all index.html files in page/*/1/ directories
function findPaginationFiles(dir, results = []) {
  try {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat.isDirectory()) {
        if (file === 'page') {
          // Look for page/*/1/index.html
          const pageDir = filePath;
          const pageNumbers = fs.readdirSync(pageDir);
          for (const pageNum of pageNumbers) {
            const pagePath = path.join(pageDir, pageNum, 'index.html');
            if (fs.existsSync(pagePath)) {
              results.push(pagePath);
            }
          }
        } else {
          // Recurse into subdirectories (but not page/ as we handle it above)
          findPaginationFiles(filePath, results);
        }
      }
    }
  } catch (e) {
    // Ignore read errors
  }
  return results;
}

try {
  // Fix root index.html
  const rootPath = path.join(docsPath, 'index.html');
  fs.writeFileSync(rootPath, rootRedirectHTML, 'utf-8');
  console.log('✓ Fixed root index.html redirect');

  // Find all pagination redirects
  const paginationFiles = findPaginationFiles(docsPath);
  
  let fixedCount = 0;
  for (const file of paginationFiles) {
    const content = fs.readFileSync(file, 'utf-8');
    const fixed = fixRedirectHTML(content, file);
    if (fixed !== content) {
      fs.writeFileSync(file, fixed, 'utf-8');
      fixedCount++;
    }
  }

  if (fixedCount > 0) {
    console.log(`✓ Fixed ${fixedCount} pagination redirects`);
  }
  console.log('✓ All redirects converted to relative URLs for multi-domain support');
} catch (error) {
  console.error('✗ Error fixing redirects:', error);
  process.exit(1);
}
