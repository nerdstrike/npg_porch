<script>
import PipelineList from "./pipeline_list.svelte";
import TaskList from "./task_list.svelte";

let pipeline_name = null;

function pipelineSelected(event) {
    console.log(event.detail)
    pipeline_name = event.detail.pipeline_name
}
</script>

<PipelineList on:message={pipelineSelected}/>

{#if pipeline_name}
<TaskList pipelineName={pipeline_name}/>
{/if}
