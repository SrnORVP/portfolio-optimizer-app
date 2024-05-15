<script>
	import { Month } from '@svelteuidev/dates';
	import { ActionIcon, Group, Stack, NumberInput, InputWrapper } from '@svelteuidev/core';

	export let display;

	let value = new Date();
	console.log(value);

	let yearVal = value.getFullYear();
	let monthVal = value.getMonth();
	let dayVal = value.getDate();
	let changed;

	function getMonthString(val, offset) {
		let tmp = new Date();
		tmp.setMonth(val + offset);
		return tmp.toLocaleString('default', { month: 'long' });
	}

	function offsetMonth(offset) {
		monthVal = monthVal + offset;
		yearVal = monthVal === -1 ? yearVal - 1 : yearVal;
		yearVal = monthVal === 12 ? yearVal + 1 : yearVal;

		monthVal = monthVal === -1 ? 11 : monthVal;
		monthVal = monthVal === 12 ? 0 : monthVal;
		// value = new Date(yearVal, monthVal, dayVal);
	}

	$: prev = getMonthString(monthVal, -1);
	$: next = getMonthString(monthVal, 1);
	$: dateDesc = `${yearVal}-${monthVal}-${dayVal}`;
	$: value = new Date(yearVal, monthVal, dayVal);
	$: console.log(dateDesc, value);

	//  $: value
</script>

<InputWrapper label={display} description={dateDesc}>
	<Stack>
		<Group grow position="center">
			<ActionIcon variant="default" on:click={() => offsetMonth(-1)}>{`< ${prev}`}</ActionIcon>
			<NumberInput bind:value={yearVal} hideControls />
			<ActionIcon variant="default" on:click={() => offsetMonth(1)}>{`${next} >`}</ActionIcon>
		</Group>
		<!-- {#key monthVal} -->
			<Month
				bind:value
				bind:month={value}
				firstDayOfWeek="sunday"
				onChange={(val) => (value = val)}
			/>
		<!-- {/key} -->
	</Stack>
</InputWrapper>

<!-- description={`Restricted to ${formatLargeNumber(valMin)} and ${formatLargeNumber(valMax)} on website`} -->
