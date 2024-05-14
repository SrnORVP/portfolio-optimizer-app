<script>
	// import { pathString, initString } from './store';
	// let initialPath = initString
	let initString = "asdfadsfsdfds";
	let inputPath = initString;

	function hChange(e) {
		// pathString.validate(e);
	}

	function hClick(e) {
		if (e.target.value == initString) {
			e.target.value = "";
		}
	}

	function hOut(e) {
		if (e.target.value == "") {
			e.target.value = initString;
		}
	}

	async function hReset(e) {
		console.log(e);
		let a = await fetch("/abc").then((e) => e.json());
		console.log(a);
		e.target.value = a

		// console.log(a);
		// return a;
		// 	pathString.reset();
		// 	inputPath = $pathString;
	}
</script>

<div>
	<label for="pathIP">
		<input value="aaaaa" on:click={hReset} />
		<!-- <button on:click={hReset}> Reset </button> -->
	</label>
</div>

<br />

<!-- <div>
	<label for="status">
		Status:
		<p name="status">{$pathString}</p>
	</label>
</div> -->

<style>
	label {
		color: white;
		/* margin: 1rem 1rem 1rem 1rem; */
	}

	input[type="text"] {
		width: 80%;
		padding: 0.5rem 0.5rem;
		margin: 0.5rem 1rem 0.5rem 1rem;
		box-sizing: border-box;
		/* box-sizing: content-box; */
	}
	button {
		height: 2.5rem;
	}
</style>
