<script>
	import { NativeSelect, InputWrapper } from '@svelteuidev/core';
	export let value;
	export let display;
	export let explain;
	export let selections;
</script>

<InputWrapper label={display} description={explain}>
	<NativeSelect data={selections} bind:value placeholder="Pick one" />
</InputWrapper>
