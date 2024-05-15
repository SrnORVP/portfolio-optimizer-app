<script>
	import { NativeSelect } from '@svelteuidev/core';
	export let value;
	export let numStock;

	let dis2 = numStock > 6 ? true : false;
	let dis3 = numStock > 3 ? true : false;
	let dataList = [
		{ label: '1dp (i.e. 0, 0.1, 0.2 ... 1.0)', value: 1 },
		{ label: '2dps (i.e. 0, 0.01, 0.02 ... 1.00)', value: 2, disabled: dis2 },
		{ label: '3dps (i.e. 0, 0.001, 0.002 ... 1.000)', value: 3, disabled: dis3 }
	];
</script>

<NativeSelect
	data={dataList}
	bind:value
	placeholder="Pick one"
	label="Precision of weights"
	description="Higher precision = more allocation combinations"
/>
