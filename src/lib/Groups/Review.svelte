<script>
	import {
		Button,
		Stack,
		fns,
		Center,
		Space,
		Grid,
		Title,
		Flex,
		Divider,
		Group
	} from '@svelteuidev/core';

	import { getFetch, postFetch } from '$lib/fetchHandler';
	import NotifyComp from '$lib/Comps/Notify.svelte';

	export let stockValue;
	export let runValue;
	export let precValue;
	export let startDate;
	export let endDate;
	export let chartNames;
	export let messages;

	async function postConfig(code) {
		let configData = {
			state: code,
			codes: stockValue,
			runs: runValue,
			precision: precValue,
			start: startDate,
			end: endDate
		};
		let resp = await postFetch(configData);
		chartNames = resp.charts;
		messages = resp.messages;
	}

	async function getMsg() {
		let resp = await getFetch();
		messages = resp.messages;
	}
	$: msgProm = getMsg();
</script>

<Stack>
	<Group grow>
		<Button on:click={() => postConfig('c')}>Check Parameters</Button>
		<Button on:click={() => postConfig('r')}>Start Simulation</Button>
	</Group>

	{#await msgProm}
		Waiting
	{:then}
		<NotifyComp {messages} />
	{/await}
</Stack>
<!-- area for review data -->
<!-- {stockValue}
<br />
{runValue}
<br />
{precValue}
<br />
{startDate}
<br />
{endDate}
<br />
{chartNames}
<br /> -->
