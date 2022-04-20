import App from './pipeline_list.svelte';

const app = new App({
    target: document.body,
    props: {
        freeExpression: 'big'
    }
});

export default app;
