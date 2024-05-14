<script>
	// import { SvelteUIProvider } from '@svelteuidev/core';
</script>

<!-- <SvelteUIProvider withNormalizeCSS withGlobalStyles themeObserver="dark"> -->
	<nav>
		<ul>
			<li><a href="/">Home</a></li>
			<li><a href="/about">About</a></li>
			<li><a href="/chart">Chart</a></li>
		</ul>
		<br />
	</nav>
	<slot />
<!-- </SvelteUIProvider> -->

<style>
	nav ul {
		list-style-type: none;
		margin: 0;
		padding: 0;
		overflow: hidden;
		background-color: #000000;
	}

	nav li {
		float: left;
	}

	nav li a {
		display: block;
		color: white;
		text-align: center;
		padding: 14px 16px;
		text-decoration: none;
	}

	/* Change the link color to #111 (black) on hover */
	nav li a:hover {
		background-color: #111;
	}
</style>
