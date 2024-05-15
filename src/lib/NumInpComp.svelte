<script>
	import { NumberInput, InputWrapper } from '@svelteuidev/core';
	export let value;
	export let display;
	export let valMin;
	export let valMax;

	$: stepInc = 10 ** Math.floor(Math.log10(value) - 1);

	function onChange(e) {
		value = e.detail;
	}

	function formatLargeNumber(value) {
		return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	}
</script>

<InputWrapper
	label={display}
	description={`Restricted to ${formatLargeNumber(valMin)} and ${formatLargeNumber(valMax)} on website`}
>
	<NumberInput
		{value}
		on:change={onChange}
		step={stepInc}
		min={valMin}
		max={valMax}
		stepHoldInterval={(t) => Math.max(100 / t ** 2, 10)}
		formatter={(value) => (Number.isNaN(parseInt(value)) ? 'NaN' : formatLargeNumber(value))}
	/>
</InputWrapper>

<!-- parser={(value) => value.replace(/(,*)/g, '')} -->
