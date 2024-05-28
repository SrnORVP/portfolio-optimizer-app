<script>
	import { Stack, Loader, Center } from '@svelteuidev/core';

	import { getFetch, postFetch } from '$lib/fetchHandler';
	import SelectComp from '$lib/Comps/Select2.svelte';
	import FrameComp from '$lib/Comps/Frame.svelte';

	export let chartNames;
	let chartSelected;
	let chartContent;
	let selData;
	let frameHeight;
	let frameWidth;
	let isLoading = true;

	$: chartNames, updateSelections();
	$: chartSelected, postPlotState();

	async function updateSelections() {
		if (!!chartNames) {
			selData = chartNames.map((e) => ({ label: e, value: e }));
			chartSelected = '';
			isLoading = true;
		}
	}

	async function postPlotState() {
		isLoading = true;
		chartContent = '<html/>';
		if (!!chartSelected) {
			let data = {
				state: 'p',
				chart: chartSelected,
				fheight: frameHeight,
				fwidth: frameWidth
			};
			let resp = await postFetch(data);
			chartContent = resp.html;
			if (!!chartContent) {
				isLoading = false;
			}
		}
	}
</script>

<Stack spacing="xl">
	<SelectComp
		bind:value={chartSelected}
		bind:selections={selData}
		display="Choose Chart to display"
		explain="Different chart content different data"
	/>

	{#if isLoading}
		<Center>
			<Loader variant="dots" />
		</Center>
	{/if}
	<FrameComp bind:value={chartContent} bind:height={frameHeight} bind:width={frameWidth} />
</Stack>
