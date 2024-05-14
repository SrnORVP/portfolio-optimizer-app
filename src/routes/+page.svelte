<script>
	import InputComp from '$lib/storeComp/InputComp.svelte';
	import SelectComp from '$lib/selectComp.svelte';
	// import InputCompDefault from '$lib/storeComp/InputCompDefault.svelte';
	// import RadioComp from '$lib/storeComp/RadioComp.svelte';
	// import SubmitComp from '$lib/storeComp/SubmitComp.svelte';
	let stuff = 'yoyoyo';
</script>

<div>
	<h1>Welcome to My App</h1>
	<br />
	<hr />
</div>

<div>
	<h2>Choose operation:</h2>
	<!-- <InputCompDefault /> -->
	<!-- <InputComp /> -->
	<SelectComp />
	<!-- <RadioComp /> -->
	<hr />
</div>

<div>
	<!-- <SubmitComp /> -->
	<hr />
</div>

<style>
	h1 {
		color: white;
		text-align: center;
		margin: 1rem 1rem 0.5rem 1rem;
	}
	h2 {
		color: white;
		margin: 1rem 1rem 0.5rem 1rem;
	}
</style>
