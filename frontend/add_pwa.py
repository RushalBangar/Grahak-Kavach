import os
import glob

html_files = glob.glob('*.html')

pwa_head = """  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#10b981">
"""

pwa_script = """  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => {
          console.log('SW registration failed: ', err);
        });
      });
    }
  </script>
"""

for file in html_files:
    if file == 'index.html':
        continue # Already done
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<link rel="manifest"' not in content:
        # inject head
        content = content.replace('  <link rel="icon"', pwa_head + '  <link rel="icon"')
        # inject script
        content = content.replace('</body>', pwa_script + '</body>')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
