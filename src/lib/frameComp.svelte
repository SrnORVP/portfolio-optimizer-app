<script>
    export let chartName;
    $: console.debug(chartName);
</script>

<div class="container">
    <iframe
        class="plotFrame"
        id="plotFrame"
        title="Plotly Plots"
        src={`./charts/${chartName}`}
        width="100%"
    >
    </iframe>
</div>

<style>
    .container {
        position: relative;
        overflow: hidden;
        width: 100%;
        padding-top: 56.25%; /* 16:9 Aspect Ratio (divide 9 by 16 = 0.5625) */
    }

    .plotFrame {
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        width: 100%;
        height: 100%;
    }
</style>
