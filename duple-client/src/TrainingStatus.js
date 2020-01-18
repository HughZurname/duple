import React from 'react'
import { Grommet, Box, Button, Text } from 'grommet'

import { grommet } from 'grommet/themes'

const TrainingStatus = props => {
    const [positiveIds] = props.state.positiveIds
    const [negativeIds] = props.state.negativeIds
    const [attempts] = props.state.attempts

    return (
        <Grommet theme={grommet}>
            <Box direction='row' justify='between'>
                <Text size='large'>{`${positiveIds.length}/5 postive`}</Text>
                <Box direction='column' align='center'>
                    <Text size='large'>Training</Text>
                    <Text size='large'>{`${attempts}/3 attempts`}</Text>
                    <Box
                        direction='row'
                        gap='small'
                        pad={{
                            vertical: 'small',
                            horizontal: 'medium'
                        }}>
                        <Button
                            primary
                            label='Submit'
                            onClick={() => props.handleSubmit()}
                        />
                        <Button
                            label='Clear'
                            onClick={() => props.handleClear()}
                        />
                    </Box>
                </Box>
                <Text size='large'>{`${negativeIds.length}/5 negative`}</Text>
            </Box>
        </Grommet>
    )
}

export default TrainingStatus
