import React from 'react'
import { Router } from 'react-router-dom'
import { createMemoryHistory } from 'history'
import { render, fireEvent } from '@testing-library/react'
import Start from './Start'

test('navigates to /upload when a model method is selected', () => {
    const history = createMemoryHistory()
    const { container, getByTestId } = render(
        <Router history={history}>
            <Start />
        </Router>
    )
    expect(container.innerHTML).toMatch('Welcome')
    expect(history.location.pathname).toEqual('/')
    fireEvent.click(getByTestId('start-button'))
    expect(history.location.pathname).toEqual('/')

    fireEvent.click(getByTestId('method-radio').children[0])
    fireEvent.click(getByTestId('start-button'))
    expect(history.location.pathname).toEqual('/upload')
})

test('makes a reset request when reset is clicked', () => {
    const history = createMemoryHistory()
    const { container, getByTestId } = render(
        <Router history={history}>
            <Start />
        </Router>
    )
    fireEvent.click(getByTestId('reset-button'))
})
