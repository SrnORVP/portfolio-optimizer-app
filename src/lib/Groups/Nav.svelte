<script>
	import { Stack, Center, Space, Group, Title, Flex, Divider } from '@svelteuidev/core';

	let overrideStyle = {
		'font-size': '4rem'
		// padding: '0 4rem '
	};
</script>

<Stack override={overrideStyle}>
	<Flex gap="sm">
		<Center>
			<a href="/" style="text-decoration:none;"
				><Title order={2} override={overrideStyle}>Asset Allocation</Title></a
			>
		</Center>
		<Stack>
			<Space h="xs" />
			<Title order={3}>using Monte Carlo Simulation</Title>
		</Stack>
	</Flex>
	<Divider override={overrideStyle}></Divider>
</Stack>
