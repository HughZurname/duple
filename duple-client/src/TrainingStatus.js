import React from 'react'
import { Grommet, Box, Button, Text } from 'grommet'

import { grommet } from 'grommet/themes'

const TrainingStatus = props => {
    const positiveIds = props.positiveIds
    const negativeIds = props.negativeIds
    const attempts = props.attempts

    return (
        <Grommet theme={grommet}>
            <Box direction='row' justify='between'>
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
                        size='large'>{`${attempts}/3 attempts`}</Text>
                    <Box
                        direction='row'
                        gap='small'
                        pad={{
                            vertical: 'small',
                            horizontal: 'medium',
                        }}>
                        <Button
                            label='Clear'
                            onClick={() => props.handleClear()}
                        />
                        <Button
                            primary
                            label='Submit'
                            onClick={() => props.handleSubmit()}
                        />
                    </Box>
                </Box>
                <Box direction='column' align='center' gap='small'>
                    <Text
                        style={{ width: '8em', textAlign: 'end' }}
                        size='medium'>
                        {negativeIds.length}
                    </Text>
                    <Text style={{ width: '8em', textAlign: 'end' }}>
                        negative
                    </Text>
                </Box>
            </Box>
        </Grommet>
    )
}

export default TrainingStatus
