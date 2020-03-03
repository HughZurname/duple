import { Machine, actions } from 'xstate'
const { assign } = actions

const fetchData = (_, e) =>
    fetch(`http://localhost:8080/results`, {
        headers: {
            clientId: window.localStorage.getItem('clientId'),
        },
    }).then(res => res.json())

const resultsMachine = Machine({
    id: 'stats',
    initial: 'loading',
    context: {
        data: undefined,
        error: undefined,
    },
    states: {
        loading: {
            invoke: {
                src: (context, event) => fetchData(context, event),
                onDone: {
                    target: 'success',
                    actions: assign({
                        data: (_, event) => event.data,
                    }),
                },
                onError: {
                    target: 'failure',
                    actions: assign({
                        error: (_, event) => event.data,
                    }),
                },
            },
        },
        success: {
            entry: ctx => console.log('Results: ', ctx.data),
            on: {
                DONE: 'done',
            },
        },
        done: {
            type: 'final',
        },
        failure: {
            entry: ctx => console.error('Failure: ', ctx),
            on: {
                RETRY: 'loading',
            },
        },
    },
})

export default resultsMachine
