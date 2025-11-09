# UI Before / After (Brand Apply)

    **Generated:** 2025-11-06T07:24:55Z

    ## What changed
    - Updated **title/meta** and added **favicons** + **PWA manifest** in `frontend/index.html`.
    - Imported **brand tokens** (`frontend/src/brand/tokens.css`) in `frontend/src/main.tsx` **before** `styles.css`.
    - No runtime libraries added; pure CSS variables.

    ## Diff — index.html
    ```diff
    --- a/frontend/index.html
+++ b/frontend/index.html
@@ -1,9 +1,16 @@
 <!doctype html>
 <html lang="en">
   <head>
+    <meta name="theme-color" content="#22c55e" />
+    <meta name="description" content="Inventory Guardian — Control Tower v2: real-time inventory alerts, ROI proof, and pilot-ready dashboard." />
+    <link rel="icon" type="image/svg+xml" href="/favicon/favicon.svg" />
+    <link rel="icon" sizes="16x16" href="/favicon/favicon-16.png" />
+    <link rel="icon" sizes="32x32" href="/favicon/favicon-32.png" />
+    <link rel="apple-touch-icon" href="/favicon/favicon-180.png" />
+    <link rel="manifest" href="/favicon/site.webmanifest" />
     <meta charset="UTF-8" />
     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
-    <title>Inventory Guardian</title>
+    <title>Inventory Guardian — Control Tower v2</title>
   </head>
   <body>
     <div id="root"></div>

    ```

    ## Diff — main.tsx
    ```diff
    --- a/frontend/src/main.tsx
+++ b/frontend/src/main.tsx
@@ -2,6 +2,7 @@
 import ReactDOM from 'react-dom/client';
 import { BrowserRouter } from 'react-router-dom';
 import App from './App';
+import './brand/tokens.css';
 import './styles.css';

 ReactDOM.createRoot(document.getElementById('root')!).render(

    ```

    ## Build check
    Run:
    ```bash
    npm run build && npm run preview
    # Open http://localhost:5174 — Favicons rendered, green accent visible, dark theme intact.
    ```
