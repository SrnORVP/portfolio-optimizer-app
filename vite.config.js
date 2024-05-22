import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import * as path from "path";


export default defineConfig({
	plugins: [sveltekit()],
	build: {
		rollupOptions: {
			external: new RegExp('./.dump/*')
		},
	},
});
