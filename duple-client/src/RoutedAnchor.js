import React from 'react'
import { withRouter } from 'react-router-dom'
import { Anchor } from 'grommet'

export default withRouter(props => {
    if (!props.to) return <Anchor {...props} />

    return (
        <Anchor
            {...props}
            href={props.to}
            onClick={event => {
                event.preventDefault()
                props.history.push(props.to)
            }}
        />
    )
})
