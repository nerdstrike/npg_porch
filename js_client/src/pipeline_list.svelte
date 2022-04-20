<script>
    let service_uri = new URL('http://0.0.0.0:8000/pipelines');
    let source = new URL('http://0.0.0.0:8000/pipelines');
    let apiToken = '9437ce958e9f4a4dbd51b4c8a2567466';
    export let freeExpression = undefined;

    let pipeline_promise = fetch(source, {
        headers: {
            'Accept': 'application/json',
            'Origin': service_uri,
            'Authorization': 'Bearer ' + apiToken
        },
        redirect: 'follow'
    }).then(response => response.json());
</script>
<div>
    <h1>Here be {freeExpression} dragons</h1>
    <div>Data source = {source}</div>
</div>

<div>
    <h2>Some pipelines</h2>
    <table>
        <tr><th>Pipeline name</th><th>URI</th><th>Version</th></tr>
        {#await pipeline_promise}
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
    th {
        font-weight: bold;
        background-color: #9292ff
    }
</style>