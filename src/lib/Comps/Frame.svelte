<script>
	import { useElementSize } from '@svelteuidev/composables';

	export let value;
	export let width;
	export let height;

	const [elementSize, ref] = useElementSize();

	$: ({ width, height } = $elementSize);
</script>

<div class="container">
	<iframe
		use:ref
		class="plotFrame"
		id="plotFrame"
		title="Plotly Plots"
		srcdoc={value}
		width="100%"
		height="100%"
	/>
</div>

<style>
	.container {
		position: relative;
		overflow: hidden;
		width: 100%;
		height: 100%;
		/* padding-top: 10%; */
		padding-top: 56.25%;
		/* 16:9 Aspect Ratio (divide 9 by 16 = 0.5625) */
	}

	.plotFrame {
		transition: all 1s ease-out;
		position: absolute;
		top: 0;
		left: 0;
		bottom: 0;
		right: 0;
		border: 0;
		/* width: 100%; */
		/* height: 100%; */
	}
</style>
