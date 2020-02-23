import { Machine, actions } from 'xstate'
const { assign } = actions

const fetchData = (_, e) =>
    fetch(`http://localhost:8080/stats`, {
        headers: {
            clientId: window.localStorage.getItem('clientId'),
        },
    }).then(res => res.json())

const statsMachine = Machine({
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
            entry: 'notifySuccess',
            on: {
                DONE: 'done',
            },
        },
        done: {
            type: 'final',
        },
        failure: {
            on: {
                RETRY: 'loading',
            },
        },
    },
    actions: {
        notifySuccess: ctx => console.log('Results: ', ctx.data),
    },
})

export default statsMachine
