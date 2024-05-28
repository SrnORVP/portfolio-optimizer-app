<script>
	import { Accordion, Tabs, Title } from '@svelteuidev/core';
	import { onMount } from 'svelte';

	import ConfigGroup from '$lib/Groups/Config.svelte';
	import ChartsGroup from '$lib/Groups/Charts.svelte';
	import ReviewGroup from '$lib/Groups/Review.svelte';

	import { getFetch, postFetch } from '$lib/fetchHandler';

	// let overrideStyle = {
	// 	fontSize: '1.5rem',
	// 	fontWeight: 200,
	// 	margin: '1rem 0 1rem 0'
	// };

	let stockValue;
	let runValue;
	let precValue;
	let startDate;
	let endDate;
	let chartNames;
	let chartSelected;
	let chartContent;
	let riskTarget;
	let messages;

	async function getDefaultStates() {
		await getFetch().then((appState) => resolveDefaultStates(appState));
	}
	onMount(getDefaultStates);

	async function resolveDefaultStates(appState) {
		console.log('after', appState);
		stockValue = appState.codes;
		runValue = appState.runs;
		precValue = appState.precision;
		startDate = appState.start;
		endDate = appState.end;
		chartNames = appState.charts;
		chartSelected = appState.chart;
		chartContent = appState.html;
		riskTarget = appState.target;
		messages = appState.messages;
	}

	let overrideStyle = {
		fontSize: 26,
		lineHeight: 1.35,
		margin: '0.75rem 0 0.75rem 0',
		padding: '0 1rem 0 0'
	};

	let defAccord = ['config', 'optimize'];
</script>

<Tabs orientation="vertical" tabPadding="xs" variant="default">
	<Tabs.Tab label="User Inputs" override={overrideStyle}>
		<Accordion multiple defaultValue={defAccord} chevronPosition="left">
			<Accordion.Item value="config">
				<div slot="control">
					<Title order={3}>Choose Parameters</Title>
				</div>
				<ConfigGroup bind:stockValue bind:runValue bind:precValue bind:startDate bind:endDate />
			</Accordion.Item>

			<Accordion.Item value="optimize">
				<div slot="control">
					<Title order={3}>Selected Parameters</Title>
				</div>
				<ReviewGroup
					bind:stockValue
					bind:runValue
					bind:precValue
					bind:startDate
					bind:endDate
					bind:chartNames
					bind:messages
				/>
			</Accordion.Item>

			<Accordion.Item value="submit">
				<div slot="control">
					<Title order={3}>Optimization</Title>
				</div>
				Submit
				<!-- <SubmitComp /> -->
			</Accordion.Item>
		</Accordion>
	</Tabs.Tab>

	<Tabs.Tab label="Visualization" override={overrideStyle} on:click>
		<ChartsGroup bind:chartNames />
	</Tabs.Tab>

	<Tabs.Tab label="Readme" override={overrideStyle} on:click>
		README
	</Tabs.Tab>

</Tabs>

<!-- bind:noticeMsg
bind:errorMsg -->
