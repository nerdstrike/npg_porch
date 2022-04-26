<script>
    let source = new URL('http://0.0.0.0:8000/tasks');
    let service_uri = new URL('http://0.0.0.0:8000/');
    let apiToken = '9437ce958e9f4a4dbd51b4c8a2567466';

    function load_tasks(name) {
        var query = source;
        query.searchParams.append('pipeline_name', name);
        console.log('Request:' + query);
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
<h2>Some tasks for pipeline {pipelineName}</h2>
<table>
    <tr><th>Task input ID</th><th>Task input</th><th>Status</th></tr>
        {#await load_tasks(pipelineName)}
            <tr><td>Loading</td></tr>
        {:then pipelines}
            {#each pipelines as {name, uri, version}, i}
            <tr>
                <td>{name}</td><td>{uri}</td><td>{version}</td>
            </tr>
            {/each}
        {:catch error}
            <tr><td>It's all gone wrong!</td></tr>
        {/await}
</table>
</div>

<style>

</style>