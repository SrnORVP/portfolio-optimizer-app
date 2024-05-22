<script>
	import { Group, Button, Divider, Grid, Notification, Space, Text } from '@svelteuidev/core';
	import { Accordion } from '@svelteuidev/core';
	import { Tooltip } from '@svelteuidev/core';
	import { ExclamationTriangle, Check } from 'radix-icons-svelte';

	export let messages;
	// $: messages, console.log(messages);

	let buttonStyle = { minWidth: '5rem' };
	// let tooltipStyle = { maxWidth: '10rem' };
	function errColor(toggle) {
		return toggle ? 'red' : 'green';
	}
</script>

<Group position="center">
	{#each messages as { display, explain, err }}
		<Tooltip label={explain} position="bottom" placement="center" wrapLines width={'20rem'}>
			<Button
				variant="light"
				radius="md"
				color={errColor(err)}
				override={buttonStyle}
				ripple
				compact
				uppercase
			>
				{#if err}
					<ExclamationTriangle slot="leftIcon" size={18} />
				{:else}
					<Check slot="leftIcon" size={18} />
				{/if}
				&nbsp{display}
			</Button>
		</Tooltip>
	{/each}
</Group>
