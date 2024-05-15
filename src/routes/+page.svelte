<script>
	import { Accordion, Space, Tabs, Title } from '@svelteuidev/core';

	import ConfigGroup from './ConfigGroup.svelte';
	import NewDate from '$lib/NewDate.svelte';
	import ChartGroup from './ChartGroup.svelte';

	// let overrideStyle = {
	// 	fontSize: '1.5rem',
	// 	fontWeight: 200,
	// 	margin: '1rem 0 1rem 0'
	// };

	let runValue;
	let precValue;
	let stockValue;
	let startDate;
	let endDate;

	let overrideStyle = {
		fontSize: 26,
		lineHeight: 1.35,
		margin: '0.75rem 0 0.75rem 0',
		padding: '0 2rem 0 0'
	};

	let defAccord = ['config', 'optimize'];
</script>

<Tabs orientation="vertical" tabPadding="xs" variant="default">
	<Tabs.Tab label="User Inputs" override={overrideStyle}>
		<Accordion multiple defaultValue={defAccord} chevronPosition="left">
			<Accordion.Item value="config">
				<div slot="control">
					<Title order={3}>Choose operation</Title>
				</div>
				<ConfigGroup bind:stockValue bind:runValue bind:precValue bind:startDate bind:endDate />
			</Accordion.Item>

			<Accordion.Item value="optimize">
				<div slot="control">
					<Title order={3}>Optimization</Title>
				</div>

				<div>
					{stockValue}
					<br />
					{runValue}
					<br />
					{precValue}
					<br />
					{startDate}
					<br />
					{endDate}
					<br />
				</div>
				<ChartGroup />
			</Accordion.Item>

			<Accordion.Item value="submit">
				<div slot="control">
					<Title order={3}>Submit for optimization</Title>
				</div>
				Submit
				<!-- <SubmitComp /> -->
			</Accordion.Item>
		</Accordion>
	</Tabs.Tab>

	<Tabs.Tab label="Visualization" override={overrideStyle}>
		<div slot="control">Choose the chart to display</div>
		<!-- <SelectComp /> -->
	</Tabs.Tab>
</Tabs>
