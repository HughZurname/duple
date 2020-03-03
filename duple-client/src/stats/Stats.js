import React from 'react'
import { useMachine } from '@xstate/react'
import { Redirect } from 'react-router-dom'

import { Box, Button, Text } from 'grommet'

import statsMachine from './statsMachine'

const Stats = ({ onResolve }) => {
    const [state, send, service] = useMachine(statsMachine)

    const Actions = ({ children }) => (
        <Box direction='column' align='center' gap='small'>
            <Text style={{ width: '8em', textAlign: 'center' }} size='large'>
                Results
            </Text>
            <Box direction='row' gap='medium'>
                {children}
            </Box>
        </Box>
    )

    const Records = ({ records }) => (
        <Box direction='column' align='center' gap='small'>
            <Text style={{ width: '8em', textAlign: 'start' }} size='medium'>
                {records}
            </Text>
            <Text style={{ width: '8em', textAlign: 'start' }}>
                records processed
            </Text>
        </Box>
    )

    const Duplicates = ({ duplicates }) => (
        <Box direction='column' align='center' gap='small'>
            <Text
                weight='bold'
                style={{ width: '8em', textAlign: 'end' }}
                size='medium'>
                {duplicates}
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
                        <Button disabled={true} gap='medium' label='Download' />
                        <Button primary disabled={true} label='Done' />
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
                            disabled={false}
                            gap='medium'
                            label='Download'
                            href={`http://localhost:8080/results/file?clientId=${window.localStorage.getItem(
                                'clientId'
                            )}`}
                            onClick={() => send('DOWNLOAD')}
                        />
                        <Button primary disabled={true} label='Done' />
                    </Actions>
                    <Duplicates duplicates={state.context.data.duplicates} />
                </Box>
            )
        case 'download':
            return (
                <Box direction='row' justify='between' pad='small'>
                    <Records records={state.context.data.records} />
                    <Actions loading={false}>
                        <Button disabled={true} gap='medium' label='Download' />
                        <Button
                            primary
                            disabled={false}
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
                            disabled={false}
                            label='Retry'
                            onClick={() => send('RETRY')}
                        />
                        <Button
                            primary
                            disabled={false}
                            label='Done'
                            onClick={() => send('DONE')}
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
