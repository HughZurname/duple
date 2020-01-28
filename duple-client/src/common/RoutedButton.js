import React from 'react'
import { withRouter } from 'react-router-dom'
import { Button } from 'grommet'

export default withRouter(props => {
    if (!props.to) return <Button {...props} />
    if (props.disabled) return <Button {...props} />

    return (
        <Button
            {...props}
            href={props.to}
            onClick={event => {
                event.preventDefault()
                props.history.push(props.to)
            }}
        />
    )
})
