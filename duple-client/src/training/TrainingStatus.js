import React from 'react'
import { Box, Button, Text } from 'grommet'

const TrainingStatus = props => {
    const positiveIds = props.positiveIds
    const negativeIds = props.negativeIds
    const attempts = props.attempts

    return (
        <Box direction='row' justify='between' pad='small'>
            <Box direction='column' align='center' gap='small'>
                <Text
                    style={{ width: '8em', textAlign: 'start' }}
                    size='medium'>
                    {positiveIds.length}
                </Text>
                <Text style={{ width: '8em', textAlign: 'start' }}>
                    positive
                </Text>
            </Box>
            <Box direction='column' align='center'>
                <Text
                    style={{ width: '8em', textAlign: 'center' }}
                    size='large'>
                    Training
                </Text>
                <Text
                    style={{ width: '8em', textAlign: 'center' }}
                    size='large'>{`${attempts}/${props.totalAttempts} rounds`}</Text>
                <Box
                    direction='row'
                    gap='small'
                    pad={{
                        vertical: 'small',
                        horizontal: 'medium',
                    }}>
                    <Button
                        disabled={props.fetching}
                        label='Clear'
                        onClick={() => props.handleClear()}
                    />
                    <Button
                        disabled={props.fetching}
                        primary
                        label='Continue'
                        onClick={() => props.handleSubmit()}
                    />
                </Box>
            </Box>
            <Box direction='column' align='center' gap='small'>
                <Text style={{ width: '8em', textAlign: 'end' }} size='medium'>
                    {negativeIds.length}
                </Text>
                <Text style={{ width: '8em', textAlign: 'end' }}>negative</Text>
            </Box>
        </Box>
    )
}

export default TrainingStatus
