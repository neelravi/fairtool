function createScript(src) {
  return new Promise((resolve, reject) => {
    // Resolve the src against the document base so comparisons and src
    // attributes are consistent (handles relative vs absolute URLs).
    let resolved;
    try {
      resolved = new URL(src, document.baseURI).href;
    } catch (e) {
      resolved = src;
    }

    // Avoid adding duplicate script tags: match by resolved href or suffix
    const existing = Array.from(document.getElementsByTagName('script')).find(s => {
      try { return s.src === resolved || s.src === src || s.src.endsWith(src); } catch (e) { return false; }
    });
    if (existing) {
      // If it's already loaded, resolve immediately; otherwise wait for load/error
      if (existing.readyState && existing.readyState !== 'loading') return resolve();
      existing.addEventListener('load', () => resolve());
      existing.addEventListener('error', () => reject(new Error('Failed to load ' + src)));
      return;
    }
    const s = document.createElement('script');
    s.src = resolved;
    s.async = true;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error('Failed to load ' + src));
    document.head.appendChild(s);
  });
}

function waitFor3Dmol(timeout = 15000, interval = 200) {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    function check() {
      if (typeof window !== 'undefined' && typeof window.$3Dmol !== 'undefined') {
        return resolve();
      }
      if (Date.now() - start > timeout) {
        return reject(new Error('3Dmol did not load within timeout'));
      }
      setTimeout(check, interval);
    }

    // If 3Dmol isn't present, attempt to load a local copy first, then CDN
    if (typeof window === 'undefined' || typeof window.$3Dmol === 'undefined') {
      // Try local first (most reliable for previews), then CDN fallbacks
      createScript('/js/3Dmol-min.js')
        .catch(() => createScript('https://3dmol.org/build/3Dmol-min.js'))
        .catch(() => createScript('https://unpkg.com/3dmol/build/3Dmol-min.js'))
        .finally(() => {
          // Start polling for $3Dmol
          check();
        });
    } else {
      check();
    }
  });
}

function loadStructures() {
  document.querySelectorAll(".structure-viewer").forEach(container => {
    const jsonPath = container.dataset.json;
    if (!jsonPath || container.dataset.loaded === "true") return;

    container.dataset.loaded = "true"; // prevent double init

    fetch(jsonPath)
      .then(r => {
        if (!r.ok) {
          // Try resolving relative to the current page location and retry once
          const alt = new URL(jsonPath, document.baseURI).href;
          return fetch(alt).then(r2 => {
            if (!r2.ok) throw new Error('Failed to fetch ' + jsonPath + ' (tried ' + alt + '): ' + r2.status);
            return r2.json();
          });
        }
        return r.json();
      })
      .then(data => {
        // Wait until the 3Dmol script is available to avoid race conditions
        return waitFor3Dmol().then(() => data).catch(err => {
          // If 3Dmol didn't load, inject a visible error into the container so the
          // user sees why the viewer didn't render instead of a blank space.
          container.innerHTML = '';
          const msg = document.createElement('div');
          msg.style.color = '#b00';
          msg.style.padding = '1em';
          msg.textContent = '3Dmol failed to load: ' + String(err);
          const btn = document.createElement('button');
          btn.textContent = 'Retry 3D viewer';
          btn.style.marginLeft = '0.5em';
          btn.addEventListener('click', () => {
            // Reset loaded flag and re-run the loader
            delete container.dataset.loaded;
            loadStructures();
          });
          const wrapper = document.createElement('div');
          wrapper.appendChild(msg);
          wrapper.appendChild(btn);
          container.appendChild(wrapper);
          throw err;
        });
      })
      .then(data => {
        try {
          const lattice = data.lattice.matrix;
          const sites = data.sites;

          let xyz = `${sites.length}\nstructure\n`;
          sites.forEach(site => {
            const el = site.element || "X";
            const [x, y, z] = site.xyz;
            xyz += `${el} ${x} ${y} ${z}\n`;
          });

          const viewerContainer = container;
          // Clear previous children (if any) to avoid duplicate canvases
          while (viewerContainer.firstChild) viewerContainer.removeChild(viewerContainer.firstChild);

          viewerContainer.style.position = "relative";  // ensures 3Dmol fills it
          viewerContainer.style.width = "100%";
          viewerContainer.style.height = container.style.height || "500px";

          // Create the viewer and render
          const viewer = window.$3Dmol.createViewer(viewerContainer);
          viewer.addModel(xyz, "xyz");
          viewer.setStyle({}, { stick: { radius: 0.2 }, sphere: { scale: 0.3 } });

          // === Draw Unit Cell ===
          const [a, b, c] = lattice;
          const v = (v) => ({ x: v[0], y: v[1], z: v[2] });

          const verts = [
            v([0,0,0]), v(a), v(b), v(c),
            v([a[0]+b[0], a[1]+b[1], a[2]+b[2]]),
            v([a[0]+c[0], a[1]+c[1], a[2]+c[2]]),
            v([b[0]+c[0], b[1]+c[1], b[2]+c[2]]),
            v([a[0]+b[0]+c[0], a[1]+b[1]+c[1], a[2]+b[2]+c[2]]),
          ];

          const edges = [[0,1],[0,2],[0,3],[1,4],[1,5],[2,4],[2,6],[3,5],[3,6],[4,7],[5,7],[6,7]];
          edges.forEach(([i,j]) => viewer.addLine({start:verts[i], end:verts[j], color:"black"}));

          viewer.zoomTo();
          viewer.render();
        } catch (err) {
          console.error('Error rendering structure viewer for', jsonPath, err);
        }
      })
      .catch(err => {
        console.error('structure.js:', err);
      });
  });
}

// --- Run after full page load (fallback if instant nav disabled) ---
document.addEventListener("DOMContentLoaded", loadStructures);

// --- Run after every Material page navigation ---
if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    loadStructures();
  });
}
