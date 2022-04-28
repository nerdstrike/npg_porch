<script>
import PipelineList from "./pipeline_list.svelte";
import TaskList from "./task_list.svelte";

let pipeline_name = null;

function pipelineSelected(event) {
    console.log(event.detail)
    pipeline_name = event.detail.pipeline_name
}
</script>

<PipelineList on:message={pipelineSelected} tableStyle="stripey"/>

{#if pipeline_name}
<TaskList pipelineName={pipeline_name} tableStyle="stripey"/>
{/if}

<style>
    :global(table.stripey) {
        border: 1px solid;
        border-radius: 5px;
    }
    :global(tr, th, td) {
        padding: 10px;
        text-align: left;
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
</style>
