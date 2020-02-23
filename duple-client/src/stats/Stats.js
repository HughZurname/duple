import React from 'react'
import { useMachine } from '@xstate/react'
import { Redirect } from 'react-router-dom'

import { Box, Button, Text } from 'grommet'

import statsMachine from './statsMachine'

const Stats = ({ onResolve }) => {
    const [state, send, service] = useMachine(statsMachine)

    const Actions = props => (
        <Box direction='column' align='center' gap='small'>
            <Text style={{ width: '8em', textAlign: 'center' }} size='large'>
                Results
            </Text>
            <Box direction='row' gap='medium'>
                {props.children}
            </Box>
        </Box>
    )

    const Records = props => (
        <Box direction='column' align='center' gap='small'>
            <Text style={{ width: '8em', textAlign: 'start' }} size='medium'>
                {props.records}
            </Text>
            <Text style={{ width: '8em', textAlign: 'start' }}>
                records processed
            </Text>
        </Box>
    )

    const Duplicates = props => (
        <Box direction='column' align='center' gap='small'>
            <Text
                weight='bold'
                style={{ width: '8em', textAlign: 'end' }}
                size='medium'>
                {props.duplicates}
            </Text>
            <Text weight='bold' style={{ width: '8em', textAlign: 'end' }}>
                duplicates found
            </Text>
        </Box>
    )

    switch (state.value) {
        case 'loading':
            return (
                <Box direction='row' justify='between' pad='small'>
                    <Text>Loading...</Text>
                    <Actions loading={false}>
                        <Button
                            primary
                            disabled={true}
                            gap='medium'
                            label='Download'
                            onClick={() => send('RETRY')}
                        />
                        <Button
                            disabled={true}
                            color='accent-1'
                            label='Done'
                            onClick={() => send('DONE')}
                        />
                    </Actions>
                    <Text>Loading...</Text>
                </Box>
            )
        case 'success':
            return (
                <Box direction='row' justify='between' pad='small'>
                    <Records records={state.context.data.records} />
                    <Actions loading={false}>
                        <Button
                            primary
                            disabled={false}
                            gap='medium'
                            label='Download'
                            onClick={() => send('RETRY')}
                        />
                        <Button
                            disabled={false}
                            color='accent-1'
                            label='Done'
                            onClick={() => send('DONE')}
                        />
                    </Actions>
                    <Duplicates duplicates={state.context.data.duplicates} />
                </Box>
            )
        case 'failure':
            return (
                <Box direction='row' justify='between' pad='small'>
                    <Text>Failed!</Text>
                    <Actions loading={false}>
                        <Button
                            primary
                            disabled={false}
                            gap='medium'
                            label='Download'
                            onClick={() => send('RETRY')}
                        />
                        <Button
                            disabled={false}
                            color='accent-1'
                            label='Done'
                            onClick={() => send('RETRY')}
                        />
                    </Actions>
                    <Text>Failed!</Text>
                </Box>
            )
        case 'done':
            return <Redirect to='/' />
        default:
            return null
    }
}

export default Stats
