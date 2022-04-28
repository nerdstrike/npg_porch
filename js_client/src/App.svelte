<script>
import PipelineList from "./pipeline_list.svelte";
import TaskList from "./task_list.svelte";

let pipeline_name = null;

function pipelineSelected(event) {
    console.log(event.detail)
    pipeline_name = event.detail.pipeline_name
}
</script>
<h1>Porch Pipeline Status Viewer</h1>
<div class="upper">
    <PipelineList on:message={pipelineSelected} tableStyle="stripey"/>
</div>
<div class="lower">
    {#if pipeline_name}
    <TaskList pipelineName={pipeline_name} tableStyle="stripey"/>
    {/if}
</div>

<style>
    :global(table.stripey) {
        border: 1px solid;
        border-radius: 5px;
    }
    :global(tr, th, td) {
        padding: 10px;
        text-align: left;
        border: 1px solid;
    }
    :global(tr) {
        background-color: #ffffff;
        border: 5px;
    }
    :global(tr:nth-child(even)) {background-color: #a2a2a2;}
    :global(tr.selectable:hover) {background-color: #ddd;}
    :global(th) {
        font-weight: bold;
        background-color: #9292ff
    }
    :global(caption) {
        font-size: large;
        font-weight: bold;
    }
    .upper {
        position: absolute;
        top: 10%;
        bottom: 45%;
        width: 100%;
    }
    .lower {
        position: sticky;
        top: 55%;
        bottom: 95%;
        width: 100%;
    }
</style>
