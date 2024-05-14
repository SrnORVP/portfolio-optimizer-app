<script>
	import { invoke } from '@tauri-apps/api/tauri';
	// import { multiLineSVG } from './svg_xml';

    let svg_content = ""

	async function serve_svg() {
		// to invoke server
		let temp = await invoke('server_run_health_metric', { user_path: path, user_mode: ops });
		// let temp = multiLineSVG;
		svg_content = temp;
	}
</script>

<button on:click={serve_svg}> Submit </button>

<div>
	{@html svg_content}
</div>
