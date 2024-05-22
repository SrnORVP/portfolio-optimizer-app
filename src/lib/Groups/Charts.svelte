<script>
	import { Stack, fns, Center, Space, Group, Title, Flex, Divider } from '@svelteuidev/core';

	import { getFetch, postFetch } from '$lib/fetchHandler';
	import SelectComp from '$lib/Comps/Select2.svelte';
	import FrameComp from '$lib/Comps/Frame.svelte';

	export let chartNames;
	let chartSelected;
	let chartContent;
	let selData;
	let frameHeight;
	let frameWidth;

	$: chartNames, updateSelections();
	$: chartSelected, postPlotState();

	async function getChartState() {
		const resp = await getFetch();
		chartNames = resp.charts;
		chartSelected = resp.chart;
		chartContent = resp.html;
	}

	async function updateSelections() {
		if (!!chartNames) {
			selData = chartNames.map((e) => ({ label: e, value: e }));
		}
	}

	async function postPlotState() {
		if (!!chartSelected) {
			let data = {
				state: "p",
				chart: chartSelected,
				fheight: frameHeight,
				fwidth: frameWidth
				// html: chartContent
			};
			let resp = await postFetch(data);
			chartContent = resp.html;
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
	<FrameComp bind:value={chartContent} bind:height={frameHeight} bind:width={frameWidth} />
</Stack>
