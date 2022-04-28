<script>
import { loop_guard } from "svelte/internal";

    let source = new URL('http://0.0.0.0:8000/tasks');
    let service_uri = new URL('http://0.0.0.0:8000/');
    let apiToken = '9437ce958e9f4a4dbd51b4c8a2567466';

    export let tableStyle;

    function load_tasks(name) {
        var query = source;
        query.searchParams.append('pipeline_name', name);
        // console.log('Request:' + query);
        return fetch(query, {
            headers: {
                'Accept': 'application/json',
                'Origin': service_uri,
                'Authorization': 'Bearer ' + apiToken
            },
            redirect: 'follow'
        }).then(response => response.json());
    }

    export let pipelineName;
    $: pipelineName;
</script>

<div>
<table class={tableStyle}>
    <caption>Some tasks for pipeline <em>{pipelineName}</em></caption>
    <tr><th>Task input ID</th><th>Task input</th><th>Status</th></tr>
        {#await load_tasks(pipelineName)}
            <tr><td>Loading</td></tr>
        {:then tasks}
            {#each tasks as {task_input, task_input_id, status}, i}
            <tr>
                <td>{task_input_id}</td>
                <td>{JSON.stringify(task_input, null, 2)}</td>
                <td>{status}</td>
            </tr>
            {/each}
        {:catch error}
            <tr><td>It's all gone wrong!</td></tr>
        {/await}
</table>
</div>
