<script>
	import { TypographyProvider } from '@svelteuidev/core';
	import SvelteMarkdown from 'svelte-markdown';

	const markdown = `
    # This is a title
    `;

	async function fetchMD() {
		const prom = await fetch('README.md').then((resp) => resp.text());
		return prom;
	}

	let PromMD = fetchMD();
</script>

<TypographyProvider>
	{#await PromMD then md}
		<SvelteMarkdown source={md} />
	{/await}
</TypographyProvider>
