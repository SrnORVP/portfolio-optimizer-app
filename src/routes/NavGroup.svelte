<script>
	import { Stack, Center, Space, Group, Title, Flex, Divider } from '@svelteuidev/core';

	let overrideStyle = {
		'font-size': '4rem'
		// padding: '0 4rem '
	};
</script>

<Stack override={overrideStyle}>
	<Flex gap="xl">
		<Center>
			<a href="/" style="text-decoration:none;"><Title order={1} override={overrideStyle}>Asset Allocation</Title></a>
		</Center>

		<!-- <Stack>
			<Space h="xs" />
			<a href="/" style="text-decoration:none;"><Title order={3}>Home</Title></a>
		</Stack> -->

		<!-- <Stack>
			<Space h="xs" />
			<a href="/chart" style="text-decoration:none;"><Title order={3}>Chart</Title></a>
		</Stack> -->

		<Stack>
			<Space h="xs" />
			<a href="/about" style="text-decoration:none;"><Title order={3}>About</Title></a>
		</Stack>
	</Flex>
	<Divider override={overrideStyle}>aasdsaad</Divider>
</Stack>
