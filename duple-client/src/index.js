import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import * as serviceWorker from './serviceWorker'

import { FetchProvider } from '@bjornagh/use-fetch'
import uniqid from 'uniqid'

const cache = new Map()
const clientId = window.localStorage.getItem('clientId')

const authenticate = clientId => {
    if (clientId == null)
        fetch('http://localhost:8080/register', {
            headers: { token: uniqid() },
        })
            .then(response => response.ok && response.json())
            .then(data =>
                window.localStorage.setItem('clientId', data.clientId)
            )
}

ReactDOM.render(
    <FetchProvider cache={cache}>
        <App clientId={clientId} />
    </FetchProvider>,
    document.getElementById('root')
)

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.register()
authenticate(clientId)
