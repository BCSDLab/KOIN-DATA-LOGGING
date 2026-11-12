import { cloudflare } from "@cloudflare/vite-plugin";
import { defineConfig } from "vite";

export default defineConfig({
	server: { port: 15173, strictPort: true },
	plugins: [cloudflare()],
});
