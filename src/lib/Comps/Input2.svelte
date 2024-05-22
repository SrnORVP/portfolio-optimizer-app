<script>
	import { TextInput, InputWrapper } from '@svelteuidev/core';
	export let value;
	export let display;
	export let explain;
</script>

<InputWrapper label={display} description={explain}>
	<TextInput bind:value />
</InputWrapper>
