import { bindings, defineConfig } from "cf/config";
import * as entrypoint from "./src/index.ts" with { type: "cf-worker" };

export default defineConfig(({ mode }) => ({
	worker: {
		name: "koin-data-logging-workbench",
		compatibilityDate: "2026-11-12",
		compatibilityFlags: ["nodejs_compat"],
		entrypoint,
		assets: { htmlHandling: "none", notFoundHandling: "none", runWorkerFirst: true },
		observability: {
			enabled: true,
			redactQueryString: true,
			logs: { enabled: true, headSamplingRate: 0.1 },
			traces: { enabled: true, headSamplingRate: 0.1 },
		},
		env: {
			ASSETS: bindings.assets(),
			DASHBOARD_PASSWORD: bindings.secret(),
			...(mode === "github" ? { GITHUB_TOKEN: bindings.secret() } : {}),
			GITHUB_REPOSITORY: bindings.text("BCSDLab/KOIN-DATA-LOGGING"),
		},
	},
}));
