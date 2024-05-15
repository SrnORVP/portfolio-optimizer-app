<script>
	import { SvelteUIProvider, AppShell, Stack, Header, Divider } from '@svelteuidev/core';

	import NavGroup from './NavGroup.svelte';

	let isDark = false;
	let opened = false;

	function toggleTheme() {
		isDark = !isDark;
	}
	function toggleOpened() {
		opened = !opened;
	}
</script>

<SvelteUIProvider withNormalizeCSS withGlobalStyles themeObserver="dark">
	<div class="flex">
		<AppShell>
			<Stack spacing="xl">
				<NavGroup />
				<slot />
			</Stack>
		</AppShell>
	</div>
</SvelteUIProvider>

<style>
	.flex {
		margin: 5rem 5% 0;
		/* margin-top: 10rem; */
	}
</style>
