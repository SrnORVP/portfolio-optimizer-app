<script>
	import { Stack, fns, Center, Space, Grid, Title, Flex, Divider } from '@svelteuidev/core';

	// import InputComp from '$lib/storeComp/InputComp.svelte';
	import InputComp from '$lib/InputComp2.svelte';
	import NumInpComp from '$lib/NumInpComp.svelte';
	import DateComp2 from '$lib/DateComp.svelte';
	import DateComp from '$lib/NewDate.svelte';
	import SelectManual from '$lib/SelectManual.svelte';
	// import SelectComp from '$lib/SelectComp.svelte';

	export let runValue = 10000;
	export let precValue;
	export let stockValue = 'AAPL, MSFT, AWS';
	export let startDate;
	export let endDate;

	// import SubmitComp from '$lib/storeComp/SubmitComp.svelte';
	// import SelectComp from '$lib/SelectComp.svelte';

	// import InputCompDefault from '$lib/storeComp/InputCompDefault.svelte';
	// import RadioComp from '$lib/storeComp/RadioComp.svelte';
	let overrideStyle = { minWidth: 300, maxWidth: 500 };
</script>

<Stack spacing="xl" justify="flex-start">
	<Grid gutter="xs" grow justify="center" align="flex-start">
		<!-- <Grid spacing="xl" grow={true}> -->
		<Grid.Col span={6} override={{ minWidth: 600 }}>
			<InputComp
				bind:value={stockValue}
				display="Input stock code(s)"
				explain="Stock code(s) separated by commas"
			/>
		</Grid.Col>

		<Grid.Col span={3} override={overrideStyle}>
			<NumInpComp
				bind:value={runValue}
				display="Number of Monte Carlo Runs"
				valMin={1000}
				valMax={500000}
			/>
		</Grid.Col>

		<Grid.Col span={3} override={overrideStyle}>
			<SelectManual bind:value={precValue} numStock={2} />
		</Grid.Col>

		<Grid.Col span={3} override={overrideStyle}>
			<DateComp bind:value={startDate} display="Pick start date" />
		</Grid.Col>

		<Grid.Col span={3} override={overrideStyle}>
			<DateComp bind:value={endDate} display="Pick end date" explain="" />
			<!-- <DateComp2 bind:value={endDate} display="Pick end date" /> -->
		</Grid.Col>
	</Grid>

	<!-- <Divider></Divider> -->
</Stack>

<!-- <Space h="xl" /> -->
