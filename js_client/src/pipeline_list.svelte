<script>
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    let service_uri = new URL('http://0.0.0.0:8000/pipelines');
    let source = new URL('http://0.0.0.0:8000/pipelines');
    let apiToken = '9437ce958e9f4a4dbd51b4c8a2567466';

    let pipeline_promise = fetch(source, {
        headers: {
            'Accept': 'application/json',
            'Origin': service_uri,
            'Authorization': 'Bearer ' + apiToken
        },
        redirect: 'follow'
    }).then(response => response.json());

    function signalLoadTasks(event) {
        console.log('Triggered by pipeline click')
        console.log(event.target.parentElement.id)
        dispatch('message', { pipeline_name: event.target.parentElement.id});
    };
</script>

<div>
    <h2>Some pipelines</h2>
    <table>
        <tr><th>Pipeline name</th><th>URI</th><th>Version</th></tr>
        {#await pipeline_promise}
            <tr><td>Loading</td></tr>
        {:then pipelines}
            {#each pipelines as {name, uri, version}, i}
            <tr id={name} on:click={signalLoadTasks}>
                <td>{name}</td><td>{uri}</td><td>{version}</td>
            </tr>
            {/each}
        {:catch error}
            <tr><td>It's all gone wrong!</td></tr>
        {/await}
    </table>
</div>

<style>
    table {
        border: 1px solid;
        border-radius: 5px;
    }
    tr, th, td {
        padding: 10px;
        text-align: left;
    }
    tr {
        background-color: #ffffff;
        border: 1px;
    }
    tr:nth-child(even){background-color: #a2a2a2;}
    tr:hover {background-color: #ddd;}
    th {
        font-weight: bold;
        background-color: #9292ff
    }
</style>