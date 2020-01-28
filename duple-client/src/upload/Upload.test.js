import React from 'react'
import { Router } from 'react-router-dom'
import { createMemoryHistory } from 'history'
import { render, fireEvent } from '@testing-library/react'
import Upload from './Upload'

test('makes a reset request when reset is clicked', () => {
    const history = createMemoryHistory()
    const { container, getByTestId } = render(
        <Router history={history}>
            <Upload />
        </Router>
    )
    console.log(getByTestId('training-upload'))
})
