import React from 'react'
import { Grommet, Box, Button, Text } from 'grommet'

import { grommet } from 'grommet/themes'

const TrainingStatus = props => {
    const positiveIds = props.state.positiveIds
    const negativeIds = props.state.negativeIds
    const attempts = props.state.attempts

    return (
        <Grommet theme={grommet}>
            <Box direction='row' justify='between'>
                <Text
                    style={{ width: '8em', textAlign: 'start' }}
                    size='large'>{`${positiveIds.length} postive`}</Text>
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
                <Text
                    style={{ width: '8em', textAlign: 'end' }}
                    size='large'>{`${negativeIds.length} negative`}</Text>
            </Box>
        </Grommet>
    )
}

export default TrainingStatus
