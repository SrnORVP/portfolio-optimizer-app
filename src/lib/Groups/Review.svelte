<script>
	import { Button, Stack, InputWrapper, Group } from '@svelteuidev/core';

	import { getFetch, postFetch } from '$lib/fetchHandler';
	import NotifyComp from '$lib/Comps/Notify.svelte';

	export let stockValue;
	export let runValue;
	export let precValue;
	export let startDate;
	export let endDate;
	export let chartNames;
	export let messages;

	let isChecking = false;
	let isRunning = false;
	let isDisable = false;
	let disableDisp = 'Refer to warning below.';

	async function postConfig(code) {
		let configData = {
			state: code,
			codes: stockValue,
			runs: runValue,
			precision: precValue,
			start: startDate,
			end: endDate
		};
		if (code == 'c') {
			isChecking = true;
		}
		if (code == 'r') {
			isRunning = true;
		}
		let resp = await postFetch(configData);
		chartNames = resp.charts;
		messages = resp.messages;
		if (messages !== '') {
			setDisable(messages);
		}
		isChecking = false;
		isRunning = false;
	}

	async function getMsg() {
		let resp = await getFetch();
		messages = resp.messages;
	}

	function setDisable(msgs) {
		let filtered = msgs.filter(({ display, explain, err }) => err);
		isDisable = filtered.length > 0 ? true : false;
	}

	$: msgProm = getMsg();
</script>

<Stack>
	<Group grow>
		<Button ripple loading={isChecking} on:click={() => postConfig('c')}>Check Parameters</Button>
		<InputWrapper label="" error={isDisable ? disableDisp : false}>
			<Button
				ripple
				fullSize
				loading={isRunning}
				disabled={isDisable}
				on:click={() => postConfig('r')}
			>
				Start Simulation
			</Button>
		</InputWrapper>
	</Group>

	{#await msgProm then}
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
