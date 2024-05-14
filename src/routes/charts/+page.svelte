<script>
    let selected = "";

    $: chartPromise = (async function loadChart(inputParam) {
        const res = await fetch(`/111`).then((e) => e.text());
        // const res = await fetch(`/charts/${inputParam}`).then((e) => e.text());
        // console.debug(res)
        return res;
    })(selected);

</script>

<h1>chart chart chart</h1>

<div>
    {#await chartPromise}
        Select chart to displace
    {:then chart_svg}
        {@html chart_svg}
    {:catch errName}
        errName
    {/await}
</div>

<!-- {@html chart_svg} -->
