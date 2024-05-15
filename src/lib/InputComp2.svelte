<script>
	import { Input, InputWrapper } from '@svelteuidev/core';
	export let value;
	export let display;
	export let explain;
	export let defValue;

	function onChange(e) {
		value = e.detail;
	}

	function formatLargeNumber(value) {
		return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
	}
</script>

<InputWrapper label={display} description={explain} >
	<Input {value} on:change={onChange} placeholder={defValue}/>
</InputWrapper>

<!-- stepHoldInterval={(t) => Math.max(100 / t ** 2, 10)}
		formatter={(value) => (Number.isNaN(parseInt(value)) ? 'NaN' : formatLargeNumber(value))} -->

<!-- step={stepInc}
		min={valMin}
		max={valMax} -->
<!-- description={`Restricted to ${formatLargeNumber(valMin)} and ${formatLargeNumber(valMax)} on website`} -->
