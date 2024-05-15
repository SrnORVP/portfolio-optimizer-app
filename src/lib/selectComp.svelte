<script>
	import FrameComp from '$lib/frameComp.svelte';

	const sels = [1, 2, 3];
	const initValue = '--';

	let selected = initValue;
	let param = 1;

	function multi(arr, multiplier) {
		return arr.map((x) => x * multiplier);
	}

	$: dataPromise = (async function loadCompData(inputParam) {
		const res = await fetch('/chartList').then((e) => e.json());

		const opts = [initValue, ...res];
		// const opts = [initValue, ...multi(res, inputParam)];

		console.debug(inputParam);
		return opts;
	})(param);
</script>

<div>
	<select name="sel1" id="sel1" bind:value={param}>
		{#each sels as sel}
			<option value={sel}> {sel} </option>
		{/each}
	</select>

	{#await dataPromise}
		<select name="sel" id="sel">
			<option value={initValue}> {initValue} </option>
		</select>
	{:then opts}
		<select name="sel" id="sel" bind:value={selected}>
			{#each opts as opt}
				<option value={opt}> {opt} </option>
			{/each}
		</select>
	{/await}
</div>
<br />
{selected === initValue ? '' : selected}
<br />

<div>
	<FrameComp bind:chartName={selected} />
</div>

<br />

<style>
	label {
		color: white;
		/* margin: 1rem 1rem 1rem 1rem; */
	}

	select {
		width: 10%;
		padding: 0.5rem 0.5rem;
		margin: 0.5rem 1rem 0.5rem 1rem;
		box-sizing: border-box;
		/* box-sizing: content-box; */
	}
	button {
		height: 2.5rem;
	}
</style>
