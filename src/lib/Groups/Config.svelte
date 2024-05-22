<script>
	import { Button, Stack, fns, Center, Space, Grid, Title, Flex, Divider } from '@svelteuidev/core';


	import InputComp from '$lib/Comps/Input2.svelte';
	import NumInpComp from '$lib/Comps/NumInput.svelte';
	import DateComp from '$lib/Comps/NewDate.svelte';
	import SelectManual from '$lib/Comps/ManualSelect.svelte';

	export let stockValue;
	export let runValue;
	export let precValue;
	export let startDate;
	export let endDate;

	let runValMin = 1000;
	let runValMax = 500000;
	let overrideStyle = { minWidth: 300, maxWidth: 500 };
</script>

<Stack spacing="xl" justify="flex-start">
	<Grid spacing="xs" grow justify="center" align="flex-start">
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
				valMin={runValMin}
				valMax={runValMax}
			/>
		</Grid.Col>

		<Grid.Col span={3} override={overrideStyle}>
			<SelectManual bind:value={precValue} numStock={2} />
		</Grid.Col>

		<Grid.Col span={3} override={overrideStyle}>
			<DateComp bind:value={startDate} display="Pick start date" />
		</Grid.Col>

		<Grid.Col span={3} override={overrideStyle}>
			<DateComp bind:value={endDate} display="Pick end date" />
		</Grid.Col>
	</Grid>
</Stack>

<!-- <Space h="xl" /> -->
<!-- {stockValue}
<br />
{runValue}
<br />
{precValue}
<br />
{startDate}
<br />
{endDate}
<br /> -->
