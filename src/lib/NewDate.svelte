<script>
	import { ActionIcon, Group, Stack, NumberInput, InputWrapper, Grid } from '@svelteuidev/core';

	import { createEventDispatcher, onMount } from 'svelte';
	import dayjs from 'dayjs';

	// use locale
	// import 'dayjs/locale/fr';
	// dayjs.locale('fr');

	export let value;
	export let display;

	const arrDays = [...Array(7).keys()].map((x) => dayjs().day(x).format('dd'));

	let selDay = +dayjs().format('D'); // 1..31
	let selMonth = +dayjs().format('M'); // 1..12
	let selYear = +dayjs().format('YYYY'); // year
	let calMat = initCalMat();

	onMount(() => {
		value = dayjs().format('YYYY-MM-DD'); // current day month year in input
		affecteRows();
	});

	function initCalMat() {
		return [
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0]
		];
	}

	function stringProper(str) {
		return str.charAt(0).toUpperCase() + str.substr(1).toLowerCase();
	}

	function affecteRows() {
		calMat = initCalMat();
		const firstDayOfCurrentMonth = stringProper(
			dayjs(selYear + '-' + selMonth)
				.startOf('month')
				.format('dd')
		); // the day of first day of month
		const lastDayOfCurrentMonth = +dayjs(selYear + '-' + selMonth)
			.endOf('month')
			.format('D');
		let iRow = 0;
		let iCol = 0;
		let start = false;
		let cpt = 0;
		for (iRow = 0; iRow < 6; iRow++) {
			arrDays.forEach((daystr) => {
				if (cpt > lastDayOfCurrentMonth) {
					return;
				}
				if (!start && daystr === firstDayOfCurrentMonth) {
					cpt++;
					start = true;
				}
				calMat[iRow][iCol] = cpt;
				iCol++;
				if (start) {
					cpt++;
				}
			});
			iCol = 0;
		}
		selectDate(selYear, selMonth, selDay);
	}

	function getMonthString(val, offset) {
		let tmp = new Date();
		tmp.setMonth(val + offset);
		return tmp.toLocaleString('default', { month: 'long' });
	}

	function changeMonth(offset) {
		selMonth = selMonth + offset;
		if (selMonth <= 0) {
			selMonth = 12;
			selYear--;
		}
		if (selMonth > 12) {
			selMonth = 1;
			selYear++;
		}
		affecteRows();
		selectDate(selYear, selMonth, selDay);
	}

	function selectDate(y, m, d) {
		selDay = d;
		value = dayjs(y + '-' + m + '-' + d).format('YYYY-MM-DD');
	}

	$: dateDesc = value;
</script>

<InputWrapper label={display} description={`Picked: ${dateDesc}`}>
	<Stack spacing={10}>
		<Group grow>
			<ActionIcon variant="default" on:click={() => changeMonth(-1)}
				>{`< ${getMonthString(selMonth, -2)}`}</ActionIcon
			>
			<NumberInput bind:value={selYear} on:change={affecteRows} hideControls />
			<ActionIcon variant="default" on:click={() => changeMonth(1)}
				>{`${getMonthString(selMonth, 0)} >`}</ActionIcon
			>
		</Group>

		<Grid spacing={0} cols={7}>
			{#each arrDays as day}
				<Grid.Col align="center" span={1}>
					<ActionIcon>{day}</ActionIcon>
				</Grid.Col>
			{/each}
			{#each calMat as col}
				{#each col as i}
					<Grid.Col align="center" span={1}>
						{#if i > 0}
							<ActionIcon size="lg" variant="hover" on:click={selectDate(selYear, selMonth, i)}
								>{i}</ActionIcon
							>
						{:else}
							<div />
						{/if}
					</Grid.Col>
				{/each}
			{/each}
		</Grid>

		<!-- <SimpleGrid cols={7} spacing={1}>
		{#each arrDays as day}
			<ActionIcon>{day}</ActionIcon>
		{/each}
		{#each calMat as col}
			{#each col as i}
				{#if i > 0}
					<ActionIcon variant="hover" on:click={selectDate(selYear, selMonth, i)}>{i}</ActionIcon>
				{:else}
					<div />
				{/if}
			{/each}
		{/each}
	</SimpleGrid> -->
	</Stack>
</InputWrapper>
