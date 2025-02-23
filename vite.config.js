import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    // Output files directly into your static folder
    outDir: resolve(__dirname, 'static'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: false,
    rollupOptions: {
      input: {
        // List each JS file you want bundled.
        // Adjust paths as needed; here we're assuming your source files are in a folder (e.g. 'src/js').
        // If your current files live in /static/js and are already served as-is, consider moving the source code to a dedicated folder.
        chatbot: resolve(__dirname, 'app/static/js/chatbot.js'),
        dashboardPopup: resolve(__dirname, 'app/static/js/dashboard/popup.js'),
        flashcards: resolve(__dirname, 'app/static/js/flashcards.js'),
        notes: resolve(__dirname, 'app/static/js/notes.js'),
        progress: resolve(__dirname, 'app/static/js/progress.js'),
        quiz: resolve(__dirname, 'app/static/js/quiz.js'),
        settings: resolve(__dirname, 'app/static/js/settings.js'),
        transcript: resolve(__dirname, 'app/static/js/transcript.js'),
        // You can include util.js if it’s used as a dependency or if it should be bundled on its own.
        util: resolve(__dirname, 'app/static/js/util.js'),
      },
      output: {
        entryFileNames: 'js/[name]-[hash].js',
        chunkFileNames: 'js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const ext = assetInfo.name.split('.').pop();
          if (ext === 'css') {
            return 'css/[name]-[hash][extname]';
          }
          return '[name]-[hash][extname]';
        },
      },
    },
  },
});
